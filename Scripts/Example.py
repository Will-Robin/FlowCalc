import os
import numpy as np
from FlowCalc.Classes import Syringe
from FlowCalc.Classes import FlowExperiment
from FlowCalc.Utils import processing
from FlowCalc.Writers import flow_experiment_to_csv
from FlowCalc.Writers import flow_experiment_to_labm8
from FlowCalc.Writers import write_flow_experiment_conditions_file
from FlowCalc.Writers import syringe_to_nfp

experiment = FlowExperiment("example")
experiment.reactor_volume = 411
experiment.reactor_volume_unit = "µL"

# Set some values and units to use in process below.
# Units are important.
time_step = 2
time_unit = "s"

flow_rate = 1000
flow_units = "µL/h"

# Design flow profiles using numpy
time_axis = np.arange(0, 100, time_step)

flow_rates = np.full(time_axis.shape, flow_rate)

# Create a syringe object, set its properties and add it
syringe_1 = Syringe("dihydroxyacetone")
syringe_1.set_concentration(0.1, "M")
syringe_1.set_flow_profile(time_axis, time_unit, flow_rates, flow_units)
experiment.add_syringe(syringe_1)

syringe_2 = Syringe("formaldehyde")
syringe_2.set_concentration(0.5, "M")
syringe_2.set_flow_profile(time_axis, time_unit, flow_rates, flow_units)
experiment.add_syringe(syringe_2)

# Minimise the number of flow steps in the experiment
processing.minimise_steps(experiment)

conditions_filename = f"ExampleOutput/{experiment.name}_conditions.csv"
write_flow_experiment_conditions_file(experiment, conditions_filename)

flow_experiment_to_csv(experiment, "ExampleOutput/test.csv")
flow_experiment_to_labm8(experiment, "ExampleOutput/test.csv")

for s in experiment.syringes:
    syringe_to_nfp(experiment.syringes[s], f"ExampleOutput/{s}_flow_profile.nfp")
