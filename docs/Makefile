CLASSES = ../FlowCalc/Classes.py
CONV = ../FlowCalc/conversions.py
FLOW = ../FlowCalc/flow_segments.py
HELPERS = ../FlowCalc/helper_functions.py
LOADERS = ../FlowCalc/loaders.py

FLOWCALC=$(CLASSES) $(CONV) $(FLOW) $(HELPERS) $(LOADERS)

all: index.html

index.html: $(FLOWCALC)
	pdoc ../FlowCalc -d "numpy" -o ./
