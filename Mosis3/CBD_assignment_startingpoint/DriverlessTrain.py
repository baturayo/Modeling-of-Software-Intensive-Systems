from bokeh.plotting import figure, output_file, show
from CBDMultipleOutput.Source.CBD import *
from CBDMultipleOutput.Source.CBDDraw import draw
from CBDMultipleOutput.Source.TrainCostModelBlock import *

class Time(CBD):
    def __init__(self, block_name):
        CBD.__init__(self, block_name, output_ports=["OUT1", "OUTDELTA"])
        self.addBlock(ConstantBlock(block_name="TimeConstant", value=0.1))
        self.addBlock(ConstantBlock(block_name="IC", value=0))
        self.addBlock(DelayBlock(block_name="DelayOne"))
        self.addBlock(AdderBlock("PlusOne"))
        self.addConnection("DelayOne", "PlusOne")
        self.addConnection("TimeConstant", "PlusOne")
        self.addConnection("PlusOne", "DelayOne")
        self.addConnection("IC", "DelayOne", input_port_name="IC")
        self.addConnection("DelayOne", "OUT1")
        self.addConnection("TimeConstant", "OUTDELTA")


class PidController(CBD):
    def __init__(self, block_name, Kp, Ki, Kd):
        CBD.__init__(self, block_name, input_ports=["DeltaV", "DeltaT"], output_ports=["Traction"])
        self.addBlock(ConstantBlock("Kp", value=Kp))
        self.addBlock(ConstantBlock("Ki", value=Ki))
        self.addBlock(ConstantBlock("Kd", value=Kd))
        self.addBlock(ConstantBlock("ZeroBlock", value=0))
        self.addBlock(AdderBlock("FirstSum"))
        self.addBlock(AdderBlock("SecondSum"))
        self.addBlock(ProductBlock("PropProd"))
        self.addBlock(ProductBlock("IntProd"))
        self.addBlock(ProductBlock("DerivProd"))
        self.addBlock(IntegratorBlock("Integrator"))
        self.addBlock(DerivatorBlock("Derivator"))

        #Input to integrator and derivators
        self.addConnection("DeltaT", "Integrator", input_port_name="delta_t")
        self.addConnection("DeltaV", "Integrator", input_port_name="IN1")
        self.addConnection("ZeroBlock", "Integrator", input_port_name="IC")
        self.addConnection("DeltaT", "Derivator", input_port_name="delta_t")
        self.addConnection("DeltaV", "Derivator", input_port_name="IN1")
        self.addConnection("ZeroBlock", "Derivator", input_port_name="IC")
        #Products of constants and parts of pidcontroller
        self.addConnection("Kp", "PropProd")
        self.addConnection("DeltaV", "PropProd")
        self.addConnection("Ki", "IntProd")
        self.addConnection("Integrator", "IntProd")
        self.addConnection("Kd", "DerivProd")
        self.addConnection("Derivator", "DerivProd")
        #Result of products to sum
        self.addConnection("PropProd", "FirstSum")
        self.addConnection("IntProd", "FirstSum")
        self.addConnection("FirstSum", "SecondSum")
        self.addConnection("DerivProd", "SecondSum")
        #Put traction on output
        self.addConnection("SecondSum", "Traction")


class TrainandPerson(CBD):
    def __init__(self, block_name):
        CBD.__init__(self, block_name, input_ports=["Traction", "DeltaT"], output_ports=["VTrain", "XPerson"])
        #Trainpart
        self.addBlock(ConstantBlock("HalfPCdA", value=3.2832))
        self.addBlock(ConstantBlock("MassSum", value=6073.0))
        self.addBlock(ConstantBlock("IC", value=0))
        self.addBlock(InverterBlock("MassSumInv"))
        self.addBlock(NegatorBlock("Negator"))
        self.addBlock(ProductBlock("Squared"))
        self.addBlock(ProductBlock("UVSquared"))
        self.addBlock(ProductBlock("SumDivProd"))
        self.addBlock(AdderBlock("Adder"))
        self.addBlock(IntegratorBlock("Integral"))

        self.addConnection("Integral", "Squared", output_port_name="OUT1")
        self.addConnection("Integral", "Squared", output_port_name="OUT1")
        self.addConnection("Squared", "UVSquared")
        self.addConnection("HalfPCdA", "UVSquared")
        self.addConnection("UVSquared", "Negator")
        self.addConnection("Negator", "Adder")
        self.addConnection("Traction", "Adder")
        self.addConnection("MassSum", "MassSumInv")
        self.addConnection("Adder", "SumDivProd")
        self.addConnection("MassSumInv", "SumDivProd")
        self.addConnection("SumDivProd", "Integral", input_port_name="IN1")
        self.addConnection("IC", "Integral", input_port_name="IC")
        self.addConnection("DeltaT", "Integral", input_port_name="delta_t")
        self.addConnection("Integral", "VTrain")

        #Personpart
        self.addBlock(ConstantBlock("MassDivPassenger", value=73.0/6073.0))
        self.addBlock(ConstantBlock("K", value=300.0))
        self.addBlock(ConstantBlock("C", value=150.0))
        self.addBlock(ConstantBlock("MassPassenger", value=73.0))

        self.addBlock(ProductBlock("KxXpass"))
        self.addBlock(ProductBlock("CxVPassNeg"))
        self.addBlock(ProductBlock("AxTraction"))
        self.addBlock(ProductBlock("TotalDivision"))
        self.addBlock(NegatorBlock("XPassNeg"))
        self.addBlock(NegatorBlock("VPassNeg"))
        self.addBlock(NegatorBlock("AxTractionNeg"))
        self.addBlock(AdderBlock("KXplusCV"))
        self.addBlock(AdderBlock("ResultplusAFtract"))
        self.addBlock(InverterBlock("OneDivMPass"))
        self.addBlock(IntegratorBlock("getVPass"))
        self.addBlock(IntegratorBlock("getXPass"))

        self.addConnection("XPassNeg", "KxXpass")
        self.addConnection("K", "KxXpass")
        self.addConnection("VPassNeg", "CxVPassNeg")
        self.addConnection("C", "CxVPassNeg")
        self.addConnection("Traction", "AxTraction")
        self.addConnection("MassDivPassenger", "AxTraction")
        self.addConnection("AxTraction", "AxTractionNeg")
        self.addConnection("KxXpass", "KXplusCV")
        self.addConnection("CxVPassNeg", "KXplusCV")
        self.addConnection("KXplusCV", "ResultplusAFtract")
        self.addConnection("AxTractionNeg", "ResultplusAFtract")
        self.addConnection("MassPassenger", "OneDivMPass")
        self.addConnection("OneDivMPass", "TotalDivision")
        self.addConnection("ResultplusAFtract", "TotalDivision")
        #Here we have dV or a for the passenger
        self.addConnection("TotalDivision", "getVPass", input_port_name="IN1")
        self.addConnection("DeltaT", "getVPass", input_port_name="delta_t")
        self.addConnection("IC", "getVPass", input_port_name="IC")
        self.addConnection("getVPass", "VPassNeg")
        self.addConnection("getVPass", "getXPass", input_port_name="IN1")
        self.addConnection("DeltaT", "getXPass", input_port_name="delta_t")
        self.addConnection("IC", "getXPass", input_port_name="IC")
        self.addConnection("getXPass", "XPassNeg")
        self.addConnection("getXPass", "XPerson")






class DriverlessTrain(CBD):
    def __init__(self, block_name, Kp=200, Ki=0, Kd=0):
        CBD.__init__(self, block_name, output_ports=["Velocity", "XPerson", "cost"])
        self.addBlock(Time("Timeblock"))
        self.addBlock(ComputerBlock("ComputerBlock"))
        self.addBlock(AdderBlock("SumBlock"))
        self.addBlock(NegatorBlock("NegatorBlock"))
        self.addBlock(PidController("PIDController", Kp, Ki, Kd))
        self.addBlock(TrainandPerson("TrainPerson"))
        self.addBlock(CostFunctionBlock("Cost"))
        self.addConnection("Timeblock", "ComputerBlock", output_port_name="OUT1")
        self.addConnection("ComputerBlock", "SumBlock")
        self.addConnection("NegatorBlock", "SumBlock")
        self.addConnection("SumBlock", "PIDController", input_port_name="DeltaV")
        self.addConnection("Timeblock", "PIDController", input_port_name="DeltaT", output_port_name="OUTDELTA")
        self.addConnection("PIDController", "TrainPerson", input_port_name="Traction", output_port_name="Traction")
        self.addConnection("Timeblock", "TrainPerson", input_port_name="DeltaT", output_port_name="OUTDELTA")
        self.addConnection("TrainPerson", "NegatorBlock", output_port_name="VTrain")
        self.addConnection("TrainPerson", "Velocity", output_port_name="VTrain")
        self.addConnection("TrainPerson", "XPerson", output_port_name="XPerson")

        #Connect blocks to costfunction
        self.addConnection("ComputerBlock", "Cost", input_port_name="InVi")
        self.addConnection("Timeblock", "Cost", input_port_name="InDelta", output_port_name="OUTDELTA")
        self.addConnection("TrainPerson", "Cost", input_port_name="InVTrain", output_port_name="VTrain")
        self.addConnection("TrainPerson", "Cost", input_port_name="InXPerson", output_port_name="XPerson")

        self.addConnection("Cost", "cost", output_port_name="OutCost")


