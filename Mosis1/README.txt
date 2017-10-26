Files UseCase3 and UseCase4 contain the sources for usecase3 and usecase4 respectively.

To run the fsa's run UseCase*Scanner.py with python. (* is 3 or 4)

Each of the folders contain the given trace, aswell as a trace that shows the opposite reaction (violation if trace is correct, correct if trace is violation).
For UseCase3 this is the FaultiveTrace file.
For UseCase4 this is the traceCorrect file.

To switch between the two files, you have to edit the UseCase*Scanner.py files.
The main-function can be found at the bottom of each file. 
You will notice that there is a fileopen with the trace, and a commented fileopen with the opposite trace.
These lines of code can be swapped to run the other tracefile.
