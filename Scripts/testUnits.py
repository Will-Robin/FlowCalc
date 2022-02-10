from FlowCalc.helper_functions import SI_convert

example_strings = [
                    "concentration/ mM",
                    "concentration/mM",
                    "concentration (mM)",
                    "concentration(mM)",
                    "concentration [mM]",
                    "concentration[mM]"
                ]

for example in example_strings:
    results = SI_convert(example, 1.0)
    assert results[0] == "mM"
    assert results[1] == 1.0
