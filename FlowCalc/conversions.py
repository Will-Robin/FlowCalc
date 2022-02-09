# A dictionary of lambda functions used to convert flow
# profile units into SI units.
fl_SI_conversions = {"µl/h"   : (lambda x: x/(360*10e6)),
                     "µl/min" : (lambda x: x/(60*10e6)),
                     "µl/s"   : (lambda x: x/10e6),

                     "ml/h"   : (lambda x: x/(360*10e3)),
                     "ml/min" : (lambda x: x/(60*10e3)),
                     "ml/s"   : (lambda x: x/10e3),

                     "l/h"    : (lambda x: x/360),
                     "l/min"  : (lambda x: x/60),
                     "l/s"    : (lambda x: x) }
