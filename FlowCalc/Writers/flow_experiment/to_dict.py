from FlowCalc.Classes import FlowExperiment
from FlowCalc.Utils.conversions import SI_conversions


def flow_experiment_to_dict(flow_experiment: FlowExperiment) -> dict[str, list[float]]:
    """
    conditions_dict: dict
    """

    conditions_dict = {}

    # Write text
    conditions_dict["Dataset"] = flow_experiment.name
    conditions_dict["Series_values"] = flow_experiment.series_values
    conditions_dict["Series_unit"] = flow_experiment.series_unit

    conditions_dict["conditions"] = {}

    conditions_dict["conditions"]["Reactor_volume"] = [
        flow_experiment.reactor_volume,
        flow_experiment.reactor_volume_unit,
    ]

    for s in flow_experiment.syringes:
        syr_name = flow_experiment.syringes[s].name
        conc_unit = flow_experiment.syringes[s].conc_unit
        concentration = flow_experiment.syringes[s].concentration
        conditions_dict["conditions"][syr_name] = [concentration, conc_unit]

    # The following writes a shared time axis for all of the flow profiles.
    # Thus, it is assumed that all of the flow profiles share the same time
    # axis.
    a_syringe = flow_experiment.syringes[list(flow_experiment.syringes)[-1]]

    time_conversion = SI_conversions[a_syringe.time_unit]
    time = time_conversion[0](a_syringe.time).tolist()

    conditions_dict["conditions"]["flow_profile_time"] = [time, time_conversion[1]]

    tot_flow = np.zeros(len(a_syringe.time))

    for s in flow_experiment.syringes:
        flow_conversion = SI_conversions[flow_experiment.syringes[s].flow_unit]

        flow_si = flow_conversion[0](flow_experiment.syringes[s].flow_profile).tolist()
        flow_unit = flow_conversion[1]

        conditions_dict["conditions"][f"{s}_flow_profile"] = [flow_si, flow_unit]

        tot_flow = tot_flow + flow_si

    # Convert residence time to seconds
    reactor_conversion = SI_conversions[flow_experiment.reactor_volume_unit]
    residence_time = reactor_conversion[0](flow_experiment.reactor_volume) / tot_flow
    res_time = residence_time.tolist()

    conditions_dict["conditions"]["Residence time"] = [
        res_time,
        time_conversion[1],
    ]

    return conditions_dict
