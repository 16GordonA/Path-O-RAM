import Block
import Tree

class Bucket:
	header=[]
	blocks=[]
	numDummies=4
	def __init__(self, blocks, leaf):
		self.blocks=blocks
		self.leaf=leaf

	def insertBlock(self, block,segID):
		blocks.insert(0,block)

	def readOneBlock(self, segID):
		for i in range(0,len(blocks):
			if blocks[i].segID=segID:
				return blocks[i]
		return findDummy()

	def findDummy(self):
		for i in range (0,len(blocks)):
			if(blocks[i].segID==0):
				return blocks[i]
