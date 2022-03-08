from FlowCalc import Classes


def flow_experiment_from_file(filename):
    """
    Initialise a flow experiment from a formatted file.

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

    lines = text.split("\n")

    entries = {}
    for l in lines:
        entry = l.split(",")
        if len(entry) > 1:
            entries[entry[0]] = entry[1]

    experiment = Classes.FlowExperiment(entries["Exp_code"])

    reactor_vol = entries["Reactor_volume"]
    reactor_unit = entries["Reactor_volume_unit"]

    experiment.reactor_volume = float(reactor_vol)
    experiment.reactor_volume_unit = reactor_unit

    return experiment
