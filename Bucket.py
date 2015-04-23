import Block
import Tree
from _sha import blocksize

class Bucket:	
	
	def __init__(self, blocks, z, S): #blocks, bucket size, number of dummies ~= A
		self.blocks=blocks
		self.padDummy()
		self._z = z
		self._S = S
		self.reshuffle()

	def insertBlocks(self, blocks): 
		self.blocks = blocks
		self.padDummy()
		self.reshuffle()

	def readOneBlock(self, segID):
		for i in range(len(blocks)):
			if segID in header:
				return blocks[header.index(segID)]
		return findDummy()
		
		self.accesses += 1
		
		if self.accesses == self._S:
			self.reshuffle()

	def findDummy(self):
		for i in range (0,len(header)):
			if(header[i]==0):
				header[i] = -1 #mark that it is used
				return blocks[i]
			
	def reshuffle(self): #shuffles blocks, reconstructs header
		random.shuffle(self.blocks)
		self.header = [self.blocks[i].segID for i in range(len(self.blocks))]
		self.accesses = 0
		
	def padDummy(self):
		while(len(self.blocks) < self._z+self._S):
			self.blocks += [Block.Block(0,0,b"")] #fills dummies