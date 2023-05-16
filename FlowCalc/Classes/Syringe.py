import numpy as np


class Syringe:
    def __init__(self, name):
        """
        An object which stores the information for a Syringe in an experiment.

        Parameters
        ----------
        name: str
            name for syringe

        Attributes
        ----------
        self.name: str
        self.concentration: float
        self.conc_unit: str
        self.time: array like
        self.time_steps: array like
        self.time_unit: str
        self.flow_profile: array like
        self.flow_unit: str
        """

        self.name = name

        self.concentration = 0.0
        self.conc_unit = ""

        self.time = []
        self.timesteps = []
        self.time_unit = ""

        self.flow_profile = []
        self.flow_unit = ""

    def set_concentration(self, value, unit):
        """
        Set the concentration of the syringe.

        Parameters
        ----------
        value: float
            Concentration value.
        unit: str
            Concentration unit.
        """

        self.concentration = value
        self.conc_unit = unit

    def set_flow_profile(self, time_vals, time_unit, flow_profile, flow_unit):
        """
        Add a flow profile into the Syringe object.

        Parameters
        ----------
        time_vals: array
            array of time values for the flow profile.
        flow_profile: array
            flow rate values for the flow profile.
        time_unit: str
            time axis unit.
        flow_unit: str
            Flow rate unit.

        Returns
        -------
        None
        """

        self.time = time_vals
        self.time_unit = time_unit
        self.calculate_timesteps()

        self.flow_profile = flow_profile
        self.flow_unit = flow_unit

    def calculate_timesteps(self):
        """
        Calculate the timesteps between the values in self.time
        """

        time_steps = np.diff(self.time)

        # The last flow step will be held for as long as the one preceding it
        time_steps = np.hstack((time_steps, time_steps[-1]))

        self.timesteps = time_steps
