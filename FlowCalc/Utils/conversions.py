"""
Conversions from common units to SI units. By no means comprehensive, units are
written in so many ways in the wild.
"""
import re
import numpy as np
from typing import Callable

# A dictionary of lambda functions used to convert flow
# profile units into SI units.
# mu: U+03BC
# micro: U+00B5
SI_conversions: dict[str, tuple[Callable[[float], float], str]] = {
    # Volumes
    "µL": (lambda x: x / 1e6, "L"),
    "μL": (lambda x: x / 1e6, "L"),
    "uL": (lambda x: x / 1e6, "L"),
    "µl": (lambda x: x / 1e6, "L"),
    "μl": (lambda x: x / 1e6, "L"),
    "ul": (lambda x: x / 1e6, "L"),
    "mL": (lambda x: x / 1e3, "L"),
    "ml": (lambda x: x / 1e3, "L"),
    "L": (lambda x: x, "L"),
    "l": (lambda x: x, "L"),
    # Times
    "s": (lambda x: x, "s"),
    "h": (lambda x: x * 60, "s"),
    # Angles
    "rad": (lambda x: x, "rad"),
    "degrees": (lambda x: x * np.pi / 180, "rad"),
    # Concentrations
    "nM": (lambda x: x / 1e9, "M"),
    "µM": (lambda x: x / 1e6, "M"),
    "μM": (lambda x: x / 1e6, "M"),
    "uM": (lambda x: x / 1e6, "M"),
    "mM": (lambda x: x / 1e3, "M"),
    "M": (lambda x: x, "M"),
    # Flow rates
    "µL/s": (lambda x: x / 1e6, "L/s"),
    "μL/s": (lambda x: x / 1e6, "L/s"),
    "uL/s": (lambda x: x / 1e6, "L/s"),
    "µl/s": (lambda x: x / 1e6, "L/s"),
    "μl/s": (lambda x: x / 1e6, "L/s"),
    "ul/s": (lambda x: x / 1e6, "L/s"),
    "ml/s": (lambda x: x / 1e3, "L/s"),
    "mL/s": (lambda x: x / 1e3, "L/s"),
    "L/s": (lambda x: x, "L/s"),
    "l/s": (lambda x: x, "L/s"),
    "µL/min": (lambda x: x / (60 * 1e6), "L/s"),
    "μL/min": (lambda x: x / (60 * 1e6), "L/s"),
    "uL/min": (lambda x: x / (60 * 1e6), "L/s"),
    "µl/min": (lambda x: x / (60 * 1e6), "L/s"),
    "μl/min": (lambda x: x / (60 * 1e6), "L/s"),
    "ul/min": (lambda x: x / (60 * 1e6), "L/s"),
    "mL/min": (lambda x: x / (60 * 1e3), "L/s"),
    "ml/min": (lambda x: x / (60 * 1e3), "L/s"),
    "L/min": (lambda x: x / 60, "L/s"),
    "l/min": (lambda x: x / 60, "L/s"),
    "µL/h": (lambda x: x / (3600 * 1e6), "L/s"),
    "μL/h": (lambda x: x / (3600 * 1e6), "L/s"),
    "uL/h": (lambda x: x / (3600 * 1e6), "L/s"),
    "µl/h": (lambda x: x / (3600 * 1e6), "L/s"),
    "μl/h": (lambda x: x / (3600 * 1e6), "L/s"),
    "ul/h": (lambda x: x / (3600 * 1e6), "L/s"),
    "mL/h": (lambda x: x / (3600 * 1e3), "L/s"),
    "ml/h": (lambda x: x / (3600 * 1e3), "L/s"),
    "L/h": (lambda x: x / 3600, "L/s"),
    "l/h": (lambda x: x / 3600, "L/s"),
}


def field_to_SI(field: tuple[float, str]) -> tuple[float, str]:
    """
    Convert a field ([quantity: float, unit: string]) to its SI equivalent.

    Parameters
    ----------
    field: list[float, string]

    Returns
    -------
    si_field: list[float, string]
        Original field converted to SI equivalent.
    """

    value = field[0]
    unit = field[1]

    if not unit in SI_conversions:
        print(f"No conversion for unit {value}/ {unit}.")
        print("Returning original value and unit.")
        return field

    conversion_function, si_unit = SI_conversions[unit]

    si_value = conversion_function(value)

    si_field = (si_value, si_unit)

    return si_field


def SI_convert(header_name: str, value: str | int | float) -> tuple[str, float]:
    """
    Convert a named parameter to its SI equivalent using a find and replace
    strategy. If the given unit is not in SI_conversions, it is left unchanged.

    Parameters
    -----------
    header_name: str
        Expected formats:
            name (unit) e.g. Concentration (μM)
            name/ unit e.g. concentration/ mM
            name [unit] e.g. concentration [mM]
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
    """

    paren_units_regex = f"(?:.*)\((.*)\)"
    sq_brakets_units_regex = f"(?:.*)\[(.*)\]"
    quantity_calculus_units_regex = f"(?:.*\/\s?)(.*)"

    expressions = [
        paren_units_regex,
        sq_brakets_units_regex,
        quantity_calculus_units_regex,
    ]

    unit = "<unit not found!>"
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


def parameters_from_config_file(fname, SI_units=False):
    """
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
    """

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
                    params[clef][ins[0]] = {
                        k: v
                        for k, v in (
                            helper_functions.SI_convert(x, y)
                            for x, y in zip(section_header, ins[1:])
                        )
                    }
                else:
                    params[clef][ins[0]] = {
                        k: float(v) for k, v in zip(section_header, ins[1:])
                    }

    return name, params


def sine_params_from_limits(high, low):
    """
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
    """

    offset = (high + low) / 2

    amplitude = ((high + low) / 2) - low

    return amplitude, offset
