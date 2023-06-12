CLASSES = ../FlowCalc/Classes/*.py
LOADING = ../FlowCalc/Loading/*.py
UTILS = ../FlowCalc/Utils/*.py
WRITERS = ../FlowCalc/Writers/*.py

FLOWCALC=$(CLASSES) $(LOADING) $(UTILS) $(WRITERS)

all: index.html

index.html: $(FLOWCALC)
	pdoc ../FlowCalc -d "numpy" -o ./
