import tomli
from FlowCalc import Classes
from FlowCalc.Classes import FlowExperiment


def experiment_from_toml(filename: str) -> FlowExperiment:
    """
    Initialise a flow experiment from a .toml file.

    Parameters
    ----------
    filename: str
        Name of a formatted configuration file.

    Returns
    -------
    experiment: FlowExperiment
    """

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    config_dict = tomli.loads(text)

    experiment = Classes.FlowExperiment(config_dict["Exp_code"])

    reactor_vol = config_dict["Reactor_volume"][0]
    reactor_unit = config_dict["Reactor_volume"][1]

    experiment.reactor_volume = float(reactor_vol)
    experiment.reactor_volume_unit = reactor_unit

    return experiment
