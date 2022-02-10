import os
import re
import numpy as np
from conversions import SI_conversions

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
    Convert a named parameter to its SI equivalent using a find and replace
    strategy. If the given unit is not in SI_conversions, it is left unchanged.

    Parameters
    -----------
    header_name: str
        Expected formats:
            name (unit) e.g. Concentration (μM)
            name/ unit e.g. concentration/ mM
            name [unit] e.g. concentration/ mM
    value: str, int or float
        Value of the parameter. It must be possible to convert this value to a
        float if it is not already a float.

    Returns
    -------
    (header_name, value): tuple
        header_name: str
            Parameter name with SI or unchanged units.
        value: float
            Value of parameter in SI or unchanged units
    '''

    paren_units_regex = f"(?:.*)\((.*)\)"
    sq_brakets_units_regex = f"(?:.*)\[(.*)\]"
    quantity_calculus_units_regex = f"(?:.*\/\s?)(.*)"

    expressions = [
                    paren_units_regex,
                    sq_brakets_units_regex,
                    quantity_calculus_units_regex
                    ]

    unit = '<unit not found!>'
    for expr in expressions:
        matches = re.match(expr, header_name)
        if matches != None:
            unit = matches.group(1)

    if unit in SI_conversions.keys():
        converted_unit = SI_conversions[unit][1]
        conversion = SI_conversions[unit][0]

        converted_value = conversion(float(value))

        new_header_name = header_name.replace(unit, converted_unit)

        return new_header_name, converted_value

    else:
        print("No SI conversion given for <<{}>>".format(unit))

        return header_name, float(value)

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
