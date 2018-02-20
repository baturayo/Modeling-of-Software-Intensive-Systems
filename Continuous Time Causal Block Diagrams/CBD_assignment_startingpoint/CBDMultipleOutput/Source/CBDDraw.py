from CBD import *
def draw(cbd, filename, colors=None):
	""" Output cbd as a dot script to filename.

	colors is a dictionary of blockname => color
	"""
	f = open(filename, "w")
	write = lambda s: f.write(s)

	write("""
digraph graphname {
 """)

	if colors == None:
		colors = {}

	def writeBlock(block):
		if isinstance(block, ConstantBlock):
			label = block.getBlockType() + " (" + block.getBlockName() + ")\\n" + str(block.getValue())
		else:
			label = block.getBlockType() + " (" + block.getBlockName() + ")"

		shape = ""
		if isinstance(block, CBD):
			shape=",shape=Msquare"

		col = ""
		if block.getBlockName() in colors:
			col = ", color=\"{0}\", fontcolor=\"{0}\"".format(colors[block.getBlockName()])

		write("{b} [label=\"{lbl}\"{shape}{col}];\n".format(b=block.getBlockName(),
			lbl=label,
			shape=shape,
			col=col))


	for block in cbd.getBlocks():
		writeBlock(block)
		for (name, other) in  block.getLinksIn().iteritems():
			label = ""

			if not name.startswith("IN"):
				label=name

			if not other.output_port.startswith("OUT"):
				label = label + " / " + other.output_port

			write("{a} -> {b} [label=\"{lbl}\"];\n".format(a=other.block.getBlockName(),
				b=block.getBlockName(),
				lbl=label))

	write("\n}")

