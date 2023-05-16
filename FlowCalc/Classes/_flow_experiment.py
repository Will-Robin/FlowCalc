import sys
import numpy as np


class FlowExperiment:
    def __init__(self, exp_name, syringe_set=[]):
        """
        An object to store experimental information.

        Parameters
        ----------
        exp_name: str
            A name for the experiment.

        Attributes
        ----------
        self.name: str
        self.reactor_volume: float
        self.syringes: dict
        """

        self.name = exp_name
        self.reactor_volume = 0.0
        self.reactor_volume_unit = ""

        self.series_values = []
        self.series_unit = ""

        if len(syringe_set) == 0:
            self.syringes = {}
        else:
            self.syringes = {s.name: s for s in syringe_set}

    def add_syringe(self, syringe):
        """
        Add a Syringe object to the experiment.

        Parameters
        ----------
        syringe: Syringe object
            Syringe to be added to the set.

        Returns
        -------
        None
        """

        self.syringes[syringe.name] = syringe
