#! /usr/bin/env python

"""
Implementation of the Pipeline object, and a simple script to instantiate and
run a pipeline (the outputs of which can be plotted and stored to disk).
"""


from __future__ import absolute_import

from argparse import ArgumentParser
from collections import OrderedDict
from collections.abc import Mapping
from configparser import NoSectionError
from copy import deepcopy
from importlib import import_module
from itertools import product
from inspect import getsource
import os
from tabulate import tabulate
from time import time
import traceback

import numpy as np

from pisa import ureg
from pisa.core.events import Data
from pisa.core.map import Map, MapSet
from pisa.core.param import ParamSet, DerivedParam
from pisa.core.stage import Stage
from pisa.core.container import Container, ContainerSet
from pisa.core.binning import MultiDimBinning, OneDimBinning, VarBinning
from pisa.utils.config_parser import PISAConfigParser, parse_pipeline_config
from pisa.utils.fileio import mkdir
from pisa.utils.format import format_times
from pisa.utils.hash import hash_obj
from pisa.utils.log import logging, set_verbosity
from pisa.utils.profiler import profile


__all__ = ["Pipeline", "test_Pipeline", "parse_args", "main"]

__author__ = "J.L. Lanfranchi, P. Eller"

__license__ = """Copyright (c) 2014-2025, The IceCube Collaboration

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License."""


# TODO: should we check that the output binning of a previous stage produces
# the inputs required by the current stage, or that the aggregate outputs that
# got produced by previous stages (less those that got consumed in other
# previous stages) hold what the current stage requires for inputs... or
# should we not assume either will check out, since it's possible that the
# stage requires sideband objects that are to be introduced at the top of the
# pipeline by the user (and so there's no way to verify that all inputs are
# present until we see what the user hands the pipeline as its top-level
# input)? Alternatively, the lack of apparent inputs for a stage could show
# a warning message. Or we just wait to see if it fails when the user runs the
# code.


class Pipeline():
    """Instantiate stages according to a parsed config object; excecute
    stages.

    Parameters
    ----------
    config : string, OrderedDict, or PISAConfigParser
        If string, interpret as resource location; send to the
        `config_parser.parse_pipeline_config()` method to get a config
        OrderedDict. If `OrderedDict`, use directly as pipeline configuration.

    profile : bool
        Perform timings

    """

    def __init__(self, config, profile=False):
        if isinstance(config, (str, PISAConfigParser)):
            config = parse_pipeline_config(config=config)
        elif isinstance(config, OrderedDict):
            pass
        else:
            raise TypeError(
                "`config` passed is of type %s but must be string,"
                " PISAConfigParser, or OrderedDict" % type(config).__name__
            )

        self.pisa_version = None

        self.name = config['pipeline']['name']
        self.data = ContainerSet(self.name)
        self.detector_name = config['pipeline']['detector_name']
        self._output_binning = config['pipeline']['output_binning']
        self.output_key = config['pipeline']['output_key']

        self._profile = profile
        self._setup_times = []
        self._run_times = []
        self._get_outputs_times = []

        self._stages = []
        self._config = config
        self._init_stages()
        self._source_code_hash = None

        if isinstance(self._output_binning, VarBinning):
            self.assert_varbinning_compat()
            self.assert_exclusive_varbinning()

        # check in case someone decided to add a non-daemonflux parameter with daemon_
        # in it, which would potentially make penalty calculation incorrect
        if "daemon_chi2" in self.params.names:
            num_daemon_params = len([name for name in self.params.names if "daemon_" in name])
            assert num_daemon_params == self.params["daemon_params_len"].value.m_as("dimensionless"), \
                    'Incorrect number of parameters with "daemon_" in their name detected. Non-daemonflux parameters can not have "daemon_" in their name. Rename your non-daemonflux parameters which do not comly!'

        self._covariance_set = False

    def __repr__(self):
        return self.tabulate(tablefmt="presto")

    def _repr_html_(self):
        return self.tabulate(tablefmt="html")

    def tabulate(self, tablefmt="plain"):
        headers = ['stage number', 'name', 'calc_mode', 'apply_mode', 'has setup', 'has compute', 'has apply', '# fixed params', '# free params']
        colalign=["right"] + ["center"] * (len(headers) -1 )
        table = []
        for i, s in enumerate(self.stages):
            table.append([i, s.__class__.__name__, s.calc_mode, s.apply_mode])
            table[-1].append(s.setup_function.__func__.__module__ == s.__class__.__module__)
            table[-1].append(s.compute_function.__func__.__module__ == s.__class__.__module__)
            table[-1].append(s.apply_function.__func__.__module__ == s.__class__.__module__)
            table[-1] += [len(s.params.fixed), len(s.params.free)]
        return tabulate(table, headers, tablefmt=tablefmt, colalign=colalign)

    def report_profile(self, detailed=False, format_num_kwargs=None):
        """Report timing information on pipeline and contained services

        Parameters
        ----------
        detailed : bool, default False
            Whether to increase level of detail
        format_num_kwargs : dict, optional
            Dictionary containing arguments passed to `utils.format.format_num`.
             Will display each number with three decimal digits by default.

        """
        if not self.profile:
            # Report warning only at the pipeline level, which is what the
            # typical user should come across. Assume that users calling
            # `report_profile` on a `Stage` instance directly know what they're
            # doing.
            logging.warn(
                '`profile` is set to False. Results may not show the expected '
                'numbers of function calls.'
            )
        if format_num_kwargs is None:
            format_num_kwargs = {
                'precision': 1e-3, 'fmt': 'full', 'trailing_zeros': True
            }
        assert isinstance(format_num_kwargs, Mapping)
        print(f'Pipeline: {self.name}')
        for func_str, times in [
            ('- setup:       ', self._setup_times),
            ('- run:         ', self._run_times),
            ('- get_outputs: ', self._get_outputs_times)
        ]:
            print(func_str,
                format_times(times=times,
                             nindent_detailed=len(func_str) + 1,
                             detailed=detailed, **format_num_kwargs)
            )
        print('Individual services:')
        for stage in self.stages:
            stage.report_profile(detailed=detailed, **format_num_kwargs)

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, value):
        for stage in self.stages:
            stage.profile = value
        self._profile = value

    def index(self, stage_id):
        """Return the index in the pipeline of `stage_id`.

        Parameters
        ----------
        stage_id : string or int
            Name of the stage, or stage number (0-indexed)

        Returns
        -------
        idx : integer stage number (0-indexed)

        Raises
        ------
        ValueError : if `stage_id` not in pipeline.

        """
        assert isinstance(stage_id, (int, str))
        for stage_num, stage in enumerate(self):
            if stage_id in [stage_num, stage.stage_name]:
                return stage_num
        raise ValueError('No stage "%s" found in the pipeline.' % stage_id)

    def __len__(self):
        return len(self._stages)

    def __iter__(self):
        return iter(self._stages)

    def __getitem__(self, idx):
        if isinstance(idx, str):
            return self.stages[self.index(idx)]

        if isinstance(idx, (int, slice)):
            return self.stages[idx]

        raise ValueError(
            'Cannot locate stage "%s" in pipeline. Stages'
            " available are %s." % (idx, self.stage_names)
        )

    def __getattr__(self, attr):
        for stage in self:
            if stage.stage_name == attr:
                return stage
        raise AttributeError(
            '"%s" is neither a stage in this pipeline nor an attribute/property'
            " of the `Pipeline` object." % attr
        )

    def _init_stages(self):
        """Stage factory: Instantiate stages specified by self.config.

        Conventions required for this to work:
            * Stage and service names must be lower-case
            * Service implementations must be found at Python path
              `pisa.stages.<stage_name>.<service_name>`
            * `service` cannot be an instantiation argument for a service

        """
        stages = []
        for stage_num, item in enumerate(
            self.config.items()
        ):
            try:
                name, settings = item

                if isinstance(name, str):
                    if name == 'pipeline':
                        continue

                stage_name, service_name = name

                # old cfgs compatibility
                if service_name.startswith('pi_'):
                    logging.warning(f"Old stage name `{service_name}` is automatically renamed to `{service_name.replace('pi_', '')}`. " +
                                    "Please change your config in the future!")
                service_name = service_name.replace('pi_', '')

                logging.debug(
                    "instantiating stage %s / service %s", stage_name, service_name
                )

                # Import service's module
                logging.trace(f"Importing service module: {stage_name}.{service_name}")
                try:
                    module_path = f"pisa.stages.{stage_name}.{service_name}"
                    module = import_module(module_path)
                except:
                    logging.debug(
                        f"Module {stage_name}.{service_name} not found in PISA, trying "
                        "to import from external definition."
                    )
                    module_path = f"{stage_name}.{service_name}"
                    module = import_module(module_path)

                # Get service class from module
                service_cls = getattr(module, service_name)

                # Instantiate service
                logging.trace(
                    "initializing stage.service %s.%s with settings %s"
                    % (stage_name, service_name, settings)
                )
                try:
                    service = service_cls(**settings, profile=self._profile)
                except Exception:
                    logging.error(
                        "Failed to instantiate stage.service %s.%s with settings %s",
                        stage_name,
                        service_name,
                        settings.keys(),
                    )
                    raise

                if not isinstance(service, Stage):
                    raise TypeError(
                        'Trying to create service "%s" for stage #%d (%s),'
                        " but object %s instantiated from class %s is not a"
                        " PISA Stage type but instead is of type %s."
                        % (
                            service_name,
                            stage_num,
                            stage_name,
                            service,
                            service_cls,
                            type(service),
                        )
                    )

                stages.append(service)

            except:
                logging.error(
                    "Failed to initialize stage #%d (stage=%s, service=%s).",
                    stage_num,
                    stage_name,
                    service_name,
                )
                raise



        # set parameters with an identical name to the same object
        # otherwise we get inconsistent behaviour when setting repeated params
        # See Isues #566 and #648
        all_parans = self.params
        self.update_params(all_parans, existing_must_match=True, extend=False)

        param_selections = set()
        for service in stages:
            param_selections.update(service.param_selections)
        param_selections = sorted(param_selections)

        for stage in stages:
            stage.select_params(param_selections, error_on_missing=False)

        self._stages = stages

        self.setup()

    def get_outputs(self, **get_outputs_kwargs):
        """Wrapper around `_get_outputs`. The latter might
        have quite some overhead compared to `run` alone"""
        if self.profile:
            start_t = time()
            outputs = self._get_outputs(**get_outputs_kwargs)
            end_t = time()
            self._get_outputs_times.append(end_t - start_t)
        else:
            outputs = self._get_outputs(**get_outputs_kwargs)
        return outputs

    def _get_outputs_multdimbinning(self, output_binning, output_key):
        """Logic that produces a single `MapSet` when the pipeline's
        output binning is a regular `MultiDimBinning`.

        Returns
        -------
        outputs : MapSet

        """
        self.data.representation = output_binning
        if isinstance(output_key, tuple):
            assert len(output_key) == 2
            outputs = self.data.get_mapset(output_key[0], error=output_key[1])
        else:
            outputs = self.data.get_mapset(output_key)
        return outputs

    def _get_outputs_varbinning(self, output_binning, output_key):
        """Logic that produces multiple `MapSet`s when the pipeline's
        output binning is a `VarBinning`.

        Returns
        -------
        outputs : list of MapSet

        """
        assert self.data.representation == "events"
        outputs = []

        selections = output_binning.selections
        for i in range(output_binning.nselections):
            # there will be a new ContainerSet created for each selection
            containers = []
            for c in self.data.containers:
                cc = Container(name=c.name)
                # Find the events that belong to the given selection, depending on
                # type of selection.
                # TODO: consider optimisations such as caching these masks?
                if isinstance(selections, list):
                    keep = c.get_keep_mask(selections[i])
                else:
                    assert isinstance(selections, OneDimBinning)
                    cut_var = c[selections.name]
                    # cut on bin edges
                    keep = (cut_var >= selections.edge_magnitudes[i]) & (cut_var < selections.edge_magnitudes[i+1])
                for var_name in output_binning.binnings[i].names:
                    # Store the selected var_name entries (corresponding to the
                    # dimensions in which the data for this selection will be
                    # binned) in the fresh Container
                    cc[var_name] = c[var_name][keep]
                # store the quantities that will populate each bin
                if isinstance(output_key, tuple):
                    assert len(output_key) == 2
                    cc[output_key[0]] = c[output_key[0]][keep]
                    cc.tranlation_modes[output_key[0]] = 'sum'
                    cc[output_key[1]] = np.square(c[output_key[0]][keep])
                    cc.tranlation_modes[output_key[1]] = 'sum'
                else:
                    cc[output_key] = c[output_key][keep]
                    cc.tranlation_modes[output_key] = 'sum'

                containers.append(cc)

            dat = ContainerSet(
                name=self.data.name,
                containers=containers,
                representation=output_binning.binnings[i],
            )

            if isinstance(output_key, tuple):
                for c in dat.containers:
                    # uncertainties
                    c[output_key[1]] = np.sqrt(c[output_key[1]])
                outputs.append(dat.get_mapset(output_key[0], error=output_key[1]))
            else:
                outputs.append(dat.get_mapset(output_key))
        return outputs


    def _get_outputs(self, output_binning=None, output_key=None):
        """Get MapSet output"""

        self.run()

        if output_binning is None:
            output_binning = self.output_binning
        elif isinstance(output_binning, VarBinning):
            # Only have to check exclusivity in case external output binning
            # is requested
            self.assert_exclusive_varbinning(output_binning=output_binning)
        if isinstance(output_binning, VarBinning):
            # Any contained stages' apply_modes could have changed, whether
            # an external output binning is specified here or not
            self.assert_varbinning_compat()
        if output_key is None:
            output_key = self.output_key

        assert(isinstance(output_binning, (MultiDimBinning, VarBinning)))

        if isinstance(output_binning, MultiDimBinning):
            outputs = self._get_outputs_multdimbinning(output_binning, output_key)
        else:
            assert isinstance(output_binning, VarBinning)
            outputs = self._get_outputs_varbinning(output_binning, output_key)

        return outputs

    def add_covariance(self, covmat):
        """
            Incorporates covariance between parameters. 
            This is done by replacing relevant correlated parameters with "DerivedParams"
                that depend on new parameters in an uncorrelated basis

            The parameters are all updated, but this doesn't add the new parameters in
            So we go to the first stage we find that has one of the original parameters and manually add this in 
            
        """
        if self._covariance_set:
            logging.warn("Tried to add covariance matrix while one is already here.")
            logging.fatal("Add larger covariance matrix rather than calling this multiple times")

        paramset = self.params
        paramset.add_covariance(covmat)
        self._covariance_set = True

        # this should go and replace existing stage parameters with the new ones 
        self.update_params(paramset)
        self._add_rotated(paramset)

    def _add_rotated(self, paramset:ParamSet, suppress_warning=False):
        """
            Used to manually add in the new, rotated parameters
        """
        # now we need to add in the new, rotated, parameters 
        # we want to add the new rotated parameters into a stage that had the correlated parameter
        #   it doesn't really matter where these uncorrelated parameters go, all stages
        #   that need to are already using those Derived Params 
        derived_name = ""
        for param in paramset:
            if isinstance(param, DerivedParam): 
                derived_name = param.name
                depends = param.dependson
                break
        if len(depends.keys())==0:
            if not suppress_warning:
                logging.warn("Added covariance matrix but found no Derived Params")
            return False
        
        success = True
        # now we find where a derived parameter lives 
        for stage in self.stages:
            included = stage._param_selector.params.names
            if derived_name in included:
                success = True
                # TODO incorporate selector !! 
                stage._param_selector.update(paramset)

        return success

    def run(self):
        """Wrapper around `_run_function`"""
        if self.profile:
            start_t = time()
            self._run_function()
            end_t = time()
            self._run_times.append(end_t - start_t)
        else:
            self._run_function()

    def _run_function(self):
        """Run the pipeline to compute"""
        for stage in self.stages:
            logging.debug(f"Working on stage {stage.stage_name}.{stage.service_name}")
            stage.run()

    def setup(self):
        """Wrapper around `_setup_function`"""
        if self.profile:
            start_t = time()
            self._setup_function()
            end_t = time()
            self._setup_times.append(end_t - start_t)
        else:
            self._setup_function()

    def _setup_function(self):
        """Setup (reset) all stages"""
        self.data = ContainerSet(self.name)
        for stage in self.stages:
            stage.data = self.data
            stage.setup()

    def update_params(self, params, existing_must_match=False, extend=False):
        """Update params for the pipeline.

        Note that any param in `params` in excess of those that already exist
        in the pipeline's stages will have no effect.

        Parameters
        ----------
        params : ParamSet
            Parameters to be updated

        existing_must_match : bool
        extend : bool

        """
        for stage in self:
            stage._param_selector.update(params, existing_must_match=existing_must_match, extend=extend)
            #stage.params.update(params, existing_must_match=existing_must_match, extend=extend)

    def select_params(self, selections, error_on_missing=False):
        """Select a set of alternate param values/specifications.

        Parameters
        -----------
        selections : string or iterable of strings
        error_on_missing : bool

        Raises
        ------
        KeyError if `error_on_missing` is `True` and any of `selections` does
            not exist in any stage in the pipeline.

        """
        successes = 0
        for stage in self:
            try:
                stage.select_params(selections, error_on_missing=True)
            except KeyError:
                pass
            else:
                successes += 1

        if error_on_missing and successes == 0:
            raise KeyError(
                "None of the stages in this pipeline has all of the"
                " selections %s available." % (selections,)
            )

    @property
    def params(self):
        """pisa.core.param.ParamSet : pipeline's parameters"""
        params = ParamSet()
        for stage in self:
            params.extend(stage.params)
        return params

    @property
    def param_selections(self):
        """list of strings : param selections collected from all stages"""
        selections = set()
        for stage in self:
            selections.update(stage.param_selections)
        return sorted(selections)

    @property
    def stages(self)->'list[Stage]':
        """list of Stage : stages in the pipeline"""
        return [s for s in self]

    @property
    def stage_names(self):
        """list of strings : names of stages in the pipeline"""
        return [s.stage_name for s in self]

    @property
    def service_names(self):
        """list of strings : names of services in the pipeline"""
        return [s.service_name for s in self]

    @property
    def config(self):
        """Deepcopy of the OrderedDict used to instantiate the pipeline"""
        return deepcopy(self._config)

    @property
    def source_code_hash(self):
        """Hash for the source code of this object's class.

        Not meant to be perfect, but should suffice for tracking provenance of
        an object stored to disk that were produced by a Stage.

        """
        if self._source_code_hash is None:
            self._source_code_hash = hash_obj(getsource(self.__class__))
        return self._source_code_hash

    @property
    def hash(self):
        """int : Hash of the state of the pipeline. This hashes together a hash
        of the Pipeline class's source code and a hash of the state of each
        contained stage."""
        return hash_obj([self.source_code_hash] + [stage.hash for stage in self])

    def __hash__(self):
        return self.hash

    def assert_varbinning_compat(self):
        """Asserts that pipeline setup is compatible with `VarBinning`:
        all stages need to apply to events (this precludes use with
        any histogramming service, which requires a binning as apply_mode).

        Raises
        ------
        ValueError
            if at least one stage has apply_mode!='events'

        """
        incompat = []
        for s in self.stages:
            if not s.apply_mode == 'events':
                incompat.append(s)
        if len(incompat) >= 1:
            str_incompat = ", ".join(
                [f"{stage.stage_name}.{stage.service_name}" for stage in incompat]
            )
            raise ValueError(
                "When a variable binning is used, all stages need to set "
                f"apply_mode='events', but '{str_incompat}' of '{self.name}' "
                "do(es) not!"
            )

    def assert_exclusive_varbinning(self, output_binning=None):
        """Assert that `VarBinning` selections are mutually exclusive.
        This is done individually for each `Container` in `self.data`.

        Parameters
        -----------
        output_binning : None, MultiDimBinning, VarBinning

        Raises
        ------
        ValueError
            if a `VarBinning` is tested and at least two selections
            (if applicable) are not mutually exclusive

        """
        if output_binning is None:
            selections =  self.output_binning.selections
            nselections = self.output_binning.nselections
        else:
            selections = output_binning.selections
            nselections = output_binning.nselections
        if isinstance(selections, list):
            # list of selection-criteria strings
            # perform and report sanity checks on selected event counts
            # total count per selection across all containers
            tot_sel_counts = {sel: 0 for sel in selections}
            for c in self.data:
                keep = np.zeros(c.size)
                # Looping over all selections for a fixed container is
                # sufficient to detect overlaps
                for sel in selections:
                    keep_mask = c.get_keep_mask(sel)
                    keep += keep_mask
                    # number of events selected from this container
                    sel_count = np.sum(keep_mask)
                    logging.debug(f"'{c.name}' selected by '{sel}': {sel_count}")
                    tot_sel_counts[sel] += sel_count
                if not np.all(keep <= 1):
                    raise ValueError(
                        f"Selections {selections} are not mutually exclusive for "
                        f"'{c.name}' (at least) in pipeline '{self.name}'!"
                    )
            # Warn on empty selections (don't assume that this must be an error)
            empty_sels = [sel for sel in selections if tot_sel_counts[sel] == 0]
            if empty_sels:
                empty_sels_str = ", ".join(empty_sels)
                logging.warning(
                    f"There are empty selections in pipeline '{self.name}': "
                    f"'{empty_sels_str}'"
                )

    @property
    def output_binning(self):
        return self._output_binning

    @output_binning.setter
    def output_binning(self, binning):
        if isinstance(binning, VarBinning):
            self.assert_varbinning_compat()
            self.assert_exclusive_varbinning(output_binning=binning)
        self._output_binning = binning


def test_Pipeline():
    """Unit tests for Pipeline class"""
    # TODO: make a test config file with hierarchy AND material selector,
    # uncomment / add in tests commented / removed below

    #
    # Test: select_params and param_selections
    #

    hierarchies = ["nh", "ih"]
    #materials = ["iron", "pyrolite"]
    materials = []

    t23 = dict(ih=49.5 * ureg.deg, nh=42.3 * ureg.deg)
    #YeO = dict(iron=0.4656, pyrolite=0.4957)

    # Instantiate with two pipelines: first has both nh/ih and iron/pyrolite
    # param selectors, while the second only has nh/ih param selectors.
    pipeline = Pipeline("settings/pipeline/example.cfg")  # pylint: disable=redefined-outer-name

    #current_mat = "iron"
    current_hier = "nh"

    for new_hier, new_mat in product(hierarchies, materials):
        #_ = YeO[new_mat]

        assert pipeline.param_selections == sorted([current_hier]), str(
            pipeline.param_selections
        )
        assert pipeline.params.theta23.value == t23[current_hier], str(
            pipeline.params.theta23
        )
        #assert pipeline.params.YeO.value == YeO[current_mat], str(pipeline.params.YeO)

        # Select just the hierarchy
        pipeline.select_params(new_hier)
        assert pipeline.param_selections == sorted([new_hier]), str(
            pipeline.param_selections
        )
        assert pipeline.params.theta23.value == t23[new_hier], str(
            pipeline.params.theta23
        )
        #assert pipeline.params.YeO.value == YeO[current_mat], str(pipeline.params.YeO)

        ## Select just the material
        #pipeline.select_params(new_mat)
        #assert pipeline.param_selections == sorted([new_hier, new_mat]), str(
        #    pipeline.param_selections
        #)
        assert pipeline.params.theta23.value == t23[new_hier], str(
            pipeline.params.theta23
        )
        #assert pipeline.params.YeO.value == YeO[new_mat], str(pipeline.params.YeO)

        # Reset both to "current"
        pipeline.select_params([current_hier])
        assert pipeline.param_selections == sorted([current_hier]), str(
            pipeline.param_selections
        )
        assert pipeline.params.theta23.value == t23[current_hier], str(
            pipeline.params.theta23
        )
        #assert pipeline.params.YeO.value == YeO[current_mat], str(pipeline.params.YeO)

        ## Select both hierarchy and material
        #pipeline.select_params([new_hier])
        #assert pipeline.param_selections == sorted([new_hier, new_mat]), str(
        #    pipeline.param_selections
        #)
        #assert pipeline.params.theta23.value == t23[new_hier], str(
        #    pipeline.params.theta23
        #)
        #assert pipeline.params.YeO.value == YeO[new_mat], str(pipeline.params.YeO)

        #current_hier = new_hier
        #current_mat = new_mat

    #
    # Test: a pipeline using a VarBinning
    #
    p = Pipeline("settings/pipeline/varbin_example.cfg")
    out = p.get_outputs()
    # a split into two event selections has to result in two MapSets
    assert len(out) == 2
    # a binned apply_mode has to result in a ValueError
    # first get a pre-existing binning
    binned_calc_mode = p.stages[2].calc_mode
    assert isinstance(binned_calc_mode, MultiDimBinning)
    p.stages[2].apply_mode = binned_calc_mode
    try:
        out = p.get_outputs()
    except ValueError:
        pass
    else:
        assert False

    # also verify that pipeline correctly detects non-exclusive selections
    p.stages[2].apply_mode = "events"
    vb = p.output_binning
    # define a selection string which will simply be repeated
    assert vb.nselections > 1
    sel = ["pid > 0"] * vb.nselections
    invalid_vb = VarBinning(binnings=vb.binnings, selections=sel)
    try:
        p.output_binning = invalid_vb
    except ValueError:
        pass
    else:
        assert False

    # pipeline should accept any empty selections
    sel[-1] = "pid > np.inf"
    invalid_vb = VarBinning(binnings=vb.binnings, selections=sel)
    p.output_binning = invalid_vb

# ----- Most of this below cang go (?) ---

def parse_args():
    """Parse command line arguments if `pipeline.py` is called as a script."""
    parser = ArgumentParser(
        # formatter_class=ArgumentDefaultsHelpFormatter,
        description="""Instantiate and run a pipeline from a config file.
        Optionally store the resulting distribution(s) and plot(s) to disk."""
    )

    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "-p",
        "--pipeline",
        metavar="CONFIGFILE",
        type=str,
        required=True,
        help="File containing settings for the pipeline.",
    )

    parser.add_argument(
        "-a",
        "--arg",
        metavar="SECTION ARG=VAL",
        nargs="+",
        action="append",
        help="""Set config arg(s) manually. SECTION can be e.g.
        "stage:<stage_name>" (like "stage:flux", "stage:reco", etc.),
        "pipeline", and so forth. Arg values specified here take precedence
        over those in the config file, but note that the sections specified
        must already exist in the config file.""",
    )
    parser.add_argument(
        "--select",
        metavar="PARAM_SELECTIONS",
        nargs="+",
        default=None,
        help="""Param selectors (separated by spaces) to use to override any
        defaults in the config file.""",
    )
    parser.add_argument(
        "--inputs",
        metavar="FILE",
        type=str,
        help="""File from which to read inputs to be fed to the pipeline.""",
    )
    parser.add_argument(
        "--only-stage",
        metavar="STAGE",
        type=str,
        help="""Test stage: Instantiate a single stage in the pipeline
        specification and run it in isolation (as the sole stage in a
        pipeline). If it is a stage that requires inputs, these can be
        specified with the --infile argument, or else dummy stage input maps
        (numpy.ones(...), matching the input binning specification) are
        generated for testing purposes.""",
    )
    parser.add_argument(
        "--stop-after-stage",
        metavar="STAGE",
        help="""Instantiate a pipeline up to and including STAGE, but stop
        there. Can specify a stage by index in the pipeline config (e.g., 0, 1,
        etc.) or name (e.g., flux, osc, etc.)""",
    )
    parser.add_argument(
        "--outdir",
        metavar="DIR",
        type=str,
        help="""Store all output files (data and plots) to this directory.
        Directory will be created (including missing parent directories) if it
        does not exist already. If no dir is provided, no outputs will be
        saved.""",
    )
    parser.add_argument(
        "--intermediate",
        action="store_true",
        help="""Store all intermediate outputs, not just the final stage's
        outputs.""",
    )
    parser.add_argument("--pdf", action="store_true", help="""Produce pdf plot(s).""")
    parser.add_argument("--png", action="store_true", help="""Produce png plot(s).""")
    parser.add_argument(
        "--annotate", action="store_true", help="""Annotate plots with counts per bin"""
    )
    parser.add_argument(
        "-v",
        action="count",
        default=None,
        help="""Set verbosity level. Repeat for increased verbosity. -v is
        info-level, -vv is debug-level and -vvv is trace-level output.""",
    )
    args = parser.parse_args()
    return args


def main(return_outputs=False):
    """Main; call as script with `return_outputs=False` or interactively with
    `return_outputs=True`

    FIXME: This is broken in various ways (easiest fix:
    pipeline.get_outputs() has no idx parameter anymore)
    """
    from pisa.utils.plotter import Plotter

    args = parse_args()
    set_verbosity(args.v)

    # Even if user specifies an integer on command line, it comes in as a
    # string. Try to convert to int (e.g. if `'1'` is passed to indicate the
    # second stage), and -- if successful -- use this as `args.only_stage`.
    # Otherwise, the string value passed will be used (e.g. `'osc'` could be
    # passed).
    try:
        only_stage_int = int(args.only_stage)
    except (ValueError, TypeError):
        pass
    else:
        args.only_stage = only_stage_int

    if args.outdir:
        mkdir(args.outdir)
    else:
        if args.pdf or args.png:
            raise ValueError("No --outdir provided, so cannot save images.")

    # Most basic parsing of the pipeline config (parsing only to this level
    # allows for simple strings to be specified as args for updating)
    bcp = PISAConfigParser()
    bcp.read(args.pipeline)

    # Update the config with any args specified on command line
    if args.arg is not None:
        for arg_list in args.arg:
            if len(arg_list) < 2:
                raise ValueError(
                    'Args must be formatted as: "section arg=val". Got "%s"'
                    " instead." % " ".join(arg_list)
                )
            section = arg_list[0]
            remainder = " ".join(arg_list[1:])
            eq_split = remainder.split("=")
            newarg = eq_split[0].strip()
            value = ("=".join(eq_split[1:])).strip()
            logging.debug(
                'Setting config section "%s" arg "%s" = "%s"', section, newarg, value
            )
            try:
                bcp.set(section, newarg, value)
            except NoSectionError:
                logging.error(
                    'Invalid section "%s" specified. Must be one of %s',
                    section,
                    bcp.sections(),
                )
                raise

    # Instantiate the pipeline
    pipeline = Pipeline(bcp)  # pylint: disable=redefined-outer-name

    if args.select is not None:
        pipeline.select_params(args.select, error_on_missing=True)

    if args.only_stage is None:
        stop_idx = args.stop_after_stage
        try:
            stop_idx = int(stop_idx)
        except (TypeError, ValueError):
            pass
        if isinstance(stop_idx, str):
            stop_idx = pipeline.index(stop_idx)
        outputs = pipeline.get_outputs( # pylint: disable=redefined-outer-name
            idx=stop_idx
        )
        if stop_idx is not None:
            stop_idx += 1
        indices = slice(0, stop_idx)
    else:
        assert args.stop_after_stage is None
        idx = pipeline.index(args.only_stage)
        stage = pipeline[idx]
        indices = slice(idx, idx + 1)

        # Create dummy inputs if necessary
        inputs = None
        if hasattr(stage, "input_binning"):
            logging.warning(
                "Stage requires input, so building dummy"
                " inputs of random numbers, with random state set to the input"
                " index according to alphabetical ordering of input names and"
                " filled in alphabetical ordering of dimension names."
            )
            input_maps = []
            tmp = deepcopy(stage.input_binning)
            alphabetical_binning = tmp.reorder_dimensions(sorted(tmp.names))
            for input_num, input_name in enumerate(sorted(stage.input_names)):
                # Create a new map with all 3's; name according to the input
                hist = np.full(shape=alphabetical_binning.shape, fill_value=3.0)
                input_map = Map(
                    name=input_name, binning=alphabetical_binning, hist=hist
                )

                # Apply Poisson fluctuations to randomize the values in the map
                input_map.fluctuate(method="poisson", random_state=input_num)

                # Reorder dimensions according to user's original binning spec
                input_map.reorder_dimensions(stage.input_binning)
                input_maps.append(input_map)
            inputs = MapSet(maps=input_maps, name="ones", hash=1)

        outputs = stage.run(inputs=inputs)

    for stage in pipeline[indices]:
        if not args.outdir:
            break
        stg_svc = stage.stage_name + "__" + stage.service_name
        fbase = os.path.join(args.outdir, stg_svc)
        if args.intermediate or stage == pipeline[indices][-1]:
            stage.outputs.to_json(fbase + "__output.json.bz2")

        # also only plot if args intermediate or last stage
        if args.intermediate or stage == pipeline[indices][-1]:
            formats = OrderedDict(png=args.png, pdf=args.pdf)
            if isinstance(stage.outputs, Data):
                # TODO(shivesh): plots made here will use the most recent
                # "pisa_weight" column and so all stages will have identical plots
                # (one workaround is to turn on "memcache_deepcopy")
                # TODO(shivesh): intermediate stages have no output binning
                if stage.output_binning is None:
                    logging.debug("Skipping plot of intermediate stage %s", stage)
                    continue
                outputs = stage.outputs.histogram_set(
                    binning=stage.output_binning,
                    nu_weights_col="pisa_weight",
                    mu_weights_col="pisa_weight",
                    noise_weights_col="pisa_weight",
                    mapset_name=stg_svc,
                    errors=True,
                )

            try:
                for fmt, enabled in formats.items():
                    if not enabled:
                        continue
                    my_plotter = Plotter(
                        stamp="Event rate",
                        outdir=args.outdir,
                        fmt=fmt,
                        log=False,
                        annotate=args.annotate,
                    )
                    my_plotter.ratio = True
                    my_plotter.plot_2d_array(
                        outputs, fname=stg_svc + "__output", cmap="RdBu"
                    )
            except ValueError as exc:
                logging.error(
                    "Failed to save plot to format %s. See exception" " message below",
                    fmt,
                )
                traceback.format_exc()
                logging.exception(exc)
                logging.warning("I can't go on, I'll go on.")

    if return_outputs:
        return pipeline, outputs


if __name__ == "__main__":
    pipeline, outp = main(return_outputs=True)
