import Block
import Tree
import random
from _sha import blocksize

class Bucket:	
	
	def __init__(self, blocks, z, S): #blocks, bucket size, number of dummies ~= A		self.blocks=blocks
		self._z = z
		self._S = S
		self.insertBlocks(blocks)

	def __init__ (self, z, S):
		self._z = z
		self._S = S
		self.insertBlocks([])

	def access(self, blocks, segID, action):
		initlen = len(self.blocks)
		
		if action == 1:
			a = self.insertBlocks(blocks)
			#print('insertBlocks')
		if action == 2:
			a = self.readOneBlock(segID)
			#print('readOneBlock')
		if action == 3: 
			a = self.readAll()
			#print('readAll')
		
		#if len(self.blocks) != initlen:
			#print('blocks lost')
			
		return a
	def insertBlocks(self, blocks): 
		
		assert len(blocks) <= self._z, "Evicted " + str(len(blocks)) + " blocks when z is only " + str(self._z)
		self.blocks = blocks
		self.padDummy()
		self.reshuffle()

	def readOneBlock(self, segID):
		if self.accesses == self._S:
			self.reshuffle()
		
		b = None
		
		for i in range(len(self.blocks)):
			if segID in self.header:
				b =  self.blocks[self.header.index(segID)]
				self.header[self.header.index(segID)] = -1
		
		if b is None:
			b = self.findDummy()
		
		self.accesses += 1
			
		
		#print(self.header)
		return b

	def readAll(self):
		resp = []
		'''
		if len(self.header) != len(self.blocks):
			print(self.header)
			print(len(self.blocks))
		'''
		
		for i in range(len(self.header)):
			if self.header[i] > 0: #makes sure not dummy block
				#assert i < len(self.blocks), 'header length is ' + str(len(self.header)) + ' and blocks length is ' + str(len(self.blocks))
				resp += [self.blocks[i]]
		
		self.blocks = []
		self.padDummy()
		self.accesses = 0
		
		return resp
	
	def findDummy(self):
		return self.blocks[self.desdum[self.accesses]]
		'''
		for i in range (0,len(self.header)):
			if(self.header[i]==0):
				self.header[i] = -1 #mark that it is used
				return self.blocks[i]
		'''
		
		#return ErrorType()
			
	def reshuffle(self): #shuffles blocks, reconstructs header
		random.shuffle(self.blocks)
		self.header = [self.blocks[i].getSegID() for i in range(len(self.blocks))]
		self.accesses = 0
		
		self.desdum = []
		for i in range(len(self.header)):
			if self.header[i] == -2:
				self.desdum += [i]
		
		random.shuffle(self.desdum)
		
	def padDummy(self):
		while(len(self.blocks) < self._z):
			self.blocks.append(Block.Block(0,0,b"")) #fills dummies to z
		for i in range(self._S):
			self.blocks.append(Block.Block(0,-2,b"")) #fills designated dummies to z + S
		#print('have ' + str(len(self.blocks)) + ' blocks')
		
		
class ErrorType:
	def __init__(self):
		self.error = True