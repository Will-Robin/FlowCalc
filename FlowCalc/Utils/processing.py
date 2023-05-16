import numpy as np
from copy import deepcopy
from FlowCalc.Classes import FlowExperiment


def minimise_steps(flow_experiment: FlowExperiment) -> FlowExperiment:
    """
    Truncate flow profiles based on where flow profiles change.
    Returns a modified copy of the experiment.

    Parameters
    ----------
    flow_experiment: FlowExperiment

    Returns
    -------
    experiment: FlowExperiment
    """
    experiment = deepcopy(flow_experiment)

    delta_positions = np.array([], dtype=int)
    for s in experiment.syringes:
        syringe = experiment.syringes.get(s)
        changes = np.hstack(([1.0], np.diff(syringe.flow_profile)))
        delta_idx = np.where((changes > 0) | (changes < 0))[0]
        if len(delta_idx) == 0:
            delta_idx = [0]
        delta_positions = np.hstack((delta_positions, delta_idx))

    retain_idx = np.sort(np.unique(delta_positions))

    # ensure the final timestep is included
    retain_idx = np.hstack((retain_idx, [-1]))

    for s in experiment.syringes:
        syringe = experiment.syringes.get(s)
        syringe.time = syringe.time[retain_idx]
        syringe.flow_profile = syringe.flow_profile[retain_idx]
        syringe.calculate_timesteps()

    return experiment
