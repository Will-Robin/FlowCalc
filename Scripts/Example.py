import os
import numpy as np

from FlowCalc import Classes
from FlowCalc import Loading

# Create an experiment from a configuration file.
# Either .csv or .toml formats can be used.
_ = Loading.experiment_from_csv('config.csv')
experiment = Loading.experiment_from_toml('config.toml')

# Create a syringe object to contain information.
syringe = Classes.Syringe('dihydroxyacetone')

# Set some values and units to use in process below.
# Units are important.
time_step = 2
time_unit = "s"

flow_rate = 1000
flow_units = "μL/h"

# Design flow profiles using numpy
time_axis = np.arange(0,100,time_step)

flow_rates = np.full(time_axis.shape, flow_rate)

# Set the properties of the syringe
syringe.set_concentration(0.1, "M")

syringe.set_flow_profile(time_axis, time_unit, flow_rates, flow_units)

# Add the syringe to the experiment
experiment.add_syringe(syringe)

# Write flow profiles to files
experiment.write_flow_profile('ExampleOutput')

conditions_filename = f"ExampleOutput/{experiment.name}_conditions.csv"
experiment.write_conditions_file(conditions_filename)
experiment.write_toml("ExampleOutput/test.toml")

