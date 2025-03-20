"""
PISA pi stage for the calculation of earth layers and osc. probabilities

Maybe it would amke sense to split this up into a separate earth layer stage
and an osc. stage....todo

"""

from __future__ import absolute_import, print_function, division

import numpy as np

from pisa import FTYPE, ureg
from pisa.core.param import Param, ParamSet
from pisa.core.stage import Stage
from pisa.utils.log import logging
from pisa.stages.osc.nsi_params import StdNSIParams, VacuumLikeNSIParams
from pisa.stages.osc.osc_params import OscParams
from pisa.stages.osc.decay_params import DecayParams
from pisa.stages.osc.lri_params import LRIParams
from pisa.stages.osc.scaling_params import Mass_scaling, Core_scaling_w_constrain, Core_scaling_wo_constrain
from pisa.stages.osc.layers import Layers
from pisa.stages.osc.prob3numba.numba_osc_hostfuncs import propagate_array, fill_probs
from pisa.utils.resources import find_resource

__all__ = ['prob3', 'init_test']


class prob3(Stage):  # pylint: disable=invalid-name
    """
    Prob3-like oscillation PISA Pi class

    Parameters
    ----------
    params
        Expected params .. ::

            detector_depth : float
            earth_model : PREM file path
            prop_height : quantity (dimensionless)
            YeI : quantity (dimensionless)
            YeO : quantity (dimensionless)
            YeM : quantity (dimensionless)
            density_scale : quantity (dimensionless)
            core_density_scale : quantity (dimensionless)
            innermantle_density_scale : quantity (dimensionless)
            middlemantle_density_scale : quantity (dimensionless)
            theta12 : quantity (angle)
            theta13 : quantity (angle)
            theta23 : quantity (angle)
            deltam21 : quantity (mass^2)
            deltam31 : quantity (mass^2)
            deltacp : quantity (angle)
            eps_scale : quantity(dimensionless)
            eps_prime : quantity(dimensionless)
            phi12 : quantity(angle)
            phi13 : quantity(angle)
            phi23 : quantity(angle)
            alpha1 : quantity(angle)
            alpha2 : quantity(angle)
            deltansi : quantity(angle)
            eps_ee : quantity (dimensionless)
            eps_emu_magn : quantity (dimensionless)
            eps_emu_phase : quantity (angle)
            eps_etau_magn : quantity (dimensionless)
            eps_etau_phase : quantity (angle)
            eps_mumu : quantity(dimensionless)
            eps_mutau_magn : quantity (dimensionless)
            eps_mutau_phase : quantity (angle)
            eps_tautau : quantity (dimensionless)
            decay_alpha3 : quantity (energy^2)
            v_lri : quantity (eV)

        Expected container keys are .. ::

            "true_energy"
            "true_coszen"
            "nubar"
            "flav"
            "nu_flux"
            "weights"

    **kwargs
        Other kwargs are handled by Stage
    -----

    """

    def __init__(
      self,
      nsi_type=None,
      reparam_mix_matrix=False,
      neutrino_decay=False,
      tomography_type=None,
      lri_type=None,
      **std_kwargs,
    ):

        expected_params = (
          'detector_depth',
          'earth_model',
          'prop_height',
          'YeI',
          'YeO',
          'YeM',
          'theta12',
          'theta13',
          'theta23',
          'deltam21',
          'deltam31',
          'deltacp'
        )

        expected_container_keys = (
            'true_energy',
            'true_coszen',
            'nubar',
            'flav',
            'nu_flux',
            'weights'
        )


        # Check whether and if so with which NSI parameters we are to work.
        if nsi_type is not None:
            choices = ['standard', 'vacuum-like']
            nsi_type = nsi_type.strip().lower()
            if not nsi_type in choices:
                raise ValueError(
                    'Chosen NSI type "%s" not available! Choose one of %s.'
                    % (nsi_type, choices)
                )
        self.nsi_type = nsi_type
        """Type of NSI to assume."""
        self.tomography_type = tomography_type
        self.reparam_mix_matrix = reparam_mix_matrix
        """Use a PMNS mixing matrix parameterisation that differs from
           the standard one by an overall phase matrix
           diag(e^(i*delta_CP), 1, 1). This has no impact on
           oscillation probabilities in the *absence* of NSI."""

        self.neutrino_decay = neutrino_decay

        if neutrino_decay:
            self.decay_flag = 1
        else :
            self.decay_flag = -1
        """Invoke neutrino decay with neutrino oscillation."""


        if self.nsi_type is None:
            nsi_params = ()
        elif self.nsi_type == 'vacuum-like':
            nsi_params = ('eps_scale',
                          'eps_prime',
                          'phi12',
                          'phi13',
                          'phi23',
                          'alpha1',
                          'alpha2',
                          'deltansi'
            )
        elif self.nsi_type == 'standard':
            nsi_params = ('eps_ee',
                          'eps_emu_magn',
                          'eps_emu_phase',
                          'eps_etau_magn',
                          'eps_etau_phase',
                          'eps_mumu',
                          'eps_mutau_magn',
                          'eps_mutau_phase',
                          'eps_tautau'
            )

        if self.neutrino_decay :
            decay_params = ('decay_alpha3',)
        else:
            decay_params = ()

        if lri_type is not None:
            choices = ['emu-symmetry', 'etau-symmetry', 'mutau-symmetry']
            lri_type = lri_type.strip().lower()
            if not lri_type in choices:
                raise ValueError(
                    'Chosen LRI symmetry type "%s" not available! Choose one of %s.'
                    % (lri_type, choices)
                )
        self.lri_type = lri_type

        if self.lri_type is None:
            lri_params = ()
        else:
            lri_params = ('v_lri',)


        if self.tomography_type is None:
            tomography_params = ()
        elif self.tomography_type == 'mass_of_earth':
            tomography_params = ('density_scale',)
        elif self.tomography_type == 'mass_of_core_w_constrain':
            tomography_params = ('core_density_scale',)
        elif self.tomography_type == 'mass_of_core_wo_constrain':
            tomography_params = ('core_density_scale',
                                 'innermantle_density_scale',
                                 'middlemantle_density_scale'
            )


        expected_params = (expected_params + nsi_params + decay_params
                           + lri_params + tomography_params)

        # init base class
        super().__init__(
            expected_params=expected_params,
            expected_container_keys=expected_container_keys,
            **std_kwargs,
        )


        self.layers = None
        self.osc_params = None
        self.nsi_params = None
        self.tomography_params = None
        self.decay_params = None
        self.decay_matrix = None
        self.lri_params = None
        self.lri_pot = None
        # The interaction potential (Hamiltonian) just scales with the
        # electron density N_e for propagation through the Earth,
        # even(to very good approx.) in the presence of generalised interactions
        # (NSI), which is why we can simply treat it as a constant here.
        self.gen_mat_pot_matrix_complex = None
        """Interaction Hamiltonian without the factor sqrt(2)*G_F*N_e."""
        self.YeI = None
        self.YeO = None
        self.YeM = None

    def setup_function(self):

        # object for oscillation parameters
        self.osc_params = OscParams()
        if self.reparam_mix_matrix:
            logging.debug(
                'Working with reparameterizated version of mixing matrix.'
            )
        else:
            logging.debug(
                'Working with standard parameterization of mixing matrix.'
            )
        if self.nsi_type == 'vacuum-like':
            logging.debug('Working in vacuum-like NSI parameterization.')
            self.nsi_params = VacuumLikeNSIParams()
        elif self.nsi_type == 'standard':
            logging.debug('Working in standard NSI parameterization.')
            self.nsi_params = StdNSIParams()


        if self.neutrino_decay:
            logging.debug('Working with neutrino decay')
            self.decay_params = DecayParams()

        if self.lri_type is not None:
            logging.debug('Working with LRI')
            self.lri_params = LRIParams()


        if self.tomography_type == "mass_of_earth":
            logging.debug('Working with a single density scaling factor.')
            self.tomography_params = Mass_scaling()
        elif self.tomography_type == "mass_of_core_w_constrain":
            logging.debug('Working with different scaling for different layers.')
            self.tomography_params = Core_scaling_w_constrain()
        elif self.tomography_type == "mass_of_core_wo_constrain":
            logging.debug('Working without any external constraints')
            self.tomography_params = Core_scaling_wo_constrain()


        # setup the layers
        #if self.params.earth_model.value is not None:
        earth_model = find_resource(self.params.earth_model.value)
        self.YeI = self.params.YeI.value.m_as('dimensionless')
        self.YeO = self.params.YeO.value.m_as('dimensionless')
        self.YeM = self.params.YeM.value.m_as('dimensionless')
        prop_height = self.params.prop_height.value.m_as('km')
        detector_depth = self.params.detector_depth.value.m_as('km')
        self.layers = Layers(earth_model, detector_depth, prop_height)
        self.layers.setElecFrac(self.YeI, self.YeO, self.YeM)


        # --- calculate the layers ---
        if self.is_map:
            # speed up calculation by adding links
            # as layers don't care about flavour
            self.data.link_containers('nu', ['nue_cc', 'numu_cc', 'nutau_cc',
                                             'nue_nc', 'numu_nc', 'nutau_nc',
                                             'nuebar_cc', 'numubar_cc', 'nutaubar_cc',
                                             'nuebar_nc', 'numubar_nc', 'nutaubar_nc'])

        for container in self.data:
            self.layers.calcLayers(container['true_coszen'])
            container['densities'] = self.layers.density.reshape((container.size, self.layers.max_layers))
            container['distances'] = self.layers.distance.reshape((container.size, self.layers.max_layers))

        # don't forget to un-link everything again
        self.data.unlink_containers()

        # --- setup empty arrays ---
        if self.is_map:
            self.data.link_containers('nu', ['nue_cc', 'numu_cc', 'nutau_cc',
                                             'nue_nc', 'numu_nc', 'nutau_nc'])
            self.data.link_containers('nubar', ['nuebar_cc', 'numubar_cc', 'nutaubar_cc',
                                                'nuebar_nc', 'numubar_nc', 'nutaubar_nc'])
        for container in self.data:
            container['probability'] = np.empty((container.size, 3, 3), dtype=FTYPE)
        self.data.unlink_containers()

        # setup more empty arrays
        for container in self.data:
            container['prob_e'] = np.empty((container.size), dtype=FTYPE)
            container['prob_mu'] = np.empty((container.size), dtype=FTYPE)

    def calc_probs(self, nubar, e_array, rho_array, len_array, out):
        ''' wrapper to execute osc. calc '''
        if self.reparam_mix_matrix:
            mix_matrix = self.osc_params.mix_matrix_reparam_complex
        else:
            mix_matrix = self.osc_params.mix_matrix_complex

        logging.debug('matter potential:\n%s'
                          % self.gen_mat_pot_matrix_complex)
        logging.debug('decay matrix:\n%s'
                          % self.decay_matix)

        propagate_array(self.osc_params.dm_matrix, # pylint: disable = unexpected-keyword-arg, no-value-for-parameter
                        mix_matrix,
                        self.gen_mat_pot_matrix_complex,
                        self.decay_flag,
                        self.decay_matix,
                        self.lri_pot,
                        nubar,
                        e_array,
                        rho_array,
                        len_array,
                        out=out
                       )

    def compute_function(self):

        if self.is_map:
            # speed up calculation by adding links
            self.data.link_containers('nu', ['nue_cc', 'numu_cc', 'nutau_cc',
                                             'nue_nc', 'numu_nc', 'nutau_nc'])
            self.data.link_containers('nubar', ['nuebar_cc', 'numubar_cc', 'nutaubar_cc',
                                                'nuebar_nc', 'numubar_nc', 'nutaubar_nc'])

        # this can be done in a more clever way (don't have to recalculate all paths)
        YeI = self.params.YeI.value.m_as('dimensionless')
        YeO = self.params.YeO.value.m_as('dimensionless')
        YeM = self.params.YeM.value.m_as('dimensionless')

        if YeI != self.YeI or YeO != self.YeO or YeM != self.YeM:
            self.YeI = YeI; self.YeO = YeO; self.YeM = YeM
            self.layers.setElecFrac(self.YeI, self.YeO, self.YeM)
            for container in self.data:
                self.layers.calcLayers(container['true_coszen'])
                container['densities'] = self.layers.density.reshape((container.size, self.layers.max_layers))
                container['distances'] = self.layers.distance.reshape((container.size, self.layers.max_layers))


        # some safety checks on units
        # trying to avoid issue of angles with no dimension being assumed to be radians
        # here we enforce the user must speficy a valid angle unit
        for angle_param in [self.params.theta12, self.params.theta13, self.params.theta23, self.params.deltacp] :
            assert angle_param.value.units != ureg.dimensionless, "Param %s is dimensionless, but should have angle units [rad, degree]" % angle_param.name

        # --- update mixing params ---
        self.osc_params.theta12 = self.params.theta12.value.m_as('rad')
        self.osc_params.theta13 = self.params.theta13.value.m_as('rad')
        self.osc_params.theta23 = self.params.theta23.value.m_as('rad')
        self.osc_params.dm21 = self.params.deltam21.value.m_as('eV**2')
        self.osc_params.dm31 = self.params.deltam31.value.m_as('eV**2')
        self.osc_params.deltacp = self.params.deltacp.value.m_as('rad')
        if self.nsi_type == 'vacuum-like':
            self.nsi_params.eps_scale = self.params.eps_scale.value.m_as('dimensionless')
            self.nsi_params.eps_prime = self.params.eps_prime.value.m_as('dimensionless')
            self.nsi_params.phi12 = self.params.phi12.value.m_as('rad')
            self.nsi_params.phi13 = self.params.phi13.value.m_as('rad')
            self.nsi_params.phi23 = self.params.phi23.value.m_as('rad')
            self.nsi_params.alpha1 = self.params.alpha1.value.m_as('rad')
            self.nsi_params.alpha2 = self.params.alpha2.value.m_as('rad')
            self.nsi_params.deltansi = self.params.deltansi.value.m_as('rad')
        elif self.nsi_type == 'standard':
            self.nsi_params.eps_ee = self.params.eps_ee.value.m_as('dimensionless')
            self.nsi_params.eps_emu = (
                (self.params.eps_emu_magn.value.m_as('dimensionless'),
                self.params.eps_emu_phase.value.m_as('rad'))
            )
            self.nsi_params.eps_etau = (
                (self.params.eps_etau_magn.value.m_as('dimensionless'),
                self.params.eps_etau_phase.value.m_as('rad'))
            )
            self.nsi_params.eps_mumu = self.params.eps_mumu.value.m_as('dimensionless')
            self.nsi_params.eps_mutau = (
                (self.params.eps_mutau_magn.value.m_as('dimensionless'),
                self.params.eps_mutau_phase.value.m_as('rad'))
            )
            self.nsi_params.eps_tautau = self.params.eps_tautau.value.m_as('dimensionless')
        if self.neutrino_decay:
            self.decay_params.decay_alpha3 = self.params.decay_alpha3.value.m_as('eV**2')

        if self.lri_type is not None:
            self.lri_params.v_lri = self.params.v_lri.value.m_as('eV')
        if self.tomography_type is not None:
            if self.tomography_type == "mass_of_earth":
                self.tomography_params.density_scale = self.params.density_scale.value.m_as('dimensionless')
                self.layers.scaling(scaling_array=self.tomography_params.density_scale)
            elif self.tomography_type == "mass_of_core_w_constrain":
                self.tomography_params.core_density_scale = self.params.core_density_scale.value.m_as('dimensionless')
                self.layers.scaling(scaling_array=self.tomography_params.scaling_array)
            elif self.tomography_type == "mass_of_core_wo_constrain":
                self.tomography_params.core_density_scale = self.params.core_density_scale.value.m_as('dimensionless')
                self.tomography_params.innermantle_density_scale = self.params.innermantle_density_scale.value.m_as('dimensionless')
                self.tomography_params.middlemantle_density_scale = self.params.middlemantle_density_scale.value.m_as('dimensionless')
                self.layers.scaling(scaling_array=self.tomography_params.scaling_factor_array)
            self.layers.setElecFrac(self.YeI, self.YeO, self.YeM)
            for container in self.data:
                self.layers.calcLayers(container['true_coszen'])
                container['densities'] = self.layers.density.reshape((container.size, self.layers.max_layers))


        # now we can proceed to calculate the generalised matter potential matrix
        std_mat_pot_matrix = np.zeros((3, 3), dtype=FTYPE) + 1.j * np.zeros((3, 3), dtype=FTYPE)
        std_mat_pot_matrix[0, 0] += 1.0

        # add effective nsi coupling matrix
        if self.nsi_type is not None:
            logging.debug('NSI matrix:\n%s' % self.nsi_params.eps_matrix)
            self.gen_mat_pot_matrix_complex = (
                std_mat_pot_matrix + self.nsi_params.eps_matrix
            )
            logging.debug('Using generalised matter potential:\n%s'
                          % self.gen_mat_pot_matrix_complex)
        else:
            self.gen_mat_pot_matrix_complex = std_mat_pot_matrix
            logging.debug('Using standard matter potential:\n%s'
                          % self.gen_mat_pot_matrix_complex)

        if self.neutrino_decay:
            self.decay_matix = self.decay_params.decay_matrix
            logging.debug('Decay matrix:\n%s' % self.decay_params.decay_matrix)
        else :
            self.decay_matix = np.zeros((3, 3), dtype=FTYPE) + 1.j * np.zeros((3, 3), dtype=FTYPE)

        self.lri_pot = np.zeros((3, 3), dtype=FTYPE)
        types_lri = ['emu-symmetry', 'etau-symmetry', 'etau-symmetry']
        if self.lri_type is not None:
            if self.lri_type == 'emu-symmetry':
                self.lri_pot = self.lri_params.potential_matrix_emu
            elif self.lri_type == 'etau-symmetry':
                self.lri_pot = self.lri_params.potential_matrix_etau
            elif self.lri_type == 'mutau-symmetry':
                self.lri_pot = self.lri_params.potential_matrix_mutau
            else:
                # TODO: this just repeats the logic from init with slightly different code!
                raise ValueError("Implemented symmetries are %s" % types_lri)


        for container in self.data:
            self.calc_probs(container['nubar'],
                            container['true_energy'],
                            container['densities'],
                            container['distances'],
                            out=container['probability'],
                           )
            container.mark_changed('probability')

        # the following is flavour specific, hence unlink
        self.data.unlink_containers()

        for container in self.data:
            # initial electrons (0)
            fill_probs(container['probability'],
                       0,
                       container['flav'],
                       out=container['prob_e'],
                      )
            # initial muons (1)
            fill_probs(container['probability'],
                       1,
                       container['flav'],
                       out=container['prob_mu'],
                      )

            container.mark_changed('prob_e')
            container.mark_changed('prob_mu')


    def apply_function(self):

        # maybe speed up like this?
        #self.data.representation = self.calc_mode
        #for container in self.data:
        #    container['oscillated_flux'] = (container['nu_flux'][:,0] * container['prob_e']) + (container['nu_flux'][:,1] * container['prob_mu'])

        #self.data.representation = self.apply_mode

        # update the outputted weights
        for container in self.data:
            container['weights'] *= (container['nu_flux'][:,0] * container['prob_e']) + (container['nu_flux'][:,1] * container['prob_mu'])


def init_test(**param_kwargs):
    """Initialisation example"""
    param_set = ParamSet([
        Param(name='detector_depth', value=10*ureg.km, **param_kwargs),
        Param(name='prop_height', value=18*ureg.km, **param_kwargs),
        Param(name='earth_model', value='osc/PREM_4layer.dat', **param_kwargs),
        Param(name='YeI', value=0.5, **param_kwargs),
        Param(name='YeO', value=0.5, **param_kwargs),
        Param(name='YeM', value=0.5, **param_kwargs),
        Param(name='theta12', value=33*ureg.degree, **param_kwargs),
        Param(name='theta13', value=8*ureg.degree, **param_kwargs),
        Param(name='theta23', value=50*ureg.degree, **param_kwargs),
        Param(name='deltam21', value=8e-5*ureg.eV**2, **param_kwargs),
        Param(name='deltam31', value=3e-3*ureg.eV**2, **param_kwargs),
        Param(name='deltacp', value=180*ureg.degree, **param_kwargs),
    ])
    return prob3(params=param_set)
