import numpy as np

# A dictionary of lambda functions used to convert flow
# profile units into SI units.
SI_conversions = {

    "L/s": (lambda x: x, "L/s"),
    "l/s": (lambda x: x, "L/s"),

    "µl/h": (lambda x: x / (360 * 1e6), "L/s"),
    "µL/h": (lambda x: x / (360 * 1e6), "L/s"),
    "μl/h": (lambda x: x / (360 * 1e6), "L/s"),
    "μL/h": (lambda x: x / (360 * 1e6), "L/s"),

    "µl/min": (lambda x: x / (60 * 1e6), "L/s"),
    "µL/min": (lambda x: x / (60 * 1e6), "L/s"),
    "μl/min": (lambda x: x / (60 * 1e6), "L/s"),
    "µL/min": (lambda x: x / (60 * 1e6), "L/s"),

    "µl/s": (lambda x: x / 10e6, "L/s"),
    "µL/s": (lambda x: x / 10e6, "L/s"),

    "ml/h": (lambda x: x / (360 * 1e3), "L/s"),
    "mL/h": (lambda x: x / (360 * 1e3), "L/s"),

    "ml/min": (lambda x: x / (60 * 1e3), "L/s"),
    "mL/min": (lambda x: x / (60 * 1e3), "L/s"),

    "ml/s": (lambda x: x / 10e3, "L/s"),
    "mL/s": (lambda x: x / 10e3, "L/s"),

    "l/h": (lambda x: x / 360, "L/s"),
    "L/h": (lambda x: x / 360, "L/s"),

    "l/min": (lambda x: x / 60, "L/s"),
    "L/min": (lambda x: x / 60, "L/s"),

    "l/s": (lambda x: x, "L/s"),
    "L/s": (lambda x: x, "L/s"),

    "µl": (lambda x: x / 1e6, "L"),
    "µL": (lambda x: x / 1e6, "L"),

    "ml": (lambda x: x / 1e3, "L"),
    "mL": (lambda x: x / 1e3, "L"),

    "s": (lambda x: x, "s"),
    "h": (lambda x: x * 60, "s"),

    "rad": (lambda x: x, "rad"),
    "degrees": (lambda x: x * np.pi / 180, "rad"),

    "M": (lambda x: x, "M"),
    "mM": (lambda x: x / 1e3, "M"),

    "μM": (lambda x: x / 1e6, "M"),
    "µM": (lambda x: x / 1e6, "M"),

    "uM": (lambda x: x / 1e6, "M"),
    "nM": (lambda x: x / 1e9, "M"),
}
