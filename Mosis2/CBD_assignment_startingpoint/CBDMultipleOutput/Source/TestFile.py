from CBD import *

class Counter(CBD):
  def __init__(self, block_name):
    CBD.__init__(self,
                 block_name,
                 input_ports=[],
                 output_ports=["OutCount"])

    self.addBlock(InverterBlock(block_name="sum"))
    self.addBlock(ConstantBlock(block_name="zero", value=5.0))

    self.addConnection("zero", "sum")


inventer = InverterBlock(block_name="sum")
constant = ConstantBlock(block_name="zero", value=5.0)

inventer.linkInput(constant, None, None)
inventer.compute(0)


