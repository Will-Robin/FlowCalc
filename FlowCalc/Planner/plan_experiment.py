from FlowCalc.Classes import FlowExperiment
from FlowCalc.Classes import Syringe
from FlowCalc.Utils import conversions


def plan_experiment(config_dict):
    """
    Create an experiment using a configuration dict.

    Parameters
    ----------
    config_dict: dict

    Returns
    -------
    experiment: FlowExperiment
    """

    experiment = FlowExperiment(config_dict["exp_code"])

    if "reactor_volume" in config_dict:
        reactor_vol = config_dict["reactor_volume"][0]
        reactor_unit = config_dict["reactor_volume"][1]

    reactor_vol = load_condition(config_dict, "reactor_volume")
    if reactor_vol != None:
        experiment.reactor_volume = reactor_vol[0]
        experiment.reactor_volume_unit = reactor_vol[1]
    else:
        print(f"'reactor_volume' not found in experiment configuration.")

    temperature = load_condition(config_dict, "temperature")
    if temperature != None:
        experiment.temperature = temperature[0]
        experiment.temperature_unit = temperature[1]
    else:
        print(f"'temperature' not found in experiment configuration.")

    for s in config_dict["sections"]:
        experiment = update_experiment(experiment, config_dict["sections"][s])

    return experiment


def load_condition(config, name):
    """
    Load an experimental condition from a config dictionary.

    Parameters
    ----------
    config: dict
    name: str
        Key in config

    Returns
    -------
    value, unit
    or none if the key is not in the dictionary.
    """

    field = config.get(name)
    if field:
        if len(field) == 2:
            val_unit = conversions.field_to_SI(field)
            return val_unit[0], val_unit[1]

    return None

"""
[sections.condition_2]
[sections.condition_2.formaldehyde]
concentration = [0.1, "M"]
type = "flat"
[sections.condition_2.CaCl2]
concentration = [0.015, "M"]
type = "flat"
[sections.condition_2.NaOH]
concentration = [0.03, "M"]
type = "flat"
[condition_2.dihydroxyacetone]
concentration = [0.05, "M"]
type = "flat"
"""

def update_experiment(experiment, config, time, increment):
    """
    Update an experiment with the condition contained in config.

    Parameters
    ----------
    experiment: FlowExperiment
    config: dict

    Returns
    -------
    experiment: FlowExperiment
    """

    # default to 1 minute if time not given
    time_period = config.get("time", 60)

    for syringe in set(config) - {"time"}:
        conc = load_condition(config, "concentration")

        new_syringe = create_syringe(syringe, config[syringe], time, increment)

        if experiment.syringes.get(syringe):
            experiment.syringes[new_syringe].update_syringe()
        else:
            experiment.add_syringe(new_syringe)
        else:
            print()

    return experiment

def create_syringe(name, config, time_period, increment):
    """
    Create a syringe from a config.

    Parameters
    ----------
    name: str
    config: dict

    Returns
    -------
    syringe: Syringe

    """

    syringe = Syringe(name)

    # Default to 0 M
    conc = config.get("concentration", [0.0, "M"]) # Deafult to 0 M
    conc_standard = load_condition(conc)
    syringe.set_concentration(conc_standard[0], conc_standard[1])

    dynamic = config.get("type", "flat")
    if dynamic == "flat":
        time = np.arange(0, time_period, increment)
        # default flow rate is 0.0
        flow_profile = np.full(time.shape, config.get("flow_rate", 0.0))
        syringe.set_flow_profile(time, "s", flow_profile, "L/s")

    else:
        print(f"""{dynamic} not implemented as a flow profile type
              (Syringe {name}).""")

    return None

