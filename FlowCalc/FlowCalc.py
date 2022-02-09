import numpy as np
import matplotlib.pyplot as plt
import os
font  = 15

# A dictionary of lambda functions used to convert flow
# profile units into SI units.
fl_SI_conversions = {"µl/h"   : (lambda x: x/(360*10e6)),
                     "µl/min" : (lambda x: x/(60*10e6)),
                     "µl/s"   : (lambda x: x/10e6),

                     "ml/h"   : (lambda x: x/(360*10e3)),
                     "ml/min" : (lambda x: x/(60*10e3)),
                     "ml/s"   : (lambda x: x/10e3),

                     "l/h"    : (lambda x: x/360),
                     "l/min"  : (lambda x: x/60),
                     "l/s"    : (lambda x: x) }
class Syringe:
    def __init__(self, name, concentration):
        '''
        name: str
            name for syringe
        concentration: float
            concentration inside syringe
        '''
        self.name = name
        self.concentration = concentration
        self.conc_unit = "M"

    def add_flow_profile(self, time_vals, flow_profile):
        '''
        time_vals: array
            array of time values for the flow profile.
        flow_profile: array
            flow rate values for the flow profile.
        '''

        self.time = time_vals
        self.flow_profile = flow_profile

class Flow_Experiment:
    def __init__(self, exp_name, reactor_vol, fl_un, syringe_set = []):
        '''
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
        syringe: Syringe object
            Syringe to be added to the set.
        '''
        self.syringes[syringe.name] = syringe

    def write_flow_profile(self, number_of_cycles = 1, valve_val = 255):
        '''
        A function for creating a flow profile file for Nemesys pumps from an array.

        Parameters
        ----------
        number_of_cycles: int
            0 is an infinite loop, other nunmbers indicate how many times the flow
            profile is repeated

        valve_val: int
            valve setting for the output flow profile. 255 is default.

        Output
        -------
        file: "filename".nfp
            a file which can be read by Nemesys Pump software (see manual).

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

        A .csv file conditions file summarising the calculated experimental details.

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

            f.write("flow_profile_time/ s,")
            [f.write("{},".format(x)) for x in self.syringes[s].time]
            f.write("\n")

            tot_flow = np.zeros(len(self.syringes[s].time))

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
        global font
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
        A plot of the flow proflies calculated.
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



def change_dir(name):
    '''
    Uses os to change directory. If the folder exists,
    the directory given in the argument exists, it becomes
    the working directory. Otherwise, it is created, then
    becomes the working directory.

    Parameters
    ----------
    name: str
        path to folder.
    '''
    os.makedirs(name, exist_ok = True)
    os.chdir(name)

def time_segment(start, end, step):
    '''
    Creates a time segment.

    Parameters
    ----------
    start: float
        Start time for segment in seconds.
    end: float
        End time for segment in seconds.
    step: int
        Step increment in s.

    Returns
    -------
    Wrapper for numpy.arange() function
    '''

    return np.arange(start, end, step)

def unmod_flow(time, value):
    '''
    Parameters
    ----------
    time: array
        Array of time values
    value: float
        The flow rate to be maintatined over the time
        segment.
    Returns
    -------
    Wrapper for numpy.full function.
    '''
    return np.full(len(time), value)

def sine_wave_flow(period, amplitude, phase, offset, time):
    '''
    For generating a sine wave flow profile.

    Parameters
    ----------
    period: float
        The period of the sine wave in seconds.

    amplitude: float
        The amplitude of the sine wave (any unit: think of output).

    phase:
        Phase shift

    offset: float
        The centre of the sine wave.

    Returns
    -------
    wave: 1Darray
        An array of flow rate values.
    '''

    wave = amplitude*np.sin(2*np.pi*time/period + phase) + offset

    return wave

def extend_flow_profile(flow_profile,extension):
    '''
    Parameters
    ----------
    flow_profile: array
        Array of flow profile to be extended.
    extension: array
        Array to append to flow profile.

    Returns
    -------
    Wrapper for numpy.hstack() function.
    '''
    return np.hstack((flow_profile, extension))

def _1gaussian(x, amp1, cen1, sigma1):
    '''
    A single gaussian function
    Parameters
    ----------
    x: array
        x axis data
    amp1: float
        amplitude of the function
    cen1: float
        centre of the function (mean)
    sigma1: float
        width of the function (standard deviation)
    Returns
    -------
    function: numpy array
        y values for the function
    '''
    return amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp(-((x-cen1)**2)/((2*sigma1)**2)))

def sine_params_from_limits(high,low):
    '''
    To determine the ampliutde and offet for a sine wave given high and low
    flow rates

    Parameters
    ----------

    high: float
        High flow rate limit (any unit, think of output).

    low: float
        Low flow rate limit (any unit, think of output).

    Returns
    -------

    amplitude: float
        Amplitude of the sine wave. Same units as parameters.

    offset: float
        Offet of the sine wave. Same units as parameters.
    '''

    offset = (high+low)/2

    amplitude = ((high+low)/2)-low

    return amplitude, offset

def generate_wave_packet(time, amp, period, center, sigma, offset, phase = 0):
    '''
    Generate a wave-packet style flow profile.

    Parameters
    ----------
    time:array
    amp: float
    period: float
    center: float
    sigma: float
    offset: float
    phase: float

    Returns
    -------
    WP: array
    '''
    gauss_component = _1gaussian(time, amp, center, sigma)
    WP = sine_wave_flow(period, gauss_component, phase, offset, time)
    return WP
