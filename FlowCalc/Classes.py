import sys
import numpy as np

from FlowCalc.conversions import SI_conversions


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
            Concetration unit.
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

        self.flow_profile = flow_profile
        self.flow_unit = time_unit

    def calculate_timesteps(self):
        """
        Calculate the timesteps between the values in self.time
        """

        time_steps = np.diff(self.time)

        # The last flow step will be held for as long as the one preceding it
        time_steps = np.hstack((time_steps, time_steps[-1]))

        self.timesteps = time_steps


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

    def write_flow_profile(self, path, number_of_cycles=1, valve_val=255):
        """
        A function for creating a flow profile file for Nemesys pumps from an
        array.

        output file: "filename".nfp
            a file which can be read by Nemesys Pump software (see manual).

        Parameters
        ----------
        path: str
            Relative or absolute path to an existing directory to store the
            output.
        number_of_cycles: int
            0 is an infinite loop, other nunmbers indicate how many times the
            flow profile is repeated

        valve_val: int
            valve setting for the output flow profile. 255 is default.

        Returns
        -------
        None
        """

        for s in self.syringes:

            filename = f"{path}/{self.syringes[s].name}_flow_profile.nfp"

            # Get timesteps for the syringe.
            self.syringes[s].calculate_timesteps

            syr_time_steps = self.syringes[s].timesteps

            time_unit = self.syringes[s].time_unit

            if time_unit in SI_conversions:
                conversion_to_s = SI_conversions[time_unit][0]
                time_steps_in_s = conversion_to_s(syr_time_steps)
            else:
                syr_name = self.syringes[s].name
                sys.exit(
                    f"""Syringe {syr_name}: Please provide the units for
                        the flow profile time axis, or check if there is a
                        conversion available in Flowcalc.conversions"""
                )

            # Convert time steps to ms
            time_steps_in_ms = np.round(time_steps_in_s, 1) * 1000

            # Build output text
            text = ""
            text += f"{self.flow_unit}\n"
            text += f"{number_of_cycles}\n"

            for x in range(0, len(self.syringes[s].flow_profile)):
                flow_val = self.syringes[s].flow_profile[x]
                time_step = time_steps_in_ms[x]
                text += f"{time_step}\t {flow_val}\t{valve_val}\n"

            # Write to file
            with open(filename, "w") as file:
                file.write(text)

    def write_conditions_file(self, filename):
        """
        Output draft conditions file

        Parameters
        ----------
        filename: str
            Name for the output file.

        Output
        ------
        None
        """

        # Write text
        text += f"Dataset,{self.name}\n"
        text += "start_experiment_information\n"
        text += "dilution_factor,#NOT PROVIDED\n"
        text += "series_values,#NOT PROVIDED\n"
        text += "series_unit,#NOT PROVIDED\n"
        text += "series_regions,#NOT PROVIDED\n"
        text += "internal_ref_region,#NOT PROVIDED\n"
        text += "internal_ref_concentration/ M,#NOT PROVIDED\n"
        text += "end_experiment_information\n"

        text += "start_conditions\n"
        vol = self.reactor_volume
        vol_unit = self.reactor_volume_unit
        text += f"reactor_volume/ {vol_unit},{vol}\n"

        for s in self.syringes:
            syr_name = self.syringes[s].name
            conc_unit = self.syringes[s].conc_unit
            concentration = self.syringes[s].concentration
            text += f"{syr_name}/ {conc_unit},{concentration}\n"

        a_syringe = list(self.syringes)[-1]
        text += "flow_profile_time/ s,"

        # The following writes a shared time axis for all of the flow profiles.
        # Thus, it is assumed that all of the flow profiles share the same time
        # axis.
        time_conversion_func = SI_conversions[a_syringe.time_unit][0]
        for x in a_syringe.time:
            si_time = time_conversion_func(x)
            text += f"{si_time},"

        text += "\n"

        tot_flow = np.zeros(len(a_syringe.time))

        for s in self.syringes:
            text += f"{s}_flow/ {self.flow_unit},"

            flow_conversion_func = SI_conversions[self.syringes[s].flow_unit][0]

            for x in self.syringes[s].flow_profile:
                si_time = time_conversion_func(x)
                text += f"{si_time}"

            text += "\n"

            tot_flow = tot_flow + time_conversion_func(self.syringes[s].flow_profile)

        # Convert residence time to seconds
        reactor_conversion = SI_conversions[self.reactor_unit][0]
        reactor_vol_unit = SI_conversions[self.reactor_volume][1]
        residence_time = reactor_conversion(self.reactor_volume) / tot_flow

        text += "Residence time/ s,"

        for r in residence_time:
            text += f"{r}"

        text += "\n"

        text += "end_conditions\n"

        # Write text to file.
        with open(filename, "w") as file:
            file.write(text)
