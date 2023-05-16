import numpy as np
from FlowCalc.Classes import FlowExperiment
from FlowCalc.Utils.conversions import SI_conversions


def write_flow_experiment_conditions_file(
    flow_experiment: FlowExperiment, filename: str
) -> None:
    """
    Output draft conditions file

    Parameters
    ----------
    filename: str
        Name for the output file.

    Output
    ------
    None
    """

    # Write text
    text = f"Dataset,{flow_experiment.name}\n"
    text += "start_experiment_information\n"
    text += "series_values,#NOT PROVIDED\n"

    text += "start_conditions\n"
    vol = flow_experiment.reactor_volume
    vol_unit = flow_experiment.reactor_volume_unit
    text += f"reactor_volume/ {vol_unit},{vol}\n"

    for s in flow_experiment.syringes:
        syr_name = flow_experiment.syringes[s].name
        conc_unit = flow_experiment.syringes[s].conc_unit
        concentration = flow_experiment.syringes[s].concentration
        text += f"{syr_name}/ {conc_unit},{concentration}\n"

    a_syringe = flow_experiment.syringes[list(flow_experiment.syringes)[-1]]
    text += "flow_profile_time/ s,"

    # The following writes a shared time axis for all of the flow profiles.
    # Thus, it is assumed that all of the flow profiles share the same time
    # axis.
    time_conversion_func = SI_conversions[a_syringe.time_unit][0]
    for x in a_syringe.time:
        si_time = time_conversion_func(x)
        text += f"{si_time},"

    text += "\n"

    tot_flow = np.zeros(len(a_syringe.time))

    for s in flow_experiment.syringes:
        flow_unit_si = SI_conversions[flow_experiment.syringes[s].flow_unit][1]
        text += f"{s}_flow/ {flow_unit_si},"

        flow_conversion_func = SI_conversions[flow_experiment.syringes[s].flow_unit][0]

        for x in flow_experiment.syringes[s].flow_profile:
            si_flow = flow_conversion_func(x)
            text += f"{si_flow},"

        text += "\n"

        tot_flow = tot_flow + flow_conversion_func(
            flow_experiment.syringes[s].flow_profile
        )

    # Convert residence time to seconds
    reactor_conversion = SI_conversions[flow_experiment.reactor_volume_unit][0]
    residence_time = reactor_conversion(flow_experiment.reactor_volume) / tot_flow

    text += "Residence time/ s,"

    for r in residence_time:
        text += f"{r},"

    text += "\n"

    text += "end_conditions\n"

    # Write text to file.
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
