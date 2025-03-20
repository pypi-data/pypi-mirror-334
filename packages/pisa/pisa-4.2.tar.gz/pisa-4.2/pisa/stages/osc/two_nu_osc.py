"""
PISA pi stage for the calculation osc. probabilities assuming two-neutrino model

"""
from __future__ import absolute_import, print_function, division

import numpy as np
from numba import guvectorize

from pisa import FTYPE, ITYPE, TARGET, ureg
from pisa.core.param import Param, ParamSet
from pisa.core.stage import Stage
from pisa.utils.profiler import profile
from pisa.utils.numba_tools import myjit

__all__ = ['two_nu_osc', 'calc_probs', 'apply_probs_vectorized', 'init_test']

class two_nu_osc(Stage):  # pylint: disable=invalid-name
    """
    two neutrino osc PISA Pi class

    Parameters
    ----------
        Expected params .. ::
        
            theta : quantity (angle)
            deltam31 : quantity (mass^2)
    
        Expected container keys are .. ::

            "true_energy"
            "true_coszen"
            "nu_flux"
            "weights"

    Notes
    -----
    For two-neutrino model, there is only one mass-splitting term
    Atmospheric mixing angle is aproximated by theta (sin^2(2*theta))

    """
    def __init__(self,
                 **std_kwargs,
                ):

        expected_params = (
            'theta',
            'deltam31',
        )

        expected_container_keys = (
            'true_energy',
            'true_coszen',
            'nu_flux',
            'weights'
        )

        # init base class
        super().__init__(
            expected_params=expected_params,
            expected_container_keys=expected_container_keys,
            **std_kwargs,
        )


    @profile
    def apply_function(self):

        theta = self.params.theta.value.m_as('dimensionless')
        deltam31 = self.params.deltam31.value.m_as('eV**2')

        for container in self.data:
            if 'numu' in container.name:
                apply_probs_vectorized(container['nu_flux'],
                                    FTYPE(theta),
                                    FTYPE(deltam31),
                                    container['true_energy'],
                                    container['true_coszen'],
                                    ITYPE(1),
                                    out=container['weights'],
                                   )

            if 'nutau' in container.name:
                apply_probs_vectorized(container['nu_flux'],
                                    FTYPE(theta),
                                    FTYPE(deltam31),
                                    container['true_energy'],
                                    container['true_coszen'],
                                    ITYPE(3),
                                    out=container['weights'],
                                   )
            if 'nue' in container.name:
                apply_probs_vectorized(container['nu_flux'],
                                    FTYPE(theta),
                                    FTYPE(deltam31),
                                    container['true_energy'],
                                    container['true_coszen'],
                                    ITYPE(0),
                                    out=container['weights'],
                                   )
            container.mark_changed('weights')

@myjit
def calc_probs(t23, dm31, true_energy, true_coszen): #
    ''' calculate osc prob of numu to nutau '''
    L1 = 19. # atmospheric production height
    R = 6378.2 + L1 # mean radius of the Earth + L1
    phi = np.arcsin((1-L1/R)*np.sin(np.arccos(true_coszen)))
    psi = np.arccos(true_coszen) - phi
    propdist = np.sqrt( (R-L1)**2 + R**2 - (2*(R-L1)*R*np.cos(psi)))

    return t23*np.sin(1.267*dm31*propdist/true_energy)**2 # constant arise from conversion of units for L and E

# vectorized function to apply (flux * prob)
# must be outside class
if FTYPE == np.float64:
    FX = 'f8'
    IX = 'i8'
else:
    FX = 'f4'
    IX = 'i4'
signature = f'({FX}[:], {FX}, {FX}, {FX}, {FX}, {IX}, {FX}[:])'
@guvectorize([signature], '(d),(),(),(),(),()->()', target=TARGET)
def apply_probs_vectorized(flux, t23, dm31, true_energy, true_coszen, nuflav, out):
    if nuflav==1: # numu receive weights dependent on numu survival prob
        out[0] *= flux[1] * (1.0-calc_probs(t23, dm31, true_energy, true_coszen))
    elif nuflav==3: # nutau receive weights dependent on nutau appearance prob
        out[0] *= flux[1] * calc_probs(t23, dm31, true_energy, true_coszen)
    else:
        assert nuflav==0
        out[0] *= flux[0]


def init_test(**param_kwargs):
    """Instantiation example"""
    param_set = ParamSet([
        Param(name='theta', value=45*ureg.degree, **param_kwargs),
        Param(name='deltam31', value=2.5e-3*ureg.eV**2, **param_kwargs),
    ])
    return two_nu_osc(params=param_set)
