import sys
sys.path.append(r"C:\Users\willi\Documents\Packages")
from FlowCalc import Classes, flow_segments, helper_functions
import numpy as np
import os

'''General parameters'''
Exp_name = "FRN099"
directory = r"C:\Users\willi\Documents\Data\Conditions_files"
flow_unit = "µl/h"
time_step = 2 #  time step for changing flow rates in seconds
reactor_vol  = 411

os.chdir(directory)

modulated_component = "dihydroxyacetone"

syringes = [Classes.Syringe(modulated_component, 0.4),
            Classes.Syringe("glycolaldehyde_dimer", 0.4),
            Classes.Syringe("NaOH", 0.120),
            Classes.Syringe("CaCl2", 0.06),
            Classes.Syringe("water", 0)]

amplitudes = {modulated_component   : 770.625, # in flow_units
              "glycolaldehyde_dimer"    : 0,
              "CaCl2"           : 0,
              "NaOH"            : 0,
              "water"           : 770.625 }

phases     = {modulated_component   : 0, # in radians
              "glycolaldehyde_dimer"    : 0,
              "CaCl2"           : 0,
               "NaOH"            : 0,
              "water"           : np.pi }

direct_flows = {modulated_component    : 1541.25, # in flow_units
                "glycolaldehyde_dimer"     : 3082.50,
                "CaCl2"            : 3082.50,
                "NaOH"             : 3082.50,
                "water"            : 1541.25 }

flow_profiles = {modulated_component   : np.array([]), # Empty to begin with, but can begin with numpy arrays.
                 "glycolaldehyde_dimer"    : np.array([]),
                 "CaCl2"           : np.array([]),
                 "NaOH"            : np.array([]),
                 "water"           : np.array([])}

periods = [6] # in minutes

period = 6*60
HCHO_off = [3082.50/40,3082.50/20,3082.50/4]
sum = direct_flows["water"] + direct_flows["glycolaldehyde_dimer"]
flat_time = 20*60
mod_time = 11*period
run_time = np.array([])

for o in HCHO_off:
    direct_flows["water"] = sum - o

    direct_flows["glycolaldehyde_dimer"] = o

    flat_seg   = flow_segments.time_segment(0,flat_time, time_step)
    mod_seg = flow_segments.time_segment(0,mod_time, time_step)

    for f in flow_profiles:
        ext1 = flow_segments.unmod_flow(flat_seg, direct_flows[f])
        ext2 = flow_segments.sine_wave_flow(period, amplitudes[f], phases[f], direct_flows[f], mod_seg)

        flow_profiles[f] = helper_functions.extend_flow_profile(flow_profiles[f],ext1)
        flow_profiles[f] = helper_functions.extend_flow_profile(flow_profiles[f],ext2)

    run_time = helper_functions.extend_flow_profile(run_time, flat_seg)
    run_time = helper_functions.extend_flow_profile(run_time, mod_seg)


flow_time = flow_segments.time_segment(0,len(run_time)*time_step, 2)

for s in syringes:
    s.add_flow_profile(flow_time, flow_profiles[s.name])

Experiment = Classes.Flow_Experiment(Exp_name, reactor_vol, flow_unit, syringe_set = syringes)

helper_functions.change_dir(Exp_name)
'''Write flow profiles to files'''
Experiment.write_flow_profile()
Experiment.write_conditions_file()
Experiment.plot_profiles()
