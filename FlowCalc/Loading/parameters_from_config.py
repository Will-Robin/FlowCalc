

def parameters_from_config_file(fname, SI_units=False):
    """
    Get experiment configuration from a standard format .csv file.

    Parameters
    ----------
    fname: str
        File name or path to file with file name appended.
    SI_units: bool
        True: converts units in spreadsheet to SI using SI_convert()
        False: Reads in values as given in spreadsheet.

    Returns
    -------
    name: str
        Experiment name as given in file.
    params:
        Dictionary of dictionaries for parameters. {Section: {param: value}}
    """

    lineproc = lambda x: x.strip("\n").split(",")
    params = {}
    readstate = False
    with open(fname, "r") as f:
        lines = []
        for line in f:
            if "Experiment name" in line:
                name = lineproc(line)[1]
            if "Section" in line:
                ins = lineproc(line)
                clef = ins[0]
                params[clef] = {}
                section_header = ins[1:]
                readstate = True
                line = next(f)
            if readstate:
                ins = lineproc(line)
                if SI_units:
                    params[clef][ins[0]] = {
                        k: v
                        for k, v in (
                            helper_functions.SI_convert(x, y)
                            for x, y in zip(section_header, ins[1:])
                        )
                    }
                else:
                    params[clef][ins[0]] = {
                        k: float(v) for k, v in zip(section_header, ins[1:])
                    }

    return name, params
