import sys
import numpy as np
from FlowCalc.Classes import Syringe
from FlowCalc.Utils.conversions import SI_conversions


def syringe_to_nfp(syringe: Syringe, filename: str) -> None:
    """ """

    number_of_cycles = 1
    valve_val = 255

    # Get timesteps for the syringe.
    syringe.calculate_timesteps()

    syr_time_steps = syringe.timesteps

    time_unit = syringe.time_unit

    if time_unit in SI_conversions:
        conversion_to_s = SI_conversions[time_unit][0]
        time_steps_in_s = conversion_to_s(syr_time_steps)
    else:
        syr_name = syringe.name
        sys.exit(
            f"""Syringe {syr_name}: Please provide the units for
                the flow profile time axis, or check if there is a
                conversion available in Flowcalc.conversions"""
        )

    # Convert time steps to ms
    time_steps_in_ms = np.round(time_steps_in_s, 1) * 1000

    # Build output text
    text = ""
    text += f"{syringe.flow_unit.replace("L","l")}\n" # Cetoni software denotes L as l.
    text += f"{number_of_cycles}\n"

    for x in range(0, len(syringe.flow_profile)):
        flow_val = syringe.flow_profile[x]
        time_step = time_steps_in_ms[x]
        text += f"{time_step}\t {flow_val}\t{valve_val}\n"

    # Write to file
    with open(filename, "w", encoding="cp1252") as file:
        file.write(text)
