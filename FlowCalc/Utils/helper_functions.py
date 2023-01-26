import os
import re
import numpy as np

def extend_flow_profile(flow_profile, extension):
    """
    Parameters
    ----------
    flow_profile: array
        Array of flow profile to be extended.
    extension: array
        Array to append to flow profile.

    Returns
    -------
    Wrapper for numpy.hstack() function.
    """
    return np.hstack((flow_profile, extension))


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
