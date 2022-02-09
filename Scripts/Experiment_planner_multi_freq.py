import numpy as np
import matplotlib.pyplot as plt
import os

def write_flow_profile(name, unit, number_of_cycles, profile, timestep, valve_val = 255):
    '''
    A function for creating a flow profile file for Nemesys pumps from an array.

    Parameters
    ----------
    name: str
        name for output file

    unit: str
        units for flow values. Choose from: nl/s, µl/s, µl/min, µl/h, ml/min,
        ml/h and mm/s.

    number_of_cycles: int
        0 is an infinite loop, other nunmbers indicate how many times the flow
        profile is repeated

    profile: 1Darray
        array containing flow rate values over time.

    timestep: float
        The time between switching flow values in seconds. Converted to ms
        (as an int) for output.

    valve_val: int
        valve setting for the output flow profile. 255 is default.

    Output
    -------

    file: "filename".nfp
        a file which can be read by Nemesys Pump software (see manual).

    '''

    filename = "{}_flow_profile.nfp".format(name)

    # Convert timestep to ms
    out_tstep = int(timestep*1000)

    with open(filename, "w") as f:
        f.write("{}\n".format(unit))
        f.write("{}\n".format(number_of_cycles))
        for x in range(0,len(profile)):
            f.write("{}\t {}\t{}\n".format(out_tstep,profile[x],valve_val))

def generate_sine_wave(period, amplitude, phase, offset, time, timestep = 0.1):
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

    time_array: 1Darray
        An array of time values for the sine wave.

    wave: 1Darray
        An array of flow rate values.

    '''

    time_array = np.linspace(0,time, num = int(time/timestep))
    wave = amplitude*np.sin(2*np.pi*time_array/period + phase) + offset

    return time_array, wave

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

font  = 15

with open("input_file_multi_freq.csv", "r") as f:
    for line in f:
        if "Dataset" in line:
            ins = line.strip("\n").split(",")
            Exp_name = ins[1]
        if "period/ min" in line:
            ins = line.strip("\n").split(",")
            pd = [float(x) for x in ins[1:] if x != ""]
        if "direct flow rate/ microL/h" in line:
            ins = line.strip("\n").split(",")
            static_flow = float(ins[1])
        if "sine flow bounds/ microL/h" in line:
            ins = line.strip("\n").split(",")
            high = float(ins[1])
            low = float(ins[2])
        if "reactor volume/ microL" in line:
            ins = line.strip("\n").split(",")
            reactor_vol = float(ins[1])

try:
    os.chdir(Exp_name)

except:
    os.mkdir(Exp_name)
    os.chdir(Exp_name)

'''Settings'''

amp,off = sine_params_from_limits(high,low) # calculate the amplitude and offset for the flow profile as a sine wave
total_flow_rate = (8*off)
residence_time = 3600*reactor_vol/total_flow_rate # seconds
periods = [p*60 for p in pd] # list of periods in s

t_add = 0
for p in periods:
    t_add += p*5 + 10*residence_time
time =  15*residence_time + t_add
ph_dha = 0
ph_water = np.pi # phase difference between dihydroxyacetone flow and water
tstep = 2 #  time step for changing flow rates in seconds
flow_unit = "µl/h"

wave_NaOH_flow = np.full(int(15*residence_time/2),off)
wave_water = np.full(int(15*residence_time/2),off)

for p in periods:
    p_time = 5*p
    '''Flow profile calculations'''
    time_NaOH_flow_ins,NaOH_flow_ins = generate_sine_wave(p, amp,   ph_dha, off, p_time, timestep = tstep) # calculate sine wave for dihydroxyacetone
    time_water_ins,wave_water_ins    = generate_sine_wave(p, amp, ph_water, off, p_time, timestep = tstep)

    wave_DHA = np.hstack((wave_DHA,wave_DHA_ins))
    wave_water = np.hstack((wave_water,wave_water_ins))

    wave_DHA = np.hstack((wave_DHA,np.full(1200,off)))
    wave_water = np.hstack((wave_water,np.full(1200,off)))

time_NaOH = np.linspace(0,time, num = time/2)
time_water = np.linspace(0,time, num = time/2)

'''Create direct flow profiles'''
wave_DHA = np.full(len(NaOH_flow), static_flow/2)
CaCl2_flow = np.full(len(NaOH_flow), static_flow)
HCHO_flow  = np.full(len(NaOH_flow), static_flow)

'''Calculate the overall flow rate'''
tot_flow = wave_DHA + wave_water + CaCl2_flow + NaOH_flow + HCHO_flow
residence_time = reactor_vol/tot_flow[0]

print("flow rate = {} µl/h. Residence_time for {} µl reactor: {} min, period: {} min".format(tot_flow[0], reactor_vol, 60*reactor_vol/tot_flow[0],[p/60 for p in periods]))

'''Write flow profiles to files'''
write_flow_profile("{}_dihydroxyacetone".format(Exp_name), flow_unit, 1, wave_DHA, tstep)
write_flow_profile("{}_water".format(Exp_name), flow_unit, 1, wave_water, tstep)
write_flow_profile("{}_CaCl2".format(Exp_name), flow_unit, 1, CaCl2_flow, tstep)
write_flow_profile("{}_NaOH".format(Exp_name), flow_unit, 1, NaOH_flow, tstep)
write_flow_profile("{}_HCHO".format(Exp_name), flow_unit, 1, HCHO_flow, tstep)


'''
Output draft conditions file
'''
with open("{}_conditions.csv".format(Exp_name), "w") as f:
    f.write("Dataset,{}\n".format(Exp_name))
    f.write("start_experiment_information\n")
    f.write("dilution_factor,#NOT PROVIDED\n")
    f.write("series_values,#NOT PROVIDED\n")
    f.write("series_unit,#NOT PROVIDED\n")
    f.write("series_regions,#NOT PROVIDED\n")
    f.write("internal_ref_region,#NOT PROVIDED\n")
    f.write("internal_ref_concentration/ M,#NOT PROVIDED\n")
    f.write("end_experiment_information\n")

    f.write("start_conditions\n")
    f.write("reactor_volume/ uL,{}\n".format(reactor_vol))
    f.write("residence_time/ min,{}\n".format(residence_time*60))
    f.write("DHA_concentration_0/ M,#NOT PROVIDED\n")
    f.write("CaCl2_concentration_0/ M,#NOT PROVIDED\n")
    f.write("NaOH_concentration_0/ M,#NOT PROVIDED\n")
    f.write("HCHO_concentration_0/ M,#NOT PROVIDED\n")

    f.write("CaCl2_flow/ uL/h,{}\n".format(CaCl2_flow[0]))
    f.write("NaOH_flow/ uL/h,{}\n".format(NaOH_flow[0]))
    f.write("HCHO_flow/ uL/h,{}\n".format(HCHO_flow[0]))

    f.write("flow_profile_time/ s,")
    [f.write("{},".format(x)) for x in time_DHA]
    f.write("\n")
    f.write("DHA_flow_profile/ uL/h,")
    [f.write("{},".format(x)) for x in wave_DHA]
    f.write("\n")

    f.write("water_flow_profile/ uL/h,")
    [f.write("{},".format(x)) for x in wave_water]
    f.write("\n")

    f.write("end_conditions\n")

'''
Output plots
'''
fig, ax = plt.subplots(figsize=(10,10))
#ax.plot(time_DHA/60, tot_flow, label = "total")
ax.plot(time_DHA/60, wave_DHA, label = "dihydroxyacetone", linewidth = 3)
ax.plot(time_water/60, wave_water, label = "H$_2$O", linewidth = 3)
ax.plot(time_water/60, CaCl2_flow, label = "CaCl$_2$", linewidth = 3)
ax.plot(time_water/60, NaOH_flow, label = "NaOH", linewidth = 2)
ax.plot(time_water/60, HCHO_flow, label = "HCHO", linewidth = 1)

ax.set_xlabel("time/ minutes", fontsize = font)
ax.set_ylabel("flow rate ({}) ".format(flow_unit), fontsize = font)
ax.tick_params(labelsize = font, axis = "both")
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.3, box.width, box.height * 0.7])
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), fancybox=True, shadow=True, ncol=4, fontsize = font)
plt.savefig("{}_flow_profiles".format(Exp_name))
plt.show()
plt.clf()
