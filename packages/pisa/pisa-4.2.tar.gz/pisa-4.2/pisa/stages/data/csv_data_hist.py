"""
A Stage to load data from a CSV datarelease format file into a PISA pi ContainerSet
"""

from __future__ import absolute_import, print_function, division

import pandas as pd

from pisa import FTYPE
from pisa.core.stage import Stage
from pisa.utils.resources import find_resource
from pisa.core.container import Container

__all__ = ['csv_data_hist', 'init_test']


class csv_data_hist(Stage):  # pylint: disable=invalid-name
    """
    CSV file loader PISA Pi class

    Parameters
    ----------

    events_file : csv file path

    """
    def __init__(self,
                 events_file,
                 **std_kwargs,
                ):

        # instantiation args that should not change
        self.events_file = find_resource(events_file)

        expected_params = ()

        # init base class
        super().__init__(
            expected_params=expected_params,
            expected_container_keys=(),
            **std_kwargs,
        )


    def setup_function(self):

        events = pd.read_csv(self.events_file)

        container = Container('total')
        container.representation = self.calc_mode

        container['weights'] = events['count'].values.astype(FTYPE)
        container['reco_energy'] = events['reco_energy'].values.astype(FTYPE)
        container['reco_coszen'] = events['reco_coszen'].values.astype(FTYPE)
        container['pid'] = events['pid'].values.astype(FTYPE)

        self.data.add_container(container)

        # check created at least one container
        if len(self.data.names) == 0:
            raise ValueError(
                'No containers created during data loading for some reason.'
            )


def init_test(**param_kwargs):
    """Instantiation example"""
    return csv_data_hist(events_file='events/IceCube_3y_oscillations/data.csv.bz2')
