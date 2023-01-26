import tomli
from FlowCalc import Classes
from FlowCalc.Planner import plan_experiment


def experiment_from_toml(filename):
    """
    Initialise a flow experiment from a .toml file.

    Parameters
    ----------
    filename: str
        Name of a formatted configuration file.

    Returns
    -------
    experiment: Classes.FlowExperiment
    """

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    config_dict = tomli.loads(text)

    experiment = plan_experiment(config_dict)

    return experiment
