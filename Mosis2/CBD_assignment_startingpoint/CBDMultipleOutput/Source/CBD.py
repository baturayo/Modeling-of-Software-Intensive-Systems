import math
import naivelog
from collections import namedtuple

InputLink = namedtuple("InputLink", ["block", "output_port"])
Signal = namedtuple("Signal", ["time", "value"])
def enum(**enums):
            return type('Enum', (), enums)
level = enum(WARNING=1, ERROR=2, FATAL=3)	
epsilon = 0.001		

class BaseBlock:
    """
    A base class for all types of basic blocks
    """
    def __init__(self, name, input_ports, output_ports):
        self.setBlockName(name)

        #The output signals produced by this block is encoded as a dictionary.
        #The key of this dictionary is the name of the output port.
        #Each element of the dictionary contains an ordered list of values.
        self.__signals = dict()
        for output_port in output_ports:
            self.__signals[output_port] = []

        #The input links produced by this block is encoded as a dictionary.
        #The key of this dictionary is the name of the input port.
        #Each element of the dictionary contains
        #an tuple of the block and the output name of the other block.
        self._linksIn = dict()

        #The list of possible input ports
        self.__nameLinks = input_ports
        #In wich CBD the baseblock is situated
        self._parent = None

    def getBlockName(self):
        return self.__block_name

    def setBlockName(self, block_name):
        self.__block_name = block_name

    def setParent(self, parent):
        self._parent = parent

    def getBlockType(self):
        return self.__class__.__name__

    def getLinksIn(self):
        return self._linksIn

    def getOutputNameOfInput(self, inputBlock):
        return [ y for (x,y) in self._linksIn.iteritems() if y.block == inputBlock ][0].output_port

    def getInputName(self, inputBlock):
        return [ x for (x,y) in self._linksIn.iteritems() if y.block == inputBlock ]

    def getClock(self):
        return self._parent.getClock()

    def appendToSignal(self, value, name_output = None):
        name_output = "OUT1" if name_output == None else name_output
        assert name_output in self.__signals.keys()
        self.__signals[name_output].append(Signal(self.getClock().getTime(), value))

    def getSignal(self, name_output = None):
        name_output = "OUT1" if name_output == None else name_output
        assert name_output in self.__signals.keys()
        return self.__signals[name_output] if name_output != None else self.__signals["OUT1"]

    def getDependencies(self, curIteration):
        # TO IMPLEMENT: this is a helper function you can use to create the dependency graph...
        pass

    def getBlockConnectedToInput(self, input_port):
        return self._linksIn[input_port]

    def getInputSignal(self, curIteration, input_port = None):
        """
        Returns the signal sent out by the input block (IN1 if none given,
        at the last time if no curIteration is given).
        """
        input_port = "IN1" if input_port == None else input_port
        curIteration = -1 if curIteration == None else curIteration

        (incoming_block, out_port_name) = self._linksIn[input_port]
        return incoming_block.getSignal(out_port_name)[curIteration]

    def compute(self, curIteration):
        exit("BaseBlock has nothing to compute")

    def linkInput(self, in_block, name_input, name_output):
        """
        linkInput will link the output of the from_block to the input of the to_block
        -if no name_input was given for the to_block, we will derive the right input,
        by checking which input IN has nothing connected to it yet
        -if no name_output was given we use the first OUT output
        """
        name_output = "OUT1" if name_output == None else name_output
        if name_input != None:
            assert name_input in self.__nameLinks
            self._linksIn[name_input] = InputLink(in_block, name_output)
        else:
            i = 1
            while True:
                nextIn = "IN" + str(i)
                if nextIn in self.__nameLinks:
                    if not nextIn in self._linksIn:
                        self._linksIn[nextIn] = InputLink(in_block, name_output)
                        return
                else:
                    exit("There are no open IN inputs left in block %s" % self.getBlockName())
                i += 1

    def __repr__(self):
        repr = self.getBlockName() + ":" + self.getBlockType() + "\n"
        if len(self._linksIn) == 0:
            repr+= "  No incoming connections to IN ports\n"
        else:
            for (key, (in_block, out_port)) in self._linksIn.iteritems():
                repr += "In input " + key + ":  IN <- " + in_block.getBlockName() + ":" + in_block.getBlockType() + "\n"
        return repr

class ConstantBlock(BaseBlock):
    """
    The constant block will always output its constant value
    """
    def __init__(self, block_name, value=0.0):
        BaseBlock.__init__(self, block_name, [], ["OUT1"])
        self.__value = value

    def getValue(self):
        return self.__value

    def setValue(self, value):
        self.__value = value

    def compute(self, curIteration):
        # TO IMPLEMENT
        pass

    def __repr__(self):
        return BaseBlock.__repr__(self) + "  Value = " + str(self.getValue()) + "\n"

class NegatorBlock(BaseBlock):
    """
    The negator block will output the value of the input multiplied with -1
    """
    def __init__(self, block_name):
        BaseBlock.__init__(self, block_name, ["IN1"], ["OUT1"])

    def compute(self, curIteration):
        # TO IMPLEMENT
        pass

class InverterBlock(BaseBlock):
    """
    The invertblock will output 1/IN
    """
    def __init__(self, block_name):
        BaseBlock.__init__(self, block_name, ["IN1"], ["OUT1"])

    def compute(self, curIteration):
        # TO IMPLEMENT
        pass

class AdderBlock(BaseBlock):
    """
    The adderblock will add the 2 inputs
    """
    def __init__(self, block_name):
        BaseBlock.__init__(self, block_name, ["IN1", "IN2"], ["OUT1"])

    def	compute(self, curIteration):
    # TO IMPLEMENT
        pass

class ProductBlock(BaseBlock):
    """
    The product block will multiply the two inputs
    """
    def __init__(self, block_name):
        BaseBlock.__init__(self, block_name, ["IN1", "IN2"], ["OUT1"])

    def	compute(self, curIteration):
        # TO IMPLEMENT
        pass

class GenericBlock(BaseBlock):
    """
    The generic block will evaluate the operator on the input
    operator is the name (a string) of a Python function from the math library
    which will be called when the block is evaluated
    by default, initialized to None
    """
    def __init__(self, block_name, block_operator=None):
        # operator is the name (a string) of a Python function from the math library
        BaseBlock.__init__(self, block_name, ["IN1"], ["OUT1"])
        self.__block_operator = block_operator

    def getBlockOperator(self):
        return self.__block_operator

    def compute(self, curIteration):
        # TO IMPLEMENT
        pass

    def __repr__(self):
        repr = BaseBlock.__repr__(self)
        if self.__block_operator == None:
            repr += "  No operator given\n"
        else:
            repr += "  Operator :: " + self.__block_operator + "\n"
        return repr

class RootBlock(BaseBlock):
    """
    A basic block that computes the IN2-th root from IN1
    """
    def __init__(self, block_name):
        BaseBlock.__init__(self, block_name, ["IN1", "IN2"], ["OUT1"])

    def compute(self, curIteration):
        # TO IMPLEMENT
        pass

class ModuloBlock(BaseBlock):
    """
    A basic block that computes the IN1 modulo IN3
    """
    def __init__(self, block_name):
        BaseBlock.__init__(self, block_name, ["IN1", "IN2"], ["OUT1"])

    def compute(self, curIteration):
        # TO IMPLEMENT
        pass

class DelayBlock(BaseBlock):
    """
    A delay block that takes the last value from the list
    IC: Initial Condition
    """
    def __init__(self, block_name):
        BaseBlock.__init__(self, block_name, ["IN1", "IC"], ["OUT1"])
        self.__values = []

    def getDependencies(self, curIteration):
        # TO IMPLEMENT: This is a helper function you can use to create the dependency graph
        # Treat dependencies differently. For instance, at the first iteration (curIteration == 0), the block only depends on the IC;
        pass

    def compute(self, curIteration):
        #TO IMPLEMENT
        pass

class InputPortBlock(BaseBlock):
    """
    The input port of a CBD
    """
    def __init__(self, block_name, parent):
        BaseBlock.__init__(self, block_name, [], ["OUT1"])
        self.parent = parent

    def	compute(self, curIteration):
        self.appendToSignal(self.parent.getInputSignal(curIteration, self.getBlockName()).value)

class OutputPortBlock(BaseBlock):
    """
    The output port of a CBD
    """
    def __init__(self, block_name, parent):
        BaseBlock.__init__(self, block_name, ["IN1"], ["OUT1"])
        self.parent = parent

    def	compute(self, curIteration):
        self.appendToSignal(self.getInputSignal(curIteration, "IN1").value)

class WireBlock(BaseBlock):
    """
    When a CBD gets flattened, the port blocks will be replaced by a wire block
    """
    def __init__(self, block_name):
        BaseBlock.__init__(self, block_name, ["IN1"], ["OUT1"])

    def	compute(self, curIteration):
        self.appendToSignal(self.getInputSignal(curIteration, "IN1").value)

class TimeBlock(BaseBlock):
    """
    Outputs the current time of the simulation
    """
    def __init__(self, block_name):
        BaseBlock.__init__(self, block_name, [], ["OUT1"])

    def	compute(self, curIteration):
        self.appendToSignal(self.getClock().getTime())

class SequenceBlock(BaseBlock):
    """
    A simple Sequence block: block initializes signal input with given sequence
    Use only for the tests please
    """
    def __init__(self, block_name, sequence):
        BaseBlock.__init__(self, block_name, [], ["OUT1"])
        self.__sequence = sequence

    def	compute(self, curIteration):
        if len(self.__sequence) < curIteration:
            self.__logger.fatal("Sequence is niet lang genoeg")
        self.appendToSignal(self.__sequence[curIteration])

class LoggingBlock(BaseBlock):
    """
    A simple Logging block
    """
    def __init__(self, block_name, string, lev = level.WARNING):
        BaseBlock.__init__(self, block_name, ["IN1"], [])
        self.__string = string
        self.__logger = naivelog.getLogger("WarningLog")
        self.__lev = lev

    def	compute(self, curIteration):
        if self.getInputSignal(curIteration, "IN1").value == 1:
            if self.__lev == level.WARNING:
                self.__logger.warning("Time " + str(self.getClock().getTime()) + ": " + self.__string)
            elif self.__lev == level.ERROR:
                self.__logger.error("Time " + str(self.getClock().getTime()) + ": " + self.__string)
            elif self.__lev == level.FATAL:
                self.__logger.fatal("Time " + str(self.getClock().getTime()) + ": " + self.__string)

class Clock:
    """
    The clock of the simulation
    delta_t is the timestep of the simulation
    """
    def __init__(self, delta_t):
        self.__delta_t = delta_t
        self.__time = 0.0

    def getTime(self):
        return self.__time

    def step(self):
        self.__time = self.__time + self.__delta_t

    def setDeltaT(self, new_delta_t):
        self.__delta_t = new_delta_t

    def getDeltaT(self):
        return self.__delta_t

class CBD(BaseBlock):
    """
    The CBD class, contains an entire Causal Block Diagram
    Call the run function to simulate the model.
    """
    def __init__(self, block_name, input_ports = None, output_ports = None):
        input_ports = input_ports if input_ports != None else []
        output_ports = output_ports if output_ports != None else []
        BaseBlock.__init__(self, block_name, input_ports, output_ports)
        #The blocks in the CBD will be stored both
        #-as an ordered list __blocks and
        #-as a dictionary __blocksDict with the blocknames as keys
        #for fast name-based retrieval and to ensure block names are unique within a single CBD
        self.__blocks = []
        self.__blocksDict = {}
        self.__clock = None
        self.__deltaT = None
        self.__logger = naivelog.getLogger("CBD")

        for input_port in input_ports:
            self.addBlock(InputPortBlock(input_port, self))

        for output_port in output_ports:
            self.addBlock(OutputPortBlock(output_port, self))

    def getTopCBD(self):
        return self if self._parent == None else self._parent.getTopCBD()

    def flatten(self, parent = None):
        """
        Flatten the CBD parent and call flatten recursively for CBD's in this CBD
        """
        blocksToRemove = []
        blocksToAdd = []

        for childBlock in self.__blocks:
            if isinstance(childBlock, InputPortBlock):
                # Replace InputPortBlock with WireBlock
                wb = WireBlock(childBlock.getBlockName())

                # Replace links going out of inputportblock
                blocksToRemove.append(childBlock)
                blocksToAdd.append(wb)

                for b in self.getBlocks():
                    for input_name, output_port in  [ (x,y.output_port) for (x,y) in b._linksIn.iteritems() if y.block == childBlock ]:
                        b._linksIn[input_name] = InputLink(wb, "OUT1")

                input = self._linksIn[wb.getBlockName()]
                parent.addConnection(input.block, wb, output_port_name = input.output_port)
            elif isinstance(childBlock, OutputPortBlock):
                # Replace OutputPortBlock with WireBlock
                wb = WireBlock(childBlock.getBlockName())
                blocksToRemove.append(childBlock)
                blocksToAdd.append(wb)

                for (x,y) in childBlock._linksIn.iteritems():
                    wb._linksIn[x] = y

                # blocks connected to this output
                for b in parent.__blocks:
                    for (portname, input) in b._linksIn.iteritems():
                        if input.block == self and input.output_port == wb.getBlockName():
                            b._linksIn[portname] = InputLink(wb, "OUT1")

        for childBlock in self.__blocks:
            if isinstance(childBlock, CBD):
                childBlock.flatten(self)
                blocksToRemove.append(childBlock)

        # Delete blocksToRemove
        for block in blocksToRemove:
            self.removeBlock(block)

        for b in blocksToAdd:
            self.addBlock(b)

        if parent != None:
            # Add all components to parent, do not copy blocksToRemove
            for block in [ b for b in self.__blocks if not b in blocksToRemove ]:
                block.setBlockName(self.getBlockName() + "." + block.getBlockName())
                parent.addBlock(block)

    def setBlocks(self, blocks):
        # blocks must be a list of BaseBlock (subclass) instances
        assert type(blocks) == list, ("CBD.setBlocks() takes a list as argument, not a %s" % type(blocks))
        for block in blocks:
            assert isinstance(block, BaseBlock), "CBD.setBlocks() takes a list of BaseBlock (subclass) instances"

    def getBlocks(self):
        return self.__blocks

    def getBlockByName(self, name):
        return self.__blocksDict[name]

    def getClock(self):
        return self.__clock if self._parent == None else self._parent.getClock()

    def setDeltaT(self, deltaT):
        self.__deltaT = deltaT

    def addBlock(self, block):
        """
        Add a block to the CBD model
        """
        assert isinstance(block, BaseBlock), "Can only add BaseBlock (subclass) instances to a CBD"
        block.setParent(self)

        if not self.__blocksDict.has_key(block.getBlockName()):
            self.__blocks.append(block)
            self.__blocksDict[block.getBlockName()] = block
        else:
            print("Warning: did not add this block as it has the same name %s as an existing block" % block.getBlockName())

    def removeBlock(self, block):
        assert isinstance(block, BaseBlock), "Can only delete BaseBlock (subclass) instances to a CBD"

        if self.__blocksDict.has_key(block.getBlockName()):
            self.__blocks.remove(block)
            del self.__blocksDict[block.getBlockName()]
        else:
            exit("Warning: did not remove this block %s as it was not found" % block.getBlockName())

    def addConnection(self, from_block, to_block, input_port_name = None, output_port_name = None):
        """
        Add a connection between from_block with input_port_name to to_block with outport_port_name
        """
        if type(from_block) == str:
            from_block = self.getBlockByName(from_block)
        if type(to_block) == str:
            to_block = self.getBlockByName(to_block)
        to_block.linkInput(from_block, input_port_name, output_port_name)

    def __repr__(self):
        repr = BaseBlock.__repr__(self)
        repr += "\n"
        for block in self.getBlocks():
            repr+= block.__repr__()
        return repr

    def dump(self):
        print("=========== Start of Model Dump ===========")
        print(self)
        print("=========== End of Model Dump =============\n")

    def dumpSignals(self):
        print("=========== Start of Signals Dump ===========")
        for block in self.getBlocks():
            print("%s:%s" % (block.getBlockName(), block.getBlockType()))
            print(str(block.getSignal()) + "\n")
        print("=========== End of Signals Dump =============\n")

    def getSignal(self, name_output = None):
        name_output = "OUT1" if name_output == None else name_output
        portBlock = self.getBlockByName(name_output)
        assert portBlock != None
        return portBlock.getSignal("OUT1")

    def run(self, steps, delta_t = 1.0, verbose = False):
        """
        Simulate the model!
        @param delta_t: The timestep of the simulation
        """
        self.__clock = Clock(delta_t)
        self.__deltaT = delta_t
        depGraph = None
        sortedGraph = None
        for curIteration in range(steps):
            if curIteration < 2:
                depGraph = self.__createDepGraph(curIteration)
                sortedGraph = depGraph.getStrongComponents(curIteration)
            self.__step(depGraph, sortedGraph, curIteration)

    def __step(self, depGraph, sortedGraph, curIteration):
        self.__computeBlocks(sortedGraph, depGraph, curIteration)
        self.getClock().setDeltaT(self.__deltaT)
        self.getClock().step()

    def __createDepGraph(self, curIteration):
        """
         Create a dependency graph of the CBD model.
         Use the curIteration to differentiate between the first and other iterations
         Watch out for dependencies with sub-models.
        """
        blocks = self.getBlocks()
        depGraph = DepGraph()
        # TO IMPLEMENT
        # hints: use depGraph.setDependency(block, block_it_depends_on)
        #        use the getDependencies that is implemented in each specific block.
        #
        return depGraph

    def __computeBlocks(self, sortedGraph, depGraph, curIteration):
        for component in sortedGraph:
            if (not self.__hasCycle(component, depGraph)):
                block = component[0]   # the strongly connected component has a single element
                block.compute(curIteration)
            else:
                # Detected a strongly connected component
                if not self.__isLinear(component):
                    self.__logger.fatal("Cannot solve non-linear algebraic loop")
                solverInput = self.__constructLinearInput(component, curIteration)
                self.__gaussjLinearSolver(solverInput)
                solutionVector = solverInput[1]
                for block in component:
                    blockIndex = component.index(block)
                    block.appendToSignal(solutionVector[blockIndex])

    def __hasCycle(self, component, depGraph):
        """
        Determine whether a component is cyclic
        """
        assert len(component)>=1, "A component should have at least one element"
        if len(component)>1:
            return True
        else: # a strong component of size one may still have a cycle: a self-loop
            if depGraph.hasDependency(component[0], component[0]):
                return True
            else:
                return False

    def __isLinear(self, strongComponent):
        """
        Determines if an algebraic loop describes a linear equation or not
        As input you get the detected loop in a list.
        If the loop is linear return True
        Else: call exit(1) to exit the simulation with exit code 1
        """
        #TO IMPLEMENT
        pass

    def __constructLinearInput(self, strongComponent, curIteration):
        """
        Constructs input for a solver of systems of linear equations
        Input consists of two matrices:
        M1: coefficient matrix, where each row represents an equation of the system
        M2: result matrix, where each element is the result for the corresponding equation in M1
        """
        size = len(strongComponent)
        row = []
        M1 = []
        M2 = []

        # Initialize matrices with zeros
        i = 0
        while (i < size):
            j = 0
            row = []
            while (j < size):
                row.append(0)
                j += 1
            M1.append(row)
            M2.append(0)
            i += 1

        # block -> index of block
        indexdict = dict()

        for (i,block) in enumerate(strongComponent):
            indexdict[block] = i

        resolveBlock = lambda possibleDep, output_port: possibleDep if not isinstance(possibleDep, CBD) else possibleDep.getBlockByName(output_port)

        def getBlockDependencies2(block):
            return [ resolveBlock(b,output_port) for (b, output_port) in [block.getBlockConnectedToInput("IN1"),  block.getBlockConnectedToInput("IN2")]]

        for (i, block) in enumerate(strongComponent):
            if block.getBlockType() == "AdderBlock":
                for external in [ x for x in getBlockDependencies2(block) if x not in strongComponent ]:
                    M2[i] -= external.getSignal()[curIteration].value
                M1[i][i] = -1

                for compInStrong in [ x for x in getBlockDependencies2(block) if x in strongComponent ]:
                    M1[i][indexdict[compInStrong]] = 1
            elif block.getBlockType() == "ProductBlock":
                #M2 can stay 0
                M1[i][i] = -1
                M1[i][indexdict[[ x for x in getBlockDependencies2(block)  if x in strongComponent ][0]]] = reduce(lambda x,y: x*y, [ x.getSignal()[curIteration].value for x in getBlockDependencies2(block) if x not in strongComponent ])
            elif block.getBlockType() == "NegatorBlock":
                #M2 can stay 0
                M1[i][i] = -1
                possibleDep, output_port = block.getBlockConnectedToInput("IN1")
                M1[i][indexdict[resolveBlock(possibleDep, output_port)]] = - 1
            elif block.getBlockType() == "InputPortBlock":
                #M2 can stay 0
                M1[i][i] = 1
                possibleDep, output_port = block.parent.getBlockConnectedToInput(block.getBlockName())
                M1[i][indexdict[resolveBlock(possibleDep, output_port)]] = - 1
            elif block.getBlockType() == "OutputPortBlock" or block.getBlockType() == "WireBlock":
                #M2 can stay 0
                M1[i][i] = 1
                M1[i][indexdict[block.getDependencies(0)[0]]] = - 1
            elif block.getBlockType() == "DelayBlock":
                # If a delay is in a strong component, this is the first iteration
                assert curIteration == 0
                # And so the dependency is the IC
                # M2 can stay 0 because we have an equation of the type -x = -ic <=> -x + ic = 0
                M1[i][i] = -1
                possibleDep, output_port = block.getBlockConnectedToInput("IC")
                dependency = resolveBlock(possibleDep, output_port)
                assert dependency in strongComponent
                M1[i][indexdict[dependency]] = 1
            else:
                self.__logger.fatal("Unknown element, please implement")
        return [M1, M2]

    def __ivector(self, n):
        v = []
        for i in range(n):
            v.append(0)
        return v

    def __swap(self, a, b):
        return (b, a)

    def __gaussjLinearSolver(self, solverInput):
        M1 = solverInput[0]
        M2 = solverInput[1]
        n = len(M1)
        indxc = self.__ivector(n)
        indxr = self.__ivector(n)
        ipiv = self.__ivector(n)
        icol = 0
        irow = 0
        for i in range(n):
            big = 0.0
            for j in range(n):
                if (ipiv[j] != 1):
                    for k in range(n):
                        if (ipiv[k] == 0):
                            if (math.fabs(M1[j][k]) >= big):
                                big = math.fabs(M1[j][k])
                                irow = j
                                icol = k
                        elif (ipiv[k] > 1):
                            raise ValueError("GAUSSJ: Singular Matrix-1")
            ipiv[icol] += 1
            if (irow != icol):
                for l in range(n):
                    (M1[irow][l], M1[icol][l]) = self.__swap(M1[irow][l], M1[icol][l])
                (M2[irow], M2[icol]) = self.__swap(M2[irow], M2[icol])
            indxr[i] = irow
            indxc[i] = icol
            if (M1[icol][icol] == 0.0):
                raise ValueError("GAUSSJ: Singular Matrix-2")
            pivinv = 1.0/M1[icol][icol]
            M1[icol][icol] = 1.0
            for l in range(n):
                M1[icol][l] *= pivinv
            M2[icol] *= pivinv
            for ll in range(n):
                if (ll != icol):
                    dum = M1[ll][icol]
                    M1[ll][icol] = 0.0
                    for l in range(n):
                        M1[ll][l] -= M1[icol][l] * dum
                    M2[ll] -= M2[icol] * dum
        l = n
        while (l > 0):
            l -= 1
            if (indxr[l] != indxc[l]):
                for k in range(n):
                    (M1[k][indxr[l]], M1[k][indxc[l]]) = self.__swap(M1[k][indxr[l]], M1[k][indxc[l]])

class AddOneBlock(CBD):
    """
    Block adds a one to the input (used a lot for mux)
    """
    def __init__(self, block_name, faultOrder=3):
        CBD.__init__(self, block_name, ["IN1"], ["OUT1"])
        self.addBlock(ConstantBlock(block_name="OneConstant", value=1))
        self.addBlock(AdderBlock("PlusOne"))
        self.addConnection("IN1", "PlusOne")
        self.addConnection("OneConstant", "PlusOne")
        self.addConnection("PlusOne", "OUT1")

class DerivatorBlock(CBD):
    """
    The derivator block is a CBD that calculates the derivative
    """
    def __init__(self, block_name):
        CBD.__init__(self, block_name, ["IN1", "delta_t", "IC"], ["OUT1"])
        #TO IMPLEMENT

class IntegratorBlock(CBD):
    """
    The integrator block is a CBD that calculates the integration
    """
    def __init__(self, block_name):
        CBD.__init__(self, block_name, ["IN1", "delta_t", "IC"], ["OUT1"])
        # TO IMPLEMENT


""" This module implements a dependency graph
    @author: Marc Provost
    @organization: McGill University
    @license: GNU General Public License
    @contact: marc.provost@mail.mcgill.ca
"""

import copy
class DepNode:
    """ Class implementing a node in the dependency graph.
    """

    def __init__(self, object):
        """ DepNode's constructor.
                @param object: Reference to a semantic object identifying the node
                @type object: Object
        """
        self.__object = object
        self.__isMarked	 = False

    def mark(self):
        self.__isMarked = True

    def unMark(self):
        self.__isMarked = False

    def isMarked(self):
        return self.__isMarked

    def getMappedObj(self):
        return self.__object

    def __repr__(self):
        return "DepNode :: "+str(self.__object)

class DepGraph:
    """ Class implementing dependency graph.
    """

    def __init__(self):
        """ DepGraph's constructor.
        """
        #Dict holding a mapping "Object -> DepNode"
        self.__semanticMapping = {}

        #map object->list of objects depending on object
        self.__dependents = {}
        #map object->list of objects that influences object
        self.__influencers = {}

    def __repr__(self):
        repr = "Dependents: \n"
        for dep in self.__dependents:
            repr += dep.getBlockName() + ":" + str(self.__dependents[dep]) + "\n"
        repr += "Influencers: \n"
        for infl in self.__influencers:
            repr += infl.getBlockName() + ":" + str(self.__influencers[infl]) + "\n"
        return repr

    def addMember(self, object):
        """ Add an object mapped to this graph.
                @param object: the object to be added
                @type object: Object
                @raise ValueError: If object is already in the graph
        """
        if not self.hasMember(object):
            if not isinstance(object, CBD):
                node = DepNode(object)
                self.__dependents[object] = []
                self.__influencers[object] = []
                self.__semanticMapping[object] = node
            else:
                for block in object.getBlocks():
                    self.addMember(block)
        else:
            raise ValueError("Specified object is already member of this graph")

    def hasMember(self, object):
        return self.__semanticMapping.has_key(object)

    def removeMember(self, object):
        """ Remove a object from this graph.
                @param object: the object to be removed
                @type object: Object
                @raise ValueError: If object is not in the graph
        """
        if self.hasMember(object):
            for dependent in self.getDependents(object):
                self.__influencers[dependent].remove(object)
            for influencer in self.getInfluencers(object):
                self.__dependents[influencer].remove(object)

            del self.__dependents[object]
            del self.__influencers[object]
            del self.__semanticMapping[object]
        else:
            raise ValueError("Specified object is not member of this graph")

    def setDependency(self, dependent, influencer, curIt):
        """
            Creates a dependency between two objects.
                @param dependent: The object which depends on the other
                @param influcencer: The object which influences the other
                @type dependent: Object
                @type dependent: Object
                @raise ValueError: if depedent or influencer is not member of this graph
                @raise ValueError: if the dependency already exists
        """

        # Link CBD outputs
        if isinstance(influencer, CBD):
            # When there is more than one connection from a CBD to one and the same block,
            # more than one dependency should be set, as there is more than one underlying
            # output block
            for output_port in [ y.output_port for (x,y) in dependent.getLinksIn().iteritems() if y.block == influencer ]:
                self.setDependency(dependent, influencer.getBlockByName(output_port), curIt)
            return

        # Link CBD inputs
        if isinstance(dependent, CBD):
            cbd = dependent
            directlyConnected = influencer.parent if isinstance(influencer, OutputPortBlock) else influencer
            inputnames = dependent.getInputName(directlyConnected)

            # When one influencer has multiple connections to this CBD, call this function once fo
            for inputname in inputnames:
                inputtingBlock = dependent.getBlockByName(inputname)
                thisdep = inputtingBlock
                self.setDependency(thisdep, influencer, curIt)
            return

        if self.hasMember(dependent) and self.hasMember(influencer):
            if not influencer in self.__influencers[dependent] and\
                 not dependent in self.__dependents[influencer]:
                self.__influencers[dependent].append(influencer)
                self.__dependents[influencer].append(dependent)
        else:
            if not self.hasMember(dependent):
                raise ValueError("Specified dependent object is not member of this graph")
            if not self.hasMember(influencer):
                print(influencer)
                raise ValueError("Specified influencer object is not member of this graph")

    def hasDependency(self, dependent, influencer):
        if self.hasMember(dependent) and self.hasMember(influencer):
            return influencer in self.__influencers[dependent] and\
                         dependent in self.__dependents[influencer]
        else:
            if not self.hasMember(dependent):
                raise ValueError("Specified dependent object is not member of this graph")
            if not self.hasMember(influencer):
                raise ValueError("Specified influencer object is not member of this graph")

    def unsetDependency(self, dependent, influencer):
        """ Removes a dependency between two objects.
                @param dependent: The object which depends on the other
                @param influcencer: The object which influences the other
                @type dependent: Object
                @type dependent: Object
                @raise ValueError: if depedent or influencer is not member of this graph
                @raise ValueError: if the dependency does not exists
        """
        if self.hasMember(dependent) and self.hasMember(influencer):
            if influencer in self.__influencers[dependent] and\
                 dependent in self.__dependents[influencer]:
                self.__influencers[dependent].remove(influencer)
                self.__dependents[influencer].remove(dependent)
            else:
                raise ValueError("Specified dependency does not exists")
        else:
            if not self.hasMember(dependent):
                raise ValueError("Specified dependent object is not member of this graph")
            if not self.hasMember(influencer):
                raise ValueError("Specified influencer object is not member of this graph")

    def getDependents(self, object):
        if self.hasMember(object):
            return copy.copy(self.__dependents[object])
        else:
            raise ValueError("Specified object is not member of this graph")

    def getInfluencers(self, object):
        if self.hasMember(object):
            return copy.copy(self.__influencers[object])
        else:
            raise ValueError("Specified object is not member of this graph")

    def getStrongComponents(self, curIt = 1):
        return self.__strongComponents(curIt)

    def __getDepNode(self, object):
        if self.hasMember(object):
            return self.__semanticMapping[object]
        else:
            raise ValueError("Specified object is not a member of this graph")

    def __mark(self, object):
        self.__getDepNode(object).mark()

    def __unMark(self, object):
        self.__getDepNode(object).unMark()

    def __isMarked(self, object):
        return self.__getDepNode(object).isMarked()

    def __topoSort(self):
        """ Performs a topological sort on the graph.
        """
        for object in self.__semanticMapping.keys():
            self.__unMark(object)

        sortedList = []

        for object in self.__semanticMapping.keys():
            if not self.__isMarked(object):
                self.__dfsSort(object, sortedList)

        return sortedList

    def __dfsSort(self, object, sortedList):
        """ Performs a depth first search collecting
                the objects in topological order.
                @param object: the currently visited object.
                @param sortedList: partial sorted list of objects
                @type object: Object
                @type sortedList: list Of Object
        """

        if not self.__isMarked(object):
            self.__mark(object)

            for influencer in self.getInfluencers(object):
                self.__dfsSort(influencer, sortedList)

            sortedList.append(object)

    def __strongComponents(self, curIt):
        """ Determine the strong components of the graph
                @rtype: list of list of Object
        """
        strongComponents = []
        sortedList = self.__topoSort()

        for object in self.__semanticMapping.keys():
            self.__unMark(object)

        sortedList.reverse()

        for object in sortedList:
            if not self.__isMarked(object):
                component = []
                self.__dfsCollect(object, component, curIt)
                strongComponents.append(component)

        strongComponents.reverse()
        return strongComponents

    def __dfsCollect(self, object, component, curIt):
        """ Collects objects member of a strong component.
                @param object: Node currently visited
                @param component: current component
                @type object: Object
                @type component: List of Object
        """
        if not self.__isMarked(object):
            self.__mark(object)

            for dependent in self.getDependents(object):
                self.__dfsCollect(dependent, component, curIt)

            component.append(object)













