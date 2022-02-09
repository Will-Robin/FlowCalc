# A dictionary of lambda functions used to convert flow
# profile units into SI units.
SI_conversions = {
                    "µl/h"   : (lambda x: x/(360*10e6), "L/s"),
                    "µl/min" : (lambda x: x/(60*10e6), "L/s"),
                    "µl/s"   : (lambda x: x/10e6, "L/s"),

                    "ml/h"   : (lambda x: x/(360*10e3), "L/s"),
                    "ml/min" : (lambda x: x/(60*10e3), "L/s"),
                    "ml/s"   : (lambda x: x/10e3, "L/s"),

                    "l/h"    : (lambda x: x/360, "L/s"),
                    "l/min"  : (lambda x: x/60, "L/s"),
                    "l/s"    : (lambda x: x, "L/s"),
                    "h"      : (60, "s"),
                    "degrees": (np.pi/180, "rad"),
                    "uL/h"   : ((10e-6)/(60*60), "L/s"),
                    "uM"     : (10e-6, "M")
                 }
