import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interpolate

class Syringe:
    def __init__(self, name, concentration):
        '''
        An object which stores the information for a Syringe in an experiment.

        Parameters
        ----------
        name: str
            name for syringe
        concentration: float
            concentration inside syringe

        Attributes
        ----------
        self.name: str
        self.concentration: float
        self.conc_unit: str
        self.time: array like
        self.flow_profile: array like
        self.interpolation: None or interpolate.interp1d()
        '''

        self.name = name
        self.concentration = concentration
        self.conc_unit = "M"
        self.time = []
        self.flow_profile = []
        self.interpolation = None

    def add_flow_profile(self, time_vals, flow_profile):
        '''
        Add a flow profile into the Syringe object.

        Parameters
        ----------
        time_vals: array
            array of time values for the flow profile.
        flow_profile: array
            flow rate values for the flow profile.

        Returns
        -------
        None
        '''

        self.time = time_vals
        self.flow_profile = flow_profile
        self.interpolation = interpolate.interp1d(time_vals,flow_profile, kind = "linear")

class Flow_Experiment:
    def __init__(self, exp_name, reactor_vol, fl_un, syringe_set = []):
        '''
        An object to store experimental information.

        Parameters
        ----------
        exp_name: str
            A name for the experiment.
        reactor_vol: float
            Volume of the reactor in uL.
        fl_un: str
            Units for the flow profiles.
        syringe_set: list of Syringe objects.
            Syringes of which the Syringe_Set consists.
            A list of syringes can be added when the
            Syringe_Set object is created, or they can be
            added one by one using the add_syringe method.

        Attributes
        ----------
        self.name: str
        self.reactor_volume: float
        self.flow_unit: str
        self.syringes: dict
        '''

        self.name = exp_name
        self.reactor_volume = reactor_vol
        self.flow_unit = fl_un

        if len(syringe_set) == 0:
            self.syringes = {}
        else:
            self.syringes = {s.name:s for s in syringe_set}

    def add_syringe(self,syringe):
        '''
        Add a Syringe object to the experiment.

        Parameters
        ----------
        syringe: Syringe object
            Syringe to be added to the set.

        Returns
        -------
        None
        '''

        self.syringes[syringe.name] = syringe

    def write_flow_profile(self, number_of_cycles = 1, valve_val = 255):
        '''
        A function for creating a flow profile file for Nemesys pumps from an
        array.

        output file: "filename".nfp
            a file which can be read by Nemesys Pump software (see manual).

        Parameters
        ----------
        number_of_cycles: int
            0 is an infinite loop, other nunmbers indicate how many times the
            flow profile is repeated

        valve_val: int
            valve setting for the output flow profile. 255 is default.

        Output
        -------
        None
        '''

        for s in self.syringes:

            filename = "{}_flow_profile.nfp".format(self.syringes[s].name)

            # Convert timestep to ms
            out_tstep = int(round(self.syringes[s].time[-1]/ len(self.syringes[s].time),1))*1000

            with open(filename, "w") as f:
                f.write("{}\n".format(self.flow_unit))
                f.write("{}\n".format(number_of_cycles))
                for x in range(0,len(self.syringes[s].flow_profile)):
                    f.write("{}\t {}\t{}\n".format(out_tstep,self.syringes[s].flow_profile[x],valve_val))

    def write_conditions_file(self):
        '''
        Output draft conditions file

        Parameters
        ----------
        Exp_name: str
            Name for the experiment (used in output file name and information).
        reactor_vol: float
            Volume of the flow reactor in uL
        syringes: dict
            Dictionary of syringe concentrations e.g. "NaOH0_concentration/ M": 0.12
        flow_profiles: dict
            Dictionary of flow profiles
            e.g. NaOH_flow_profile/ uL/h : np.array([1,2,...])

        Output
        ------
        None
        '''

        with open("{}_conditions.csv".format(self.name), "w") as f:
            f.write("Dataset,{}\n".format(self.name))
            f.write("start_experiment_information\n")
            f.write("dilution_factor,#NOT PROVIDED\n")
            f.write("series_values,#NOT PROVIDED\n")
            f.write("series_unit,#NOT PROVIDED\n")
            f.write("series_regions,#NOT PROVIDED\n")
            f.write("internal_ref_region,#NOT PROVIDED\n")
            f.write("internal_ref_concentration/ M,#NOT PROVIDED\n")
            f.write("end_experiment_information\n")

            f.write("start_conditions\n")
            f.write("reactor_volume/ uL,{}\n".format(self.reactor_volume))

            for s in self.syringes:
                f.write("{}/ {},{}\n".format(self.syringes[s].name, self.syringes[s].conc_unit, self.syringes[s].concentration))

            a_syringe = list(self.syringes)[-1]
            f.write("flow_profile_time/ s,")
            [f.write("{},".format(x)) for x in a_syringe.time]
            f.write("\n")

            tot_flow = np.zeros(len(a_syringe.time))

            for s in self.syringes:
                f.write("{}_flow/ {},".format(s, self.flow_unit))
                [f.write("{},".format(x)) for x in self.syringes[s].flow_profile]
                f.write("\n")
                tot_flow = tot_flow + self.syringes[s].flow_profile

            residence_time = 60*60*self.reactor_volume/tot_flow

            f.write("Residence time/ s,")
            [f.write("{},".format(r)) for r in residence_time]
            f.write("\n")

            f.write("end_conditions\n")

    def plot_profiles(self):
        '''
        Output plots

        Parameters
        ----------
        time: numpy 1D array
            Array of time values for the flow profile
        flow_profiles: dict
            Dictionary of flow profiles
            e.g. NaOH_flow_profile/ uL/h : np.array([1,2,...])
        Exp_name: str
            Name for the experiment (used in output file name).
        flow_unit: str
            Units for the flow rates calculated

        Output
        ------
        None
        '''
        fig, ax = plt.subplots(figsize=(20,20))

        for f in self.syringes:
            ax.plot(self.syringes[f].time/60, self.syringes[f].flow_profile, label = f, linewidth = 3)

        ax.set_xlabel("time/ minutes", fontsize = font)
        ax.set_ylabel("flow rate ({}) ".format(self.flow_unit), fontsize = font)
        ax.tick_params(labelsize = font, axis = "both")
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.3, box.width, box.height * 0.7])
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), fancybox=True, shadow=True, ncol=4, fontsize = font)
        plt.savefig("{}_flow_profiles".format(self.name))
        plt.show()
        plt.clf()
