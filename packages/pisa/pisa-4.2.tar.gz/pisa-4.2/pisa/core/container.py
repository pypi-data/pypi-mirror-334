"""
Class to hold generic data in container.
he data can be unbinned or binned or scalar, while
translation methods between such different representations
are provided.
"""

from __future__ import absolute_import, print_function

from collections.abc import Sequence
from collections import defaultdict

import numpy as np
import re

from pisa import FTYPE
from pisa.core.binning import OneDimBinning, MultiDimBinning
from pisa.core.map import Map, MapSet
from pisa.core.translation import histogram, lookup, resample
from pisa.utils.comparisons import ALLCLOSE_KW
from pisa.utils.log import logging


class ContainerSet():
    """
    Class to hold a set of container objects

    Parameters
    ----------
    name : str

    containers : list or None

    representation : MultiDimBinning, "events" or None

    """
    def __init__(self, name, containers=None, representation=None):
        self.name = name
        self.linked_containers = []
        self.containers = []
        if containers is None:
            containers = []
        for container in containers:
            self.add_container(container)
        self.representation = representation

    def __repr__(self):
        return f'ContainerSet containing {[c.name for c in self]}'

    @property
    def is_map(self):
        '''Is current representation a map/grid'''
        if len(self.containers):
            return self.containers[0].is_map

    def add_container(self, container):
        '''Append a container whose name mustn't exist yet'''
        if container.name in self.names:
            raise ValueError('container with name %s already exists'%container.name)
        self.containers.append(container)

    @property
    def representation(self):
        return self._representation

    @representation.setter
    def representation(self, representation):
        """
        Parameters
        ----------
        representation : str, MultiDimBinning or any hashable object
            Data specs should be set to retreive the right representation
            i.e. the representation one is working in at the moment

            This property is meant to be changed while working with a ContainerSet
        """
        self._representation = representation
        for container in self:
            container.representation = representation

    @property
    def names(self):
        return [c.name for c in self.containers]

    def get_shared_keys(self, rep_indep=True):
        """
        Get a tuple of all keys shared among contained containers.

        Parameters
        ----------
        rep_indep : bool
            Whether all keys should be considered, not just those in
            the current representation (default: `True`)

        """
        if len(self.containers) == 0:
            return ()

        return tuple(
            set.intersection(*[
                set(c.all_keys_incl_aux_data if rep_indep else c.keys_incl_aux_data)
                for c in self.containers
            ])
        )

    def link_containers(self, key, names):
        """Link containers together. When containers are linked, they are
        treated as a single (virtual) container for binned data

        Parameters
        ----------
        key : str
            name of linked object

        names : list
            name of containers to be linked under the given key

        """
        # intersection of names for linking and available names

        link_names = set(names) & set(self.names)
        if len(link_names) < len(names):
            logging.warning(
                "Skipping containers %s in linking, as those are not present"
                % (set(names) - set(self.names))
            )
        containers = [self.__getitem__(name) for name in link_names]
        logging.trace('Linking containers %s into %s'%(link_names, key))
        new_container = VirtualContainer(key, containers)
        self.linked_containers.append(new_container)


    def unlink_containers(self):
        """Unlink all container"""
        logging.trace('Unlinking all containers')
        for c in self.linked_containers:
            c.unlink()
        self.linked_containers = []

    def __getitem__(self, key):
        if key in self.names:
            return self.containers[self.names.index(key)]
        if len(self.linked_containers) > 0:
            linked_names = [c.name for c in self.linked_containers]
            if key in linked_names:
                return self.linked_containers[linked_names.index(key)]
        raise KeyError(f"No name `{key}` in container")

    def __iter__(self):
        """Iterate over individual non-linked containers and virtual containers
        for the ones that are linked together
        """
        containers_to_be_iterated = [c for c in self.containers if not c.linked] + self.linked_containers
        return iter(containers_to_be_iterated)

    def get_mapset(self, key, error=None):
        """For a given key, get a MapSet

        Parameters
        ----------
        key : str

        error : None or str
            specify a key that errors are read from

        Returns
        -------
        map_set : MapSet

        """
        maps = []
        for container in self:
            maps.append(container.get_map(key, error=error))
        return MapSet(name=self.name, maps=maps)


class VirtualContainer():
    """
    Class providing a virtual container for linked individual containers

    It should just behave like a normal container

    For reading, it just uses one container as a representative
    (no checking at the moment if the others actually contain the same data)

    For writing, it creates one object that is added to all containers

    Parameters
    ----------
    name : str

    containers : list

    """

    def __init__(self, name, containers):
        self.name = name
        # check and set link flag
        for container in containers:
            if container.linked:
                raise ValueError(
                    'Cannot link container %s since it is already linked'
                    % container.name
                )
            container.linked = True
        self.containers = containers

    def __repr__(self):
        return f'VirtualContainer containing {[c.name for c in self]}'

    def unlink(self):
        '''Reset link flag and copy all accessed keys'''
        # reset flag
        for container in self:
            container.linked = False

    def __iter__(self):
        return iter(self.containers)

    def __getitem__(self, key):
        # should we check they're all the same?
        return self.containers[0][key]

    def __setitem__(self, key, value):
        for container in self:
            container[key] = value

    def set_aux_data(self, key, val):
        '''See `Container.set_aux_data`'''
        for container in self:
            container.set_aux_data(key, val)

    def mark_changed(self, key):
        '''Copy data under this key from representative container into
        all others and then mark all as changed (see `Container.mark_changed`)'''
        for container in self.containers[1:]:
            container[key] = np.copy(self.containers[0][key])
        for container in self:
            container.mark_changed(key)

    def mark_valid(self, key):
        '''See `Container.mark_valid`'''
        for container in self:
            container.mark_valid(key)

    @property
    def representation(self):
        return self.containers[0].representation

    @representation.setter
    def representation(self, representation):
        for container in self:
            container.representation = representation

    @property
    def shape(self):
        return self.containers[0].shape

    @property
    def size(self):
        return np.product(self.shape)


class Container():
    """
    Container to hold data in multiple representations

    Parameters:
    -----------

    name : str
        name of container

    representation : hashable object, e.g. str or MultiDimBinning
        Representation in which to initialize the container

    """

    default_translation_mode = "average"
    translation_modes = ("average", "sum")
    array_representations = ("events", "log_events")


    def __init__(self, name, representation='events'):
        self.name = name
        self._representation = None

        self.linked = False

        # ToDo: simple auxiliary data like scalars
        # dict of form [variable]
        self._aux_data = {}

        # validity bit
        # dict of form [variable][representation_hash]
        self.validity = defaultdict(dict)

        # translation mode
        # dict of form [variable]
        self.tranlation_modes = {}

        # Actual data
        # dict of form [representation_hash][variable]
        self.data = defaultdict(dict)

        # Representation objects
        # dict of form [representation_hash]
        self._representations = {}

        # Precedence of representation (lower number = higher precedence)
        # dict of form [representation_hash]
        self.precedence = defaultdict(int)

        self.representation = representation

    def __repr__(self):
        return f'Container containing keys {self.all_keys}'
    
    @property
    def representation(self):
        return self._representation

    
    def set_aux_data(self, key, val):
        '''Add any auxiliary data, which will not be translated or
        tied to a specific representation'''
        if key in self.all_keys:
            raise KeyError(f'Key {key} already exsits')

        self._aux_data[key] = val
    
    @representation.setter
    def representation(self, representation):
        key = hash(representation)
        if not key in self.representation_keys:
            self._representations[key] = representation
            if isinstance(representation, MultiDimBinning):
                for name in representation.names:
                    self.validity[name][key] = True
            elif isinstance(representation, str):
                if representation not in self.array_representations:
                    raise ValueError(f"Unknown representation '{representation}'")
            
        self._representation = representation
        self.current_data = self.data[key]
        
    @property
    def shape(self):
        if self.is_map:
            return self.representation.shape
        if len(self.keys) == 0:
            return None
        key = self.keys[0]
        return self[key].shape[0:1]    

    @property
    def size(self):
        return np.product(self.shape)
    
    @property
    def num_dims(self):
        if self.is_map:
            return self.representation.num_dims
        return 1
    
    @property
    def representations(self):
        return tuple(self._representations.values())
    
    @property
    def representation_keys(self):
        return tuple(self._representations.keys())
    
    @property
    def keys(self):
        keys = tuple(self.current_data.keys())
        if self.is_map:
            keys += tuple(self.representation.names)
        return keys

    @property
    def keys_incl_aux_data(self):
        '''same as keys, but including auxiliary data'''
        return list(self.keys) + list(self._aux_data.keys())
    
    @property
    def all_keys(self):
        '''return all available keys, regardless of representation'''
        return list(self.validity.keys())

    @property
    def all_keys_incl_aux_data(self):
        '''same as `all_keys`, but including auxiliary data'''
        return self.all_keys + list(self._aux_data.keys())
        
    @property
    def is_map(self):
        '''Is current representation a map/grid'''
        return isinstance(self.representation, MultiDimBinning)
        
    def mark_changed(self, key):
        '''mark a key as changed and only what is in the current representation is valid'''
        # invalidate all
        for rep in self.validity[key]:
            self.validity[key][rep] = False
            
        if key in self.current_data.keys():
            self.mark_valid(key)

    def mark_valid(self, key):
        '''validate data as is in current representation, regardless'''
        self.validity[key][hash(self.representation)] = True
        
    def __getitem__(self, key):
        data = self.__get_data(key)        
        return data
    
    def __setitem__(self, key, data):
        
        if self.is_map:
            if key in self.representation.names:
                raise Exception(f'Cannot add variable {key}, as it is a binning dimension')
        
        self.__add_data(key, data)                
        if not key in self.tranlation_modes.keys():
            self.tranlation_modes[key] = self.default_translation_mode
        
        self.mark_changed(key)
       
    def __add_data(self, key, data):
        """
        Parameters
        ----------
        key : string
            identifier
        data : ndarray, PISA Map or (array, binning)-tuple
        is_flat : bool
            is the data already flattened (i.e. the binning dimensions unrolled)
        """
        if isinstance(data, np.ndarray):
            
            if self.is_map:
                self.__add_data(key, (self.representation, data))
            
            else:            
                shape = self.shape
                if shape is not None:
                    assert data.shape[:self.num_dims] == shape, 'Incompatible dimensions'

                self.current_data[key] = data

        elif isinstance(data, Map):
            assert hash(self.representation) == hash(data.binning)
            flat_array = data.hist.ravel()
            self.current_data[key] = flat_array

        elif isinstance(data, Sequence) and len(data) == 2:
            binning, array = data
            assert isinstance(binning, MultiDimBinning)
            
            assert hash(self.representation) == hash(binning)
                            
            is_flat = array.shape[0] == binning.size
            
            if is_flat:
                flat_array = array
            else:
                # first dimesnions must match
                assert array.shape[:binning.num_dims] == binning.shape
                
                
                if array.ndim > binning.num_dims:
                    flat_shape = (binning.size, -1)
                else:
                    flat_shape = (binning.size, )
                flat_array = array.reshape(flat_shape)
            self.current_data[key] = flat_array
        else:
            raise TypeError('unknown dataformat')
            
            
    def __get_data(self, key):
        if self.is_map:
            binning = self.representation
            # check if key is binning dimension
            if key in binning.names:
                return self.unroll_binning(key, binning)
        # check validity
        if not key in self.keys:
            if key in self.all_keys:
                self.auto_translate(key)
                #raise KeyError(f'Data {key} not present in chosen representation')
            else:
                if key in self._aux_data.keys():
                    return self._aux_data[key]
                raise KeyError(f'Data {key} not present in Container')
        
        valid = self.validity[key][hash(self.representation)]
        if not valid:
            self.auto_translate(key)
            #raise ValueError('Invalid data as it was changed in a different representation!')
        

        return self.current_data[key]
    
    @staticmethod
    def unroll_binning(key, binning):
        '''Get an Array containing the unrolled binning'''
        grid = binning.meshgrid(entity='weighted_centers', attach_units=False)
        return grid[binning.index(key)].ravel()

    
    def get_hist(self, key):
        """Return reshaped data as normal n-dimensional histogram"""
        assert self.is_map, 'Cannot retrieve hists from non-map data'
        
        # retrieve in case needs translation
        self[key]

        binning = self.representation
        data = self[key]
        if data.ndim > binning.num_dims:
            full_shape = list(binning.shape) + [-1] 
        else:
            full_shape = list(binning.shape)
            
        return data.reshape(full_shape), binning

    def get_map(self, key, error=None):
        """Return binned data in the form of a PISA map"""
        hist, binning = self.get_hist(key)
        if error is not None:
            error_hist = np.abs(self.get_hist(error)[0])
        else:
            error_hist = None
        assert hist.ndim == binning.num_dims
        return Map(name=self.name, hist=hist, error_hist=error_hist, binning=binning)
    
    def __iter__(self):
        """iterate over all keys in container"""
        return self.keys
    
    def translate(self, key, src_representation):
        '''translate variable from source representation
        
        key : str
        src_representation : representation present in container
        
        '''
        
        assert hash(src_representation) in self.representation_keys
        
        dest_representation = self.representation

        if hash(src_representation) == hash(dest_representation):
            # nothing to do
            return    
    
        from_map = isinstance(src_representation, MultiDimBinning)
        to_map = isinstance(dest_representation, MultiDimBinning)
    
        if self.tranlation_modes[key] == 'average':            
            if from_map and to_map:
                out = self.resample(key, src_representation, dest_representation)
                self.representation = dest_representation
                self[key] = out
                
            elif to_map:
                out = self.array_to_binned(key, src_representation, dest_representation)
                self.representation = dest_representation
                self[key] = out
                
            elif from_map:
                out = self.binned_to_array(key, src_representation, dest_representation)
                self.representation = dest_representation
                self[key] = out   
                
            elif src_representation == "events" and dest_representation == "log_events":
                self.representation = "events"
                logging.trace(f"Container `{self.name}`: taking log of {key}")
                sample = np.log(self[key])
                self.representation = dest_representation
                self[key] = sample
            
            elif src_representation == "log_events" and dest_representation == "events":
                self.representation = "log_events"
                sample = np.exp(self[key])
                self.representation = dest_representation
                self[key] = sample

            else:
                raise NotImplementedError(f"translating {src_representation} to {dest_representation}")
                
        elif self.tranlation_modes[key] == 'sum':
            if from_map and to_map:
                raise NotImplementedError("Map to Map in sum mode needs to integrate over bins.")

            elif to_map:
                out = self.array_to_binned(key, src_representation, dest_representation, averaged=False)
                self.representation = dest_representation
                self[key] = out

            else:
                raise NotImplementedError()

        else:
            raise NotImplementedError()
            
        # validate source!
        self.validity[key][hash(src_representation)] = True

        
    def auto_translate(self, key):
        src_representation = self.find_valid_representation(key)
        if src_representation is None:
            raise Exception(f'No valid representation for {key} in container')
        # logging.debug(f'Auto-translating variable `{key}` from {src_representation}')
        self.translate(key, src_representation)
        
                
    def find_valid_representation(self, key):
        ''' Find valid, and best representation for key'''
        validity = self.validity[key]

        precedence = np.inf
        representation = None

        for h in validity.keys():
            if validity[h]:
                if self.precedence[h] < precedence:
                    precedence = self.precedence[h]
                    representation = self._representations[h]

        return representation
        
    def resample(self, key, src_representation, dest_representation):
        """Resample a binned key into a different binning
        Parameters
        ----------
        key : str
        src_representation : MultiDimBinning
        dest_representation : MultiDimBinning
        """
        
        logging.debug('Resampling %s'%(key))

        self.representation = src_representation
        sample = [self[name] for name in src_representation.names]
        weights = self[key]

        self.representation = dest_representation
        new_sample = [self[name] for name in dest_representation.names]
        new_hist = resample(weights, sample, src_representation, new_sample, dest_representation)                
        return new_hist      
        
    def array_to_binned(self, key, src_representation, dest_representation, averaged=True):
        """Histogram data array into binned data
        Parameters
        ----------
        key : str
        src_representation : str
        dest_representation : MultiDimBinning
        #averaged : bool
        #    if True, the histogram entries are averages of the numbers that
        #    end up in a given bin. This for example must be used when oscillation
        #    probabilities are translated.....otherwise we end up with probability*count
        #    per bin
        Notes
        -----
        right now, CPU-only
        """
        # TODO: make work for n-dim
        logging.trace('Transforming %s array to binned data'%(key))
        
        assert src_representation in self.array_representations
        assert isinstance(dest_representation, MultiDimBinning)
        
        if not dest_representation.is_irregular:
            sample = []
            dimensions = []
            for d in dest_representation:
                if d.is_log:
                    self.representation = "log_events"
                    sample.append(self[d.name])
                    dimensions.append(OneDimBinning(
                        d.name,
                        domain=np.log(d.domain.m),
                        num_bins=d.num_bins
                    ))
                else:
                    self.representation = "events"
                    sample.append(self[d.name])
                    dimensions.append(d)
            hist_binning = MultiDimBinning(dimensions)
        else:
            self.representation = src_representation
            sample = [self[name] for name in dest_representation.names]
            hist_binning = dest_representation

        self.representation = src_representation
        weights = self[key]
        self.representation = dest_representation
        hist = histogram(sample, weights, hist_binning, averaged=averaged)
        return hist

    def binned_to_array(self, key, src_representation, dest_representation):
        """Augmented binned data to array data"""

        logging.trace('Transforming %s binned to array data'%(key))
        
        self.representation = src_representation
        weights = self[key]
        
        if not src_representation.is_irregular:
            logging.trace(f"Container `{self.name}`: regularized lookup for {key}")
            sample = []
            dimensions = []
            for d in src_representation:
                if d.is_log:
                    self.representation = "log_events"
                    sample.append(self[d.name])
                    dimensions.append(OneDimBinning(
                        d.name,
                        domain=np.log(d.domain.m),
                        num_bins=d.num_bins
                    ))
                else:
                    self.representation = "events"
                    sample.append(self[d.name])
                    dimensions.append(d)
            hist_binning = MultiDimBinning(dimensions)
        else:
            logging.trace(f"Container `{self.name}`: irregular lookup for {key}")
            self.representation = dest_representation
            sample = [self[name] for name in src_representation.names]
            hist_binning = src_representation
   
        return lookup(sample, weights, hist_binning)

    def get_keep_mask(self, keep_criteria):
        """Returns a mask that only keeps the events that survive the given cut(s).

        Parameters
        ----------
        keep_criteria : str
            Any string interpretable as numpy boolean expression.

        Examples
        --------
        Keep events with true energies in [1, 80] GeV (note that units are not
        recognized, so have to be handled outside this method)

        >>> mask = container.get_keep_mask("(true_energy >= 1) & (true_energy <= 80)")

        """
        assert isinstance(keep_criteria, str)

        for var in self.keys:
            # using word boundary \b to replace whole words only
            keep_criteria = re.sub(
                r'\b{}\b'.format(var),
                'self["%s"]'%(var),
                keep_criteria
            )
        return eval(keep_criteria)  # pylint: disable=eval-used



def test_container():
    """Unit tests for Container class."""

    # NOTE: Right now the numbers are tuned so that the weights are identical
    # per bin. If you change binning that's likely not the case anymore and you
    # inevitably end up with averaged values over bins, which are then not
    # equal to the individual weights anymore when those are not identical per
    # bin

    n_evts = 10000
    x = np.linspace(0, 100, n_evts, dtype=FTYPE)
    y = np.linspace(0, 100, n_evts, dtype=FTYPE)
    w = np.tile(np.arange(100, dtype=FTYPE) + 0.5, (100, 1)).T.ravel()

    container = Container('test', 'events')
    container['x'] = x
    container['y'] = y
    container['w'] = w

    binning_x = OneDimBinning(name='x', num_bins=100, is_lin=True, domain=[0, 100])
    binning_y = OneDimBinning(name='y', num_bins=100, is_lin=True, domain=[0, 100])
    binning = MultiDimBinning([binning_x, binning_y])

    logging.trace('Testing container and translation methods')

    container.representation = binning
    bx = container['x']
    m = np.meshgrid(binning.midpoints[0].m, binning.midpoints[1].m)[1].ravel()
    assert np.allclose(bx, m, **ALLCLOSE_KW), f'test:\n{bx}\n!= ref:\n{m}'

    # array repr
    container.representation = 'events'
    array_weights = container['w']
    assert np.allclose(array_weights, w, **ALLCLOSE_KW), f'test:\n{array_weights}\n!= ref:\n{w}'

    # binned repr
    container.representation = binning
    diag = np.diag(np.arange(100) + 0.5)
    bd = container['w']
    h = container.get_hist('w')

    assert np.allclose(bd, diag.ravel(), **ALLCLOSE_KW), f'test:\n{bd}\n!= ref:\n{diag.ravel()}'
    assert np.allclose(h[0], diag, **ALLCLOSE_KW), f'test:\n{h[0]}\n!= ref:\n{diag}'
    assert h[1] == binning, f'test:\n{h[1]}\n!= ref:\n{binning}'

    # augment to array repr again
    container.representation = 'events'
    a = container['w']

    assert np.allclose(a, w, **ALLCLOSE_KW), f'test:\n{a}\n!= ref:\n{w}'


def test_container_set():
    container1 = Container('test1')
    container2 = Container('test2')

    data = ContainerSet('data', [container1, container2])

    try:
        data.add_container(container1)
    except ValueError:
        pass
    else:
        raise Exception('identical containers added to a containerset, this should not be possible')

    nevts1 = 10
    container1['true_energy'] = np.linspace(1, 80, nevts1, dtype=FTYPE)
    container2['reco_coszen'] = np.linspace(-1, 1, 2*nevts1, dtype=FTYPE)

    # we have not set a representation, should make no difference
    # whether we require repr. independence or not
    for rep_indep in (True, False):
        assert len(data.get_shared_keys(rep_indep=rep_indep)) == 0

    container1['reco_coszen'] = container2['reco_coszen'][:nevts1]
    # do the following without and with events rep. for fun
    for rep in (None, 'events'):
        data.representation = rep
        for rep_indep in (True, False):
            shared_keys = data.get_shared_keys(rep_indep=rep_indep)
            if rep_indep or rep is None:
                assert len(shared_keys) == 1
                assert shared_keys[0] == 'reco_coszen'
            else:
                # Here, we have set events rep., which
                # I believe should have no keys, and don't request
                # rep. independence -> 0
                for c in data.containers:
                    assert len(c.keys) == 0
                assert len(shared_keys) == 0

    # still in events rep.
    shared_aux_key = 'AmIEvil'
    # add auxiliary data to both containers
    container1.set_aux_data(key=shared_aux_key, val=False)
    container2.set_aux_data(key=shared_aux_key, val=True)
    # get shared keys across all reps. and for the current one
    shared_keys_rep_indep = data.get_shared_keys(rep_indep=True)
    shared_keys_rep_dep = data.get_shared_keys(rep_indep=False)

    assert (shared_aux_key in shared_keys_rep_indep
            and shared_aux_key in shared_keys_rep_dep)

    # But should have "reco_coszen" next to shared_aux_key
    # in shared keys for representation-dependent request
    assert len(shared_keys_rep_indep) == 2
    assert len(shared_keys_rep_dep) == 1


if __name__ == '__main__':
    test_container()
    test_container_set()
