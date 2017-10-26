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
        
class Double(CBD):        
    def __init__(self, block_name):
        CBD.__init__(self, 
                     block_name, 
                     input_ports=["InNumber"], 
                     output_ports=["OutDouble"])
        self.addBlock(ProductBlock(block_name="mult"))
        self.addBlock(ConstantBlock(block_name="two", value=2.0))
        
        self.addConnection("InNumber", "mult")
        self.addConnection("two", "mult")
        self.addConnection("mult", "OutDouble")
    
    
class EvenNumberGen(CBD):
    def __init__(self, block_name):
        CBD.__init__(self, 
                     block_name, 
                     input_ports=[],
                     output_ports=["OutEven"])
        
        self.addBlock(Counter(block_name="counter"))
        self.addBlock(Double(block_name="double"))
        
        self.addConnection("counter", "double", 
                           input_port_name="InNumber",
                           output_port_name="OutCount")
        self.addConnection("double", "OutEven",
                           output_port_name="OutDouble")
        



cbd = EvenNumberGen("number_gen")
draw(cbd, "number_gen.dot")
draw(cbd.getBlockByName("counter"), "counter.dot")
cbd.run(10)

times = []
output = []

for timeValuePair in cbd.getSignal("OutEven"):
    times.append(timeValuePair.time)
    output.append(timeValuePair.value)
            
#Plot
output_file("./number_gen.html", title="Even Numbers")
p = figure(title="Even Numbers", x_axis_label='time', y_axis_label='N')
p.circle(x=times, y=output, legend="Even numbers")
show(p)




