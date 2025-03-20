'''
Implementing an environmentally-induced decoherence model for neutrino oscillations
Based on reference [1], which uses an energy-indepedence decoherence matrix in vacuum

References:
  [1] arxiv:1702.04738
'''



from __future__ import absolute_import, print_function, division

import math
import numpy as np
from numba import guvectorize

from pisa import FTYPE, TARGET, ureg
from pisa.core.param import Param, ParamSet
from pisa.core.stage import Stage
from pisa.utils.profiler import profile
from pisa.stages.osc.osc_params import OscParams
from pisa.stages.osc.layers import Layers
from pisa.stages.osc.prob3numba.numba_osc_hostfuncs import fill_probs
from pisa.utils.resources import find_resource
from pisa import ureg


__all__ = ['DecoherenceParams', 'calc_decoherence_probs', 'decoherence',
           'init_test']

__author__ = 'T. Stuttard, M. Jensen'


class DecoherenceParams(OscParams): #TODO Start using osc_params instead...
    '''
    Container for decoherence oscillation params
    This includes standard oscillation params plus additional 'Gamma' terms parameterising decoherence
    gamma21,31,32 params have units of energy
    '''

    def __init__(self, deltam21, deltam31, theta12, theta13, theta23, deltacp, gamma21, gamma31, gamma32):

        # Call base class constructor
        super().__init__()

        # Store args
        # Note that keeping them as quantities here
        self.dm21 = deltam21
        self.dm31 = deltam31
        self.theta12 = theta12
        self.theta13 = theta13
        self.theta23 = theta23
        self.deltacp = deltacp
        self.gamma21 = gamma21
        self.gamma31 = gamma31
        self.gamma32 = gamma32

        # Get deltam32 (this is what is used in [1])
        self.dm32 = self.dm31 - self.dm21


def calc_decoherence_probs(decoh_params, flav, energy, baseline, prob_e, prob_mu, prob_tau, two_flavor=False):  # pylint: disable=invalid-name
    '''
    Oscillation probability calculator function, with decoherence included

    Parameters
    ----------
    decoh_params :
        DecoherenceParams instance

    flav :
        str : Neutrino flavor

    energy :
        Neutrino true energy values as float(s), either a single value or an array
        If no units attached, must be [GeV]

    baseline :
        Neutrino true propagation distance values as float(s), either a single value or an array
        If no units attached, must be [km]

    prob_e :
        Array of floats of same dimensions as `energy` and `baseline`. Will be filled with probabilities to oscillate to a nue

    prob_mu :
        Array of floats of same dimensions as `energy` and `baseline`. Will be filled with probabilities to oscillate to a numu

    prob_tau :
        Array of floats of same dimensions as `energy` and `baseline`. Will be filled with probabilities to oscillate to a nutau

    two_flavor :
        bool : Flag indicating whether a two- or 3-flavor model should be used
    '''

    # Electron neutrino case
    # For nu_e case, in this approiximation we are essential neglecting nu_e oscillations
    # If a particle starts as a nu_e, it stays as a nu_e
    if flav.startswith("nue"):
        prob_e.fill(1.)
        prob_mu.fill(0.)

    # Muon neutrino case
    # For nu_mu case, in this approximation there is 0. probability of becoming a nu_e
    # Use numu disappearance calculation to get numu/tau probs
    elif flav.startswith("numu"):
        prob_e.fill(0.)
        numu_disappearance_func = _calc_numu_disappearance_prob_2flav if two_flavor else _calc_numu_disappearance_prob_3flav
        numu_survival_prob = 1. - numu_disappearance_func( decoh_params=decoh_params, E=energy, L=baseline )
        np.copyto(src=numu_survival_prob,dst=prob_mu) #TODO avoid this wasted data copy

    else:
        raise ValueError( "Input flavor '%s' not supported" % flav)

    # Assume unitarity
    np.copyto(src=1.-prob_e-prob_mu,dst=prob_tau)


def _calc_numu_disappearance_prob_2flav(decoh_params,E,L):
    """
    Calculate numu disppearance in 2-flavor model
    User should no call this directly, instead use `calc_decoherence_probs`
    Define two-flavor decoherence approximation according to Eqn 2 from [1]

    Parameters
    ----------
    decoh_params :
        DecoherenceParams instance

    E :
        Neutrino true energy values as float(s), either a single value or an array
        If no units attached, must be [GeV]

    L :
        Neutrino true propagation distance values as float(s), either a single value or an array
        If no units attached, must be [km]
    """

    # This line is a standard oscillations (no decoherence) 2 flavour approximation, can use for debugging
    #return np.sin(2.*decoh_params.theta23.m_as("rad"))**2 * np.square(np.sin(1.27*decoh_params.dm32.m_as("eV**2")*L/E))

    # Assume units if none provided for main input arrays
    # Would prefer to get units but is not always the case
    E = E if isinstance(E,ureg.Quantity) else E * ureg["GeV"]
    L = L if isinstance(L,ureg.Quantity) else L * ureg["km"]

    # Calculate normalisation term
    norm_term = 0.5 * ( np.sin( 2. * decoh_params.theta23.m_as("rad") )**2 )

    # Calculate decoherence term
    decoh_term = np.exp( -decoh_params.gamma32.m_as("eV") * ( L.m_as("m")/1.97e-7 ) ) #Convert L from [m] to natural units

    # Calculate oscillation term
    osc_term = np.cos( ( 2. * 1.27 * decoh_params.dm32.m_as("eV**2") * L.m_as("km") ) / ( E.m_as("GeV") ) )

    return norm_term * ( 1. - (decoh_term*osc_term) )


def _update_pmns_matrix(theta12, theta13, theta23):
    """
    Helper function used by _calc_numu_disappearance_prob_3flav
    Updates the PMNS matrix and its complex conjugate.
    Must be called by the class each time one of the PMNS matrix parameters are changed.
    """

    # TODO Mikkel needs to reference code he used as inspiration here

    c12  =  math.cos( theta12.m_as("rad") )
    c13  =  math.cos( theta13.m_as("rad") )
    c23  =  math.cos( theta23.m_as("rad") )
    s12  =  math.sin( theta12.m_as("rad") )
    s13  =  math.sin( theta13.m_as("rad") )
    s23  =  math.sin( theta23.m_as("rad") )
    eid  = 0.0 # e^( i * delta_cp)
    emid = 0.0 # e^(-i * delta_cp)

    matrix      = np.zeros((3,3))
    anti_matrix = np.zeros((3,3))

    matrix[0,0] = c12 * c13
    matrix[0,1] = s12 * c13
    matrix[0,2] = s13 * emid

    matrix[1,0] = (0. - s12*c23 ) - ( c12*s23*s13*eid )
    matrix[1,1] = ( c12*c23 ) - ( s12*s23*s13*eid )
    matrix[1,2] = s23*c13

    matrix[2,0] = ( s12*s23 ) - ( c12*c23*s13*eid)
    matrix[2,1] = ( 0. - c12*s23 ) - ( s12*c23*s13*eid )
    matrix[2,2] = c23*c13

    anti_matrix = matrix.conjugate()

    return matrix, anti_matrix


def _calc_numu_disappearance_prob_3flav(decoh_params, E, L):
    """
    Calculate numu disppearance in 3-flavor model

    User should no call this directly, instead use `calc_decoherence_probs`

    Define three-flavor decoherence approximation according to the equation that is not numbered but can be
    found between equations 2 and 3 in [1],with the notable difference that we are using the vacuum case
    (e.g. not substituting in the effeective matter values for parameters)

    Parameters
    ----------
    decoh_params :
        DecoherenceParams instance

    E :
        Neutrino true energy values as float(s), either a single value or an array
        If no units attached, must be [GeV]

    L :
        Neutrino true propagation distance values as float(s), either a single value or an array
        If no units attached, must be [km]
    """
    E = E if isinstance(E,ureg.Quantity) else E * ureg["GeV"]
    L = L if isinstance(L,ureg.Quantity) else L * ureg["km"]

    # Get PMNS matrix
    U,_ = _update_pmns_matrix(decoh_params.theta12, decoh_params.theta13, decoh_params.theta23)

    # Decoherence matrix
    Gamma = np.zeros([3,3])
    Gamma[1][0] = decoh_params.gamma21.m_as("GeV")
    Gamma[2][0] = decoh_params.gamma31.m_as("GeV")
    Gamma[2][1] = decoh_params.gamma32.m_as("GeV")

    # Mass splitting matrix
    delta_jk = np.zeros([3,3])
    delta_jk[1][0] = decoh_params.dm21.m_as("eV**2")
    delta_jk[2][0] = decoh_params.dm31.m_as("eV**2")
    delta_jk[2][1] = decoh_params.dm32.m_as("eV**2")

    prob_dec = np.zeros(np.shape(E))

    for i_j in range(3):
        for i_k in range(3):
            if i_j > i_k:
                prob_dec += abs(U[2][i_j])**2 * abs(U[2][i_k])**2 * (1.0 - np.exp( - Gamma[i_j][i_k] * L.m_as("km") * 5.07e+18) * np.cos(delta_jk[i_j][i_k] * 1.0e-18 / (2.0 * E.m_as("GeV")) * L.m_as("km") * 5.07e+18))
    prob_array = 2.0 * prob_dec.real

    return prob_array




class decoherence(Stage):
    """
    PISA Pi stage representing oscillations in the presence of decoherence

    Parameters
    ----------
    params
        Expected contents of `params` ParamSet: .. ::

            detector_depth : float
            earth_model : PREM file path
            prop_height : quantity (dimensionless)
            YeI : quantity (dimensionless)
            YeO : quantity (dimensionless)
            YeM : quantity (dimensionless)
            theta12 : quantity (angle)
            theta13 : quantity (angle)
            theta23 : quantity (angle)
            deltam21 : quantity (mass^2)
            deltam31 : quantity (mass^2)
            deltacp : quantity (angle)
            gamma12 : quantity (energy)
            gamma13 : quantity (energy)
            gamma23 : quantity (energy)

        Expected container keys are .. ::

            "true_energy"
            "true_coszen"
            "weights"
            "nubar"
            "flav"
            "sys_flux"

    """
    def __init__(self,
                 **std_kwargs,
                ):

        expected_params = ('detector_depth',
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
                           'deltacp',
                           'gamma21',
                           'gamma31',
                           'gamma32',
                          )

        expected_container_keys = (
            'true_energy',
            'true_coszen',
            'weights',
            'nubar',
            'flav',
            'sys_flux',
            
        )

        # init base class
        super().__init__(
            expected_params=expected_params,
            expected_container_keys=expected_container_keys,
            **std_kwargs,
        )

        #Have not yet implemented matter effects
        if self.params.earth_model.value is not None:
            raise ValueError("Matter effects not yet implemented for decoherence, must set 'earth_model' to None")


        self.layers = None

        #Toggle between 2-flavor and 3-flavor models
        self.two_flavor = False


    def setup_function(self):

        # setup Earth model
        if self.params.earth_model.value is not None:
            earth_model = find_resource(self.params.earth_model.value)
            YeI = self.params.YeI.value.m_as('dimensionless')
            YeO = self.params.YeO.value.m_as('dimensionless')
            YeM = self.params.YeM.value.m_as('dimensionless')
        else:
            earth_model = None

        # setup the layers
        prop_height = self.params.prop_height.value.m_as('km')
        detector_depth = self.params.detector_depth.value.m_as('km')
        self.layers = Layers(earth_model, detector_depth, prop_height)
        if earth_model is not None:
            self.layers.setElecFrac(YeI, YeO, YeM)

        # set the correct data mode
        self.data.representation = self.calc_mode

        # --- calculate the layers ---
        if self.data.is_map:
            # speed up calculation by adding links
            # as layers don't care about flavour
            self.data.link_containers('nu', ['nue_cc', 'numu_cc', 'nutau_cc',
                                             'nue_nc', 'numu_nc', 'nutau_nc',
                                             'nuebar_cc', 'numubar_cc', 'nutaubar_cc',
                                             'nuebar_nc', 'numubar_nc', 'nutaubar_nc'])

        for container in self.data:
            if self.params.earth_model.value is not None:
                self.layers.calcLayers(container['true_coszen'])
                container['densities'] = self.layers.density.reshape((container.size, self.layers.max_layers))
                container['distances'] = self.layers.distance.reshape((container.size, self.layers.max_layers))
            else:
                self.layers.calcPathLength(container['true_coszen'])
                container['distances'] = self.layers.distance

        # don't forget to un-link everything again
        self.data.unlink_containers()

        # --- setup empty arrays ---
        if self.data.is_map:
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


    @profile
    def compute_function(self):

        # set the correct data mode
        self.data.representation = self.calc_mode

        if self.data.is_map:
            # speed up calculation by adding links
            self.data.link_containers('nu', ['nue_cc', 'numu_cc', 'nutau_cc',
                                             'nue_nc', 'numu_nc', 'nutau_nc'])
            self.data.link_containers('nubar', ['nuebar_cc', 'numubar_cc', 'nutaubar_cc',
                                                'nuebar_nc', 'numubar_nc', 'nutaubar_nc'])

        # --- update params ---
        self.decoh_params = DecoherenceParams(deltam21=self.params.deltam21.value,
                                            deltam31=self.params.deltam31.value,
                                            theta12=self.params.theta12.value,
                                            theta13=self.params.theta13.value,
                                            theta23=self.params.theta23.value,
                                            deltacp=self.params.deltacp.value,
                                            gamma21=self.params.gamma21.value,
                                            gamma31=self.params.gamma31.value,
                                            gamma32=self.params.gamma32.value)

        # Calculate oscillation probabilities
        for container in self.data:
            self.calc_probs(container['nubar'],
                            container['true_energy'],
                            #container['densities'],
                            container['distances'],
                            out=container['probability'],
                           )

        # the following is flavour specific, hence unlink
        self.data.unlink_containers()

        for container in self.data:
            # initial electrons (0)
            fill_probs(container['probability'],
                       0, # electron
                       container['flav'],
                       out=container['prob_e'],
                      )
            # initial muons (1)
            fill_probs(container['probability'],
                       1, # muon
                       container['flav'],
                       out=container['prob_mu'],
                      )

            container.mark_changed('prob_e')
            container.mark_changed('prob_mu')



    @profile
    def apply_function(self):

        # update the outputted weights
        for container in self.data:
            apply_probs(container['sys_flux'],
                        container['prob_e'],
                        container['prob_mu'],
                        out=container['weights'])
            container.mark_changed('weights')


    def calc_probs(self, nubar, e_array, len_array, out):

        #Get the probability values output array
        prob_array = out

        #Attach units
        L = len_array * ureg["km"]
        E = e_array * ureg["GeV"]

        #nue
        calc_decoherence_probs( decoh_params=self.decoh_params, flav="nue", energy=E, baseline=L, prob_e=prob_array[:,0,0], prob_mu=prob_array[:,0,1], prob_tau=prob_array[:,0,2], two_flavor=self.two_flavor )

        #numu
        calc_decoherence_probs( decoh_params=self.decoh_params, flav="numu", energy=E, baseline=L, prob_e=prob_array[:,1,0], prob_mu=prob_array[:,1,1], prob_tau=prob_array[:,1,2], two_flavor=self.two_flavor )

        #nutau (basically just the inverse of the numu case)
        np.copyto(dst=prob_array[:,2,0], src=prob_array[:,1,0])
        np.copyto(dst=prob_array[:,2,1], src=prob_array[:,1,2])
        np.copyto(dst=prob_array[:,2,2], src=prob_array[:,1,1])

        #Register that arrays have changed
        out



# vectorized function to apply (flux * prob)
# must be outside class
if FTYPE == np.float64:
    signature = '(f8[:], f8, f8, f8[:])'
else:
    signature = '(f4[:], f4, f4, f4[:])'
@guvectorize([signature], '(d),(),()->()', target=TARGET)
def apply_probs(flux, prob_e, prob_mu, out):
    out[0] *= (flux[0] * prob_e) + (flux[1] * prob_mu)


def init_test(**param_kwargs):
    """Initialisation example"""
    param_set = ParamSet([
        Param(name='detector_depth', value=0.5*ureg.km, **param_kwargs),
        Param(name='prop_height', value=20*ureg.km, **param_kwargs),
        Param(name='earth_model', value=None, **param_kwargs),
        Param(name='YeI', value=0.5, **param_kwargs),
        Param(name='YeO', value=0.5, **param_kwargs),
        Param(name='YeM', value=0.5, **param_kwargs),
        Param(name='theta12', value=33*ureg.degree, **param_kwargs),
        Param(name='theta13', value=8*ureg.degree, **param_kwargs),
        Param(name='theta23', value=50*ureg.degree, **param_kwargs),
        Param(name='deltam21', value=8e-5*ureg.eV**2, **param_kwargs),
        Param(name='deltam31', value=3e-3*ureg.eV**2, **param_kwargs),
        Param(name='deltacp', value=180*ureg.degree, **param_kwargs),
        Param(name='gamma21', value=1e-11*ureg.GeV, **param_kwargs),
        Param(name='gamma31', value=5e-10*ureg.GeV, **param_kwargs),
        Param(name='gamma32', value=2.5e-13*ureg.GeV, **param_kwargs),
    ])
    return decoherence(params=param_set)
