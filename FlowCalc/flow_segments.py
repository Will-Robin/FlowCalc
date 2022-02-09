import numpy as np
from FlowCalc import flow_segments as FlS

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
    gauss_component = FlS._1gaussian(time, amp, center, sigma)
    WP = FlS.sine_wave_flow(period, gauss_component, phase, offset, time)
    return WP
