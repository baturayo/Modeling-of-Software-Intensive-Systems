from CBDMultipleOutput.Source.CBD import *
from CBDMultipleOutput.Source.CBDDraw import draw

class DenotSem:

    def __init__(self):
        self.equations = []  #List of all equations

    def __UniqueName(self, block, port):
        #Calculates a unique name based on the blockname and the port
        return block.getBlockName() + "." + port

    def evalCBD(self, CBD):
        #Goes through each block in the cbd and adds the correct equations for each block
        blocks = CBD.getBlocks();

        for block in blocks:
            #Connect the inputs for this block to the outputs of the previous connected blocks
            for key, value in block.getLinksIn().iteritems():
                outname = self.__UniqueName(value.block, value.output_port)
                inname = self.__UniqueName(block, key)
                self.addConnection(inname, outname)

            if block.getBlockType() == "ConstantBlock":
                outname = self.__UniqueName(block, "OUT1")
                self.addConstant(outname,block.getValue())
            if block.getBlockType() == "NegatorBlock":
                outname = self.__UniqueName(block, "OUT1")
                inname = self.__UniqueName(block, "IN1")
                self.addNegator(inname, outname)
            if block.getBlockType() == "InverterBlock":
                outname = self.__UniqueName(block, "OUT1")
                inname = self.__UniqueName(block, "IN1")
                self.addInverter(inname, outname)
            if block.getBlockType() == "AdderBlock":
                outname = self.__UniqueName(block, "OUT1")
                inname1 = self.__UniqueName(block, "IN1")
                inname2 = self.__UniqueName(block, "IN2")
                self.addAdder(inname1, inname2, outname)
            if block.getBlockType() == "ProductBlock":
                outname = self.__UniqueName(block, "OUT1")
                inname1 = self.__UniqueName(block, "IN1")
                inname2 = self.__UniqueName(block, "IN2")
                self.addProduct(inname1, inname2, outname)
            if block.getBlockType() == "GenericBlock":
                outname = self.__UniqueName(block, "OUT1")
                inname = self.__UniqueName(block, "IN1")
                function = block.getBlockOperator()
                self.addGeneric(inname, outname, function)
            if block.getBlockType() == "RootBlock":
                outname = self.__UniqueName(block, "OUT1")
                inname1 = self.__UniqueName(block, "IN1")
                inname2 = self.__UniqueName(block, "IN2")
                self.addRoot(inname1, inname2, outname)
            if block.getBlockType() == "ModuloBlock":
                outname = self.__UniqueName(block, "OUT1")
                inname1 = self.__UniqueName(block, "IN1")
                inname2 = self.__UniqueName(block, "IN2")
                self.addModulo(inname1, inname2, outname)
            if block.getBlockType() == "DelayBlock":
                outname = self.__UniqueName(block, "OUT1")
                inname1 = self.__UniqueName(block, "IN1")
                inname2 = self.__UniqueName(block, "IN2")
                self.addDelay(inname1, inname2, outname)

    def addConnection(self, fromOutput, toInput):
        #Add a connection (var1 = var2)
        self.equations.append(fromOutput + "^{[s+1]} = " + toInput + "^{[s+1]};")

    def addConstant(self, varName, value):
        self.equations.append(varName + "^{[s+1]} = " + str(value) + ";")

    def addNegator(self, InputOne, OutputOne):
        self.equations.append(OutputOne + "^{[s+1]} = -" + InputOne + "^{[s+1]};")

    def addInverter(self, InputOne, OutputOne):
        self.equations.append(OutputOne + "^{[s+1]} = \dfrac{1}{" + InputOne + "^{[s+1]}};")

    def addAdder(self, InputOne, InputTwo, OutputOne):
        self.equations.append(OutputOne + "^{[s+1]} = " + InputOne + "^{[s+1]} + " + InputTwo + "^{[s+1]};")

    def addProduct(self, InputOne, InputTwo, OutputOne):
        self.equations.append(OutputOne + "^{[s+1]} = " + InputOne + "^{[s+1]} * " + InputTwo + "^{[s+1]};")

    def addGeneric(self, Input, Output, Function):
        self.equations.append(Output + "^{[s+1]} = " + str(Function) + "(" + Input + ")^{[s+1]}")

    def addRoot(self, Value, InversePower, OutputOne):
        self.equations.append(OutputOne + "^{[s+1]} = \sqrt[" + InversePower + "]{"+ Value + "}^{[s+1]};")

    def addModulo(self, Value, Modulo, Output):
        self.equations.append(Output + "^{[s+1]} = " + Value + "^{[s+1]} \% " + Output + "^{[s+1]};")

    def addDelay(self, Input, IC, Output):
        self.equations.append(Output + "^{[s+1]} = " + Input + "^{[s]};")
        self.equations.append(Output + "^{[0]} = " + IC + "^{[s+1]};")

    def writeToLatex(self, outputName):
        #Write the stored equations to a latex file
        file = open(outputName, 'w')
        file.write("\documentclass{article}\n\\usepackage{amsmath}\n\\begin{document}\n")
        for equation in self.equations:
            file.write("\("+equation+"\)\\\\\n")

        file.write("\end{document}")

def createLatex(CBD):
    #Flatten the cbd first
    CBD.flatten()
    semantics = DenotSem()

class LatexExample(CBD):
    def __init__(self, block_name):
        CBD.__init__(self,
                     block_name,
                     input_ports=[],
                     output_ports=[])

        self.addBlock(ConstantBlock(block_name="Constant", value=5))
        self.addBlock(ConstantBlock(block_name="Constant2", value=2))
        self.addBlock(NegatorBlock(block_name="Negator"))
        self.addBlock(InverterBlock(block_name="Inverter"))
        self.addBlock(AdderBlock(block_name="Adder"))
        self.addBlock(ProductBlock(block_name="Product"))
        self.addBlock(GenericBlock(block_name="Generic", block_operator="sin"))
        self.addBlock(RootBlock(block_name="Root"))
        self.addBlock(ModuloBlock(block_name="Modulo"))
        self.addBlock(DelayBlock(block_name="Delay"))

        self.addConnection("Constant", "Negator")
        self.addConnection("Negator", "Inverter")
        self.addConnection("Inverter", "Adder", "IN1")
        self.addConnection("Constant", "Adder", "IN2")
        self.addConnection("Adder", "Product", "IN1")
        self.addConnection("Constant", "Product", "IN2")
        self.addConnection("Product", "Generic")
        self.addConnection("Generic", "Root", "IN1")
        self.addConnection("Constant2", "Root", "IN2")
        self.addConnection("Root", "Modulo", "IN1")
        self.addConnection("Constant", "Modulo", "IN2")



cbd = LatexExample("CBD")
draw(cbd, "number_gen.dot")

semantics = DenotSem()
semantics.evalCBD(cbd)
semantics.writeToLatex("Output.tex")


