import numpy as np
from FlowCalc.Classes import FlowExperiment
from FlowCalc.Utils.conversions import SI_conversions


def to_labm8(experiment, filename):
    """
    Convert an experiment to LabM8 format.

    Parameters
    ----------
    experiment: FlowExperiment
    filename: str

    Returns
    -------
    None

    """

    header = ",".join(["time"] + [*experiment.syringes])
    header = "volume aspired in time period/ µL"
    for s in experiment.syringes:
        header += f",{s}/ μL/min."

    time = np.stack([experiment.syringes[s].time for s in experiment.syringes], axis=0)
    # convert to minutes
    time = time[0] / 60

    data = np.zeros((len(experiment.syringes), len(time)))
    for c, s in enumerate(experiment.syringes):
        syringe = experiment.syringes.get(s)
        flow_unit = syringe.flow_unit
        if flow_unit in SI_conversions:
            si_conv = SI_conversions[flow_unit][0]
            # covert to L/s
            si_flow_profile = si_conv(syringe.flow_profile)
            # convert from L/s to μL/min
            microL_per_min = 1e6 * si_flow_profile * 60
            data[c] = microL_per_min
        else:
            print(f"Flow unit {flow_unit} not found.")

    data = data.T

    # create volume column
    total_volume_aspired = np.zeros(time.shape)
    for x in range(0, len(time) - 1):
        previous_flow_values = data[x]

        time_elapsed = time[x + 1] - time[x]

        total_volume_aspired[x] = previous_flow_values.sum() * time_elapsed

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{header}\n")
        for x in range(0, data.shape[0]):
            f.write(f"{total_volume_aspired[x]}")
            for y in range(0, data.shape[1]):
                f.write(f",{data[x,y]}")
            f.write("\n")
