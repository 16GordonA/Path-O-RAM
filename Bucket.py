import Block
import Tree
import random
from _sha import blocksize

class Bucket:	
	
	def __init__(self, blocks, z, S): #blocks, bucket size, number of dummies ~= A
		self.blocks=blocks
		self._z = z
		self._S = S
		self.padDummy()
		self.reshuffle()

	def __init__ (self, z, S):
		self._z = z
		self._S = S
		self.blocks = []
		self.padDummy()
		self.reshuffle()

	def insertBlocks(self, blocks): 
		self.blocks = blocks
		self.padDummy()
		self.reshuffle()

	def readOneBlock(self, segID):
		for i in range(len(blocks)):
			if segID in header:
				b =  blocks[header.index(segID)]
				blocks[header.index(segID)] = Block.Block(0,0,b"")
				header[header.index(segID)] = -1
				return b
		return findDummy()
		
		self.accesses += 1
		
		if self.accesses == self._S:
			self.reshuffle()

	def readAll(self):
		blocks = []
		
		for i in range(len(self.header)):
			if self.header[i] > 0: #makes sure not dummy block
				blocks += [self.blocks[i]]
		
		self.blocks = []
		
		return blocks
	
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