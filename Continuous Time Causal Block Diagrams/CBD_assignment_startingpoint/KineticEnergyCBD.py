#!/usr/bin/env python
from bokeh.plotting import figure, output_file, show
from CBDMultipleOutput.Source.CBD import *
from CBDMultipleOutput.Source.CBDDraw import draw


class Counter(CBD):
    def __init__(self, block_name):
        CBD.__init__(self,
                     block_name,
                     input_ports=[],
                     output_ports=["OutCount"])

        self.addBlock(DelayBlock(block_name="delay"))
        self.addBlock(AdderBlock(block_name="sum"))
        self.addBlock(ConstantBlock(block_name="zero", value=0.0))
        self.addBlock(ConstantBlock(block_name="one", value=1.0))

        self.addConnection("zero", "delay",
                           input_port_name="IC")
        self.addConnection("delay", "OutCount")
        self.addConnection("delay", "sum")
        self.addConnection("sum", "delay", input_port_name="IN1")
        self.addConnection("one", "sum")


class Multiplication(CBD):
    def __init__(self, block_name):
        CBD.__init__(self,
                     block_name,
                     input_ports=["InNumber"],
                     output_ports=["OutMult"])
        self.addBlock(ProductBlock(block_name="mult1"))
        self.addBlock(ProductBlock(block_name="mult2"))
        self.addBlock(ConstantBlock(block_name="mass", value=1.0))
        self.addBlock(AdderBlock(block_name="adder"))
        self.addBlock(NegatorBlock(block_name="negator"))

        self.addConnection("InNumber", "mult1")
        self.addConnection("mass", "mult1")
        self.addConnection("mult1", "mult2")
        self.addConnection("InNumber", "mult2")
        self.addConnection("mult2", "adder")
        self.addConnection("adder", "negator")
        self.addConnection("negator", "adder")
        self.addConnection("adder", "OutMult")


class KineticEnergyCalculator(CBD):
    def __init__(self, block_name):
        CBD.__init__(self,
                     block_name,
                     input_ports=[],
                     output_ports=["OutEnergy"])

        self.addBlock(Counter(block_name="counter"))
        self.addBlock(Multiplication(block_name="multiplication"))

        self.addConnection("counter", "multiplication",
                           input_port_name="InNumber",
                           output_port_name="OutCount")
        self.addConnection("multiplication", "OutEnergy",
                           output_port_name="OutMult")


cbd = KineticEnergyCalculator("number_gen")
draw(cbd, "number_gen.dot")
draw(cbd.getBlockByName("counter"), "counter.dot")
cbd.run(10)

times = []
output = []

for timeValuePair in cbd.getSignal("OutEnergy"):
    times.append(timeValuePair.time)
    output.append(timeValuePair.value)

# Plot
output_file("./number_gen.html", title="Kinetic Energy Calculations")
p = figure(title="Even Numbers", x_axis_label='time', y_axis_label='N')
p.circle(x=times, y=output, legend="Kinetic Energy Values")
show(p)




