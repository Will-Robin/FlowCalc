import sys
import numpy as np
import tomli_w

from FlowCalc.conversions import SI_conversions


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
            self.syringes[s].calculate_timesteps()

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
            text += f"{self.syringes[s].flow_unit}\n"
            text += f"{number_of_cycles}\n"

            for x in range(0, len(self.syringes[s].flow_profile)):
                flow_val = self.syringes[s].flow_profile[x]
                time_step = time_steps_in_ms[x]
                text += f"{time_step}\t {flow_val}\t{valve_val}\n"

            # Write to file
            with open(filename, "w", encoding="utf-8") as file:
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
        text = f"Dataset,{self.name}\n"
        text += "start_experiment_information\n"
        text += "series_values,#NOT PROVIDED\n"

        text += "start_conditions\n"
        vol = self.reactor_volume
        vol_unit = self.reactor_volume_unit
        text += f"reactor_volume/ {vol_unit},{vol}\n"

        for s in self.syringes:
            syr_name = self.syringes[s].name
            conc_unit = self.syringes[s].conc_unit
            concentration = self.syringes[s].concentration
            text += f"{syr_name}/ {conc_unit},{concentration}\n"

        a_syringe = self.syringes[list(self.syringes)[-1]]
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
            flow_unit_si = SI_conversions[self.syringes[s].flow_unit][1]
            text += f"{s}_flow/ {flow_unit_si},"

            flow_conversion_func = SI_conversions[self.syringes[s].flow_unit][0]

            for x in self.syringes[s].flow_profile:
                si_flow = flow_conversion_func(x)
                text += f"{si_flow},"

            text += "\n"

            tot_flow = tot_flow + flow_conversion_func(self.syringes[s].flow_profile)

        # Convert residence time to seconds
        reactor_conversion = SI_conversions[self.reactor_volume_unit][0]
        residence_time = reactor_conversion(self.reactor_volume) / tot_flow

        text += "Residence time/ s,"

        for r in residence_time:
            text += f"{r},"

        text += "\n"

        text += "end_conditions\n"

        # Write text to file.
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)

    def write_toml(self, filename):

        conditions_dict = self.write_to_dict()

        toml_string = tomli_w.dumps(conditions_dict)

        with open(filename, "w", encoding="utf-8") as file:
            file.write(toml_string)

    def write_to_dict(self):
        """
        conditions_dict: dict
        """

        conditions_dict = {}

        # Write text
        conditions_dict["Dataset"] = self.name
        conditions_dict["Series_values"] = self.series_values
        conditions_dict["Series_unit"] = self.series_unit

        conditions_dict["conditions"] = {}

        conditions_dict["conditions"]["Reactor_volume"] = [
            self.reactor_volume,
            self.reactor_volume_unit,
        ]

        for s in self.syringes:
            syr_name = self.syringes[s].name
            conc_unit = self.syringes[s].conc_unit
            concentration = self.syringes[s].concentration
            conditions_dict["conditions"][syr_name] = [concentration, conc_unit]

        # The following writes a shared time axis for all of the flow profiles.
        # Thus, it is assumed that all of the flow profiles share the same time
        # axis.
        a_syringe = self.syringes[list(self.syringes)[-1]]

        time_conversion = SI_conversions[a_syringe.time_unit]
        time = time_conversion[0](a_syringe.time).tolist()

        conditions_dict["conditions"]["flow_profile_time"] = [time, time_conversion[1]]

        tot_flow = np.zeros(len(a_syringe.time))

        for s in self.syringes:

            flow_conversion = SI_conversions[self.syringes[s].flow_unit]

            flow_si = flow_conversion[0](self.syringes[s].flow_profile).tolist()
            flow_unit = flow_conversion[1]

            conditions_dict["conditions"][f"{s}_flow_profile"] = [flow_si, flow_unit]

            tot_flow = tot_flow + flow_si

        # Convert residence time to seconds
        reactor_conversion = SI_conversions[self.reactor_volume_unit]
        residence_time = reactor_conversion[0](self.reactor_volume) / tot_flow
        res_time = residence_time.tolist()

        conditions_dict["conditions"]["Residence time"] = [
            res_time,
            time_conversion[1],
        ]

        return conditions_dict
