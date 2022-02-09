import numpy as np
import os

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

def SI_convert(header_name, value):
    '''
    Convert a named parameter to its SI equivalent (if given in SI_conversions,
    otherwise left unchanged, see below).

    Parameters
    -----------
    header_name: str
        Expected format: name (unit) e.g. Concentration (uM)
    value: str, int or float
        Value of the parameter

    Returns
    -------
    (header_name, value): tuple
        header_name: str
            Parameter name with SI or unchanged units.
        value: float
            Value of parameter in SI or unchanged units


    '''

    SI_conversions = {"h":(60, "s"),
                     "degrees": (np.pi/180, "rad"),
                     "uL/h":((10e-6)/(60*60), "L/s"),
                     "uM": (10e-6, "M")}

    cut_out = header_name[header_name.find("(")+1:header_name.find(")")]

    if cut_out in SI_conversions.keys():
        return header_name.replace(cut_out, SI_conversions[cut_out][1]), float(value)*SI_conversions[cut_out][0]
    else:
        print("No SI conversion given for {}".format(cut_out))
        return header_name,float(value)

def parameters_from_config_file(fname, SI_units = False):
    '''
    Get experiment configuration from a standard format .csv file.

    Parameters
    ----------
    fname: str
        File name or path to file with file name appended.
    SI_units: bool
        True: converts units in spreadsheet to SI using SI_convert()
        False: Reads in values as given in spreadsheet.

    Returns
    -------
    name: str
        Experiment name as given in file.
    params:
        Dictionary of dictionaries for parameters. {Section: {param: value}}
    '''

    lineproc = lambda x: x.strip("\n").split(",")
    params = {}
    readstate = False
    with open(fname, "r") as f:
        lines = []
        for line in f:
            if "Experiment name" in line:
                name = lineproc(line)[1]
            if "Section" in line:
                ins = lineproc(line)
                clef = ins[0]
                params[clef] = {}
                section_header = ins[1:]
                readstate = True
                line = next(f)
            if readstate:
                ins = lineproc(line)
                if SI_units:
                    params[clef][ins[0]] = {k:v for k,v in (helper_functions.SI_convert(x,y) for x,y in zip(section_header, ins[1:]))}
                else:
                    params[clef][ins[0]] = {k:float(v) for k,v in zip(section_header, ins[1:])}

    return name, params
