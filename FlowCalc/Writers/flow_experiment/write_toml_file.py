import tomli_w
from .to_dict import flow_experiment_to_dict
from FlowCalc.Classes import FlowExperiment


def write_flow_experiment_toml_file(
    flow_experiment: FlowExperiment, filename: str
) -> None:
    conditions_dict = flow_experiment_to_dict(flow_experiment)

    toml_string = tomli_w.dumps(conditions_dict)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(toml_string)
