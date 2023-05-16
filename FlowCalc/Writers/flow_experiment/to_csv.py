import numpy as np
from FlowCalc.Classes import FlowExperiment


def flow_experiment_to_csv(experiment: FlowExperiment, filename: str) -> None:
    """
    Write a simple .csv file of the experiment's syringes.

    Parameters
    ----------
    experiment: FlowExperiment
    filename: str

    Returns
    -------
    None
    """

    header = ",".join(["time"] + [*experiment.syringes])

    time = np.stack([experiment.syringes[s].time for s in experiment.syringes], axis=0)
    data = np.stack(
        [experiment.syringes[s].flow_profile for s in experiment.syringes], axis=0
    )
    time = time.T
    data = data.T

    with open(filename, "w") as f:
        f.write(f"{header}\n")
        for x in range(0, data.shape[0]):
            f.write(f"{time[x,0]}")
            for y in range(0, data.shape[1]):
                f.write(f",{data[x,y]}")
            f.write("\n")
