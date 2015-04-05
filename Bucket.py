import Block
import Tree

class Bucket:
	header=[]
	blocks=[]

	def __init__(self, blocks, leaf):
		self.blocks=blocks
		self.leaf=leaf

	def insertBlock(self, block):
