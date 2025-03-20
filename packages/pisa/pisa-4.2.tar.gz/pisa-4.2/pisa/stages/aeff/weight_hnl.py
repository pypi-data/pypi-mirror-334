"""
PISA pi stage to apply HNL specific re-weighting
"""

from __future__ import absolute_import, print_function, division

from pisa import ureg
from pisa.core.param import Param, ParamSet
from pisa.core.stage import Stage
from pisa.utils.profiler import profile

import numpy as np

# is there a place for constants in PISA, or do they already exist?
LIGHTSPEED = 299792458.0 * ureg.m / ureg.s
REDUCEDPLANCK = 6.582119569e-25 * ureg.GeV * ureg.s


def re_weight_hnl(
    U_tau4_sq,
    mass,
    energy,
    tau,
    distance_min,
    distance_max,
    hnl_decay_width,
    c=LIGHTSPEED,
    hbar=REDUCEDPLANCK,
):
    """
    Function to re-weight HNL events (from sampling 1/L to target exponential)

    Parameters
    ----------
    U_tau4_sq : float
        Square of the HNL mixing angle
    mass : float
        HNL mass in GeV
    energy : float
        HNL energy in GeV
    tau : float
        HNL proper lifetime in ns
    distance_min : float
        Minimum sampling distance of HNL decay in m
    distance_max : float
        Maximum sampling distance of HNL decay in m
    hnl_decay_width : float
        HNL decay width in GeV

    Returns
    -------
    weight_lifetime : float
        Weight to re-weight HNL events
    """

    gamma = np.sqrt(energy**2 + mass**2) / mass  # Etot/E0
    speed = c * np.sqrt(1 - np.power(1.0 / gamma, 2))  # c * sqrt(1-1/gamma^2)

    tau_min = distance_min / (gamma * speed)
    tau_max = distance_max / (gamma * speed)

    tau_proper = hbar / (hnl_decay_width * U_tau4_sq)  # this mixing is from the decay vertex

    pdf_inverse = (1.0 / (np.log(tau_max.magnitude) - np.log(tau_min.magnitude))) * (
        1.0 / tau.m_as("s")
    )  # for 1/L sampling of decay length

    pdf_exp1 = 1.0 / tau_proper
    pdf_exp2 = np.exp(-tau / tau_proper)

    pdf_exp = pdf_exp1 * pdf_exp2

    weight_lifetime = pdf_exp / pdf_inverse

    return U_tau4_sq.magnitude * weight_lifetime.magnitude  # includes overall mixing factor of production vertex


class weight_hnl(Stage):  # pylint: disable=invalid-name
    """
    PISA pi stage to apply HNL specific re-weighting.

    This re-weights HNL events from sampling 1/L to target exponential and applies .

    Parameters
    ----------
    params
        Expected params are .. ::
            U_tau4_sq : dimensionless Quantity
    """

    def __init__(
        self,
        **std_kwargs,
    ):
        expected_params = ("U_tau4_sq",)

        expected_container_keys = (
            'mHNL',
            'hnl_true_energy',
            'hnl_proper_lifetime',
            'hnl_distance_min',
            'hnl_distance_max',
            'hnl_decay_width',
            'weights',
        )

        # init base class
        super().__init__(
            expected_params=expected_params,
            expected_container_keys=expected_container_keys,
            **std_kwargs,
        )

    @profile
    def apply_function(self):
        U_tau4_sq = self.params.U_tau4_sq.m_as("dimensionless")

        for container in self.data:
            hnl_weight = re_weight_hnl(
                U_tau4_sq=U_tau4_sq * ureg.dimensionless,
                mass=container["mHNL"] * ureg.GeV,
                energy=container["hnl_true_energy"] * ureg.GeV,
                tau=container["hnl_proper_lifetime"] * ureg.ns,
                distance_min=container["hnl_distance_min"] * ureg.m,
                distance_max=container["hnl_distance_max"] * ureg.m,
                hnl_decay_width=container["hnl_decay_width"] * ureg.GeV,
            )

            container["weights"] *= hnl_weight
            container.mark_changed("weights")


def init_test(**param_kwargs):
    """Instantiation example"""
    param_set = ParamSet([
        Param(name="U_tau4_sq", value=0.1, **param_kwargs)
    ])

    return weight_hnl(params=param_set)
