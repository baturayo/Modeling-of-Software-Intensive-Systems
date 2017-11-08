#!/usr/bin/env python
from bokeh.plotting import figure, output_file, show
from CBDMultipleOutput.Source.CBD import *
from CBDMultipleOutput.Source.CBDDraw import draw


class SinusBlock(CBD):
    def __init__(self, block_name):
        CBD.__init__(self,
                     block_name,
                     input_ports=["IN1"],
                     output_ports=["OutSinus"])
        self.addBlock(GenericBlock(block_name="sinCalc", block_operator="sin"))

        self.addConnection("IN1", "sinCalc")
        self.addConnection("sinCalc", "OutSinus")

class HarmonicOscillatorIntegralBlock(CBD):
    def __init__(self, block_name):
        CBD.__init__(self,
                     block_name,
                     input_ports=["IN1"],
                     output_ports=["OutIntegral"])

        # First Integral
        self.addBlock(IntegratorBlock(block_name="int1"))
        self.addBlock(ConstantBlock(block_name="IC1", value=1.0))

        # Second Integral
        self.addBlock(IntegratorBlock(block_name="int2"))
        self.addBlock(ConstantBlock(block_name="IC2", value=0.0))

        # Negator
        self.addBlock(NegatorBlock(block_name="nega"))

        self.addConnection("IN1", "int1", input_port_name="delta_t")
        self.addConnection("IC1", "int1", input_port_name="IC")
        self.addConnection("IN1", "int2", input_port_name="delta_t")
        self.addConnection("IC2", "int2", input_port_name="IC")
        self.addConnection("int1", "int2")
        self.addConnection("int2", "nega")
        self.addConnection("nega", "int1")
        self.addConnection("int2", "OutIntegral")

class HarmonicOscillatorDerivativeBlock(CBD):
    def __init__(self, block_name):
        CBD.__init__(self,
                     block_name,
                     input_ports=["IN1"],
                     output_ports=["OutDerivative"])

        # First Derivative
        self.addBlock(DerivatorBlock(block_name="der1"))
        self.addBlock(ConstantBlock(block_name="IC1", value=1.0))

        # Second Derivative
        self.addBlock(DerivatorBlock(block_name="der2"))
        self.addBlock(ConstantBlock(block_name="IC2", value=0.0))

        # Negator
        self.addBlock(NegatorBlock(block_name="nega"))

        self.addConnection("IN1", "der1", input_port_name="delta_t")
        self.addConnection("IC1", "der1", input_port_name="IC")
        self.addConnection("IN1", "der2", input_port_name="delta_t")
        self.addConnection("IC2", "der2", input_port_name="IC")
        self.addConnection("der1", "der2")
        self.addConnection("der2", "nega")
        self.addConnection("nega", "der1")
        self.addConnection("nega", "OutDerivative")

class HOIntegralErrorBlock(CBD):
    def __init__(self, block_name):
        CBD.__init__(self,
                     block_name,
                     input_ports=[],
                     output_ports=["OutError"])

        # Integrator
        self.addBlock(IntegratorBlock(block_name="int"))
        self.addBlock(ConstantBlock(block_name="IC1", value=0.0))

        # Sinus
        self.addBlock(SinusBlock(block_name="sin"))

        # Adder
        self.addBlock(AdderBlock(block_name="sum"))

        self.addBlock(ConstantBlock(block_name="delta_t", value=0.1))
        self.addBlock(ProductBlock(block_name="mult"))

        # Harmonic Oscillator Integral Approx
        self.addBlock(HarmonicOscillatorIntegralBlock(block_name="hoApprox"))

        # Negator
        self.addBlock(NegatorBlock(block_name="nega"))

        # Time
        self.addBlock(TimeBlock(block_name="time"))

        # Absolute Value
        self.addBlock(AbsoluteBlock(block_name="abs"))


        # self.addConnection("delta_t", "int", input_port_name="delta_t")
        # self.addConnection("IC1", "int", input_port_name="IC")
        self.addConnection("time", "mult")
        self.addConnection("delta_t", "mult")
        self.addConnection("mult", "sin")
        self.addConnection("sin", "sum", output_port_name="OutSinus")
        self.addConnection("delta_t", "hoApprox")
        self.addConnection("hoApprox", "nega", output_port_name="OutIntegral")
        self.addConnection("nega", "sum")
        self.addConnection("sum", "abs")
        self.addConnection("abs", "int")
        self.addConnection("delta_t", "int", input_port_name="delta_t")
        self.addConnection("IC1", "int", input_port_name="IC")
        self.addConnection("int", "OutError")

class HODerivativeErrorBlock(CBD):
    def __init__(self, block_name):
        CBD.__init__(self,
                     block_name,
                     input_ports=[],
                     output_ports=["OutError"])

        # Integrator
        self.addBlock(IntegratorBlock(block_name="int"))
        self.addBlock(ConstantBlock(block_name="IC1", value=0.0))

        # Sinus
        self.addBlock(SinusBlock(block_name="sin"))

        # Adder
        self.addBlock(AdderBlock(block_name="sum"))

        # Delta_t
        self.addBlock(ConstantBlock(block_name="delta_t", value=0.001))

        # Product for Sinus Time
        self.addBlock(ProductBlock(block_name="mult"))

        # Harmonic Oscillator Derivative Approx
        self.addBlock(HarmonicOscillatorDerivativeBlock(block_name="hoApprox"))

        # Negator
        self.addBlock(NegatorBlock(block_name="nega"))

        # Time
        self.addBlock(TimeBlock(block_name="time"))

        # Absolute Value
        self.addBlock(AbsoluteBlock(block_name="abs"))

        self.addConnection("time", "mult")
        self.addConnection("delta_t", "mult")
        self.addConnection("mult", "sin")
        self.addConnection("sin", "sum", output_port_name="OutSinus")
        self.addConnection("delta_t", "hoApprox")
        self.addConnection("hoApprox", "nega", output_port_name="OutDerivative")
        self.addConnection("nega", "sum")
        self.addConnection("sum", "abs")
        self.addConnection("abs", "int")
        self.addConnection("delta_t", "int", input_port_name="delta_t")
        self.addConnection("IC1", "int", input_port_name="IC")
        self.addConnection("int", "OutError")

class HOIntegralTest(CBD):
    def __init__(self, block_name):
        CBD.__init__(self,
                     block_name,
                     input_ports=[],
                     output_ports=["OutTest"])

        # Harmonic Oscillator Integral Approx
        self.addBlock(HarmonicOscillatorIntegralBlock(block_name="hoApprox"))

        # Delta T
        self.addBlock(ConstantBlock(block_name="time", value=0.001))

        self.addConnection("time", "hoApprox")
        self.addConnection("hoApprox", "OutTest", output_port_name="OutIntegral")

class HODerivativeTest(CBD):
    def __init__(self, block_name):
        CBD.__init__(self,
                     block_name,
                     input_ports=[],
                     output_ports=["OutTest"])

        # Harmonic Oscillator Integral Approx
        self.addBlock(HarmonicOscillatorDerivativeBlock(block_name="hoApprox"))

        # Delta T
        self.addBlock(ConstantBlock(block_name="time", value=0.01))

        self.addConnection("time", "hoApprox")
        self.addConnection("hoApprox", "OutTest", output_port_name="OutDerivative")

class SinTest(CBD):
    def __init__(self, block_name):
        CBD.__init__(self,
                     block_name,
                     input_ports=[],
                     output_ports=["OutSin"])

        self.addBlock(TimeBlock(block_name="time"))
        self.addBlock(ConstantBlock(block_name="delta_t", value=0.01))
        self.addBlock(ProductBlock(block_name="mult"))
        self.addBlock(SinusBlock(block_name="sin"))

        self.addConnection("time", "mult")
        self.addConnection("delta_t", "mult")
        self.addConnection("mult", "sin")
        self.addConnection("sin", "OutSin", output_port_name="OutSinus")


cbd = HODerivativeErrorBlock("number_gen")
#draw(cbd, "number_gen.dot")
#draw(cbd.getBlockByName("counter"), "counter.dot")
cbd.run(10000, delta_t=1)

times = []
output = []

for timeValuePair in cbd.getSignal("OutError"):
    times.append(timeValuePair.time)
    output.append(timeValuePair.value)



# Plot
output_file("./number_gen.html", title="")
p = figure(title="y", x_axis_label='time', y_axis_label='N')
p.circle(x=times, y=output, legend="")
show(p)
