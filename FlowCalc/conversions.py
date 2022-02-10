import numpy as np
# A dictionary of lambda functions used to convert flow
# profile units into SI units.
SI_conversions = {
                    "L/s"    : (lambda x: x, "L/s"),
                    "µl/h"   : (lambda x: x/(360*1e6), "L/s"),
                    "µl/min" : (lambda x: x/(60*1e6), "L/s"),
                    "µl/s"   : (lambda x: x/10e6, "L/s"),

                    "ml/h"   : (lambda x: x/(360*1e3), "L/s"),
                    "ml/min" : (lambda x: x/(60*1e3), "L/s"),
                    "ml/s"   : (lambda x: x/10e3, "L/s"),

                    "l/h"    : (lambda x: x/360, "L/s"),
                    "l/min"  : (lambda x: x/60, "L/s"),
                    "l/s"    : (lambda x: x, "L/s"),

                    "s"      : (lambda x: x, "s"),
                    "h"      : (lambda x: x*60, "s"),

                    "rad"    : (lambda x: x, "rad"),
                    "degrees": (lambda x: x*np.pi/180, "rad"),

                    "M"      : (lambda x: x, "M"),
                    "mM"     : (lambda x: x*1e-3, "M"),
                    "μM"     : (lambda x: x*1e-6, "M"),
                    "uM"     : (lambda x: x*1e-6, "M"),
                    "nM"     : (lambda x: x*1e-9, "M")
                 }
