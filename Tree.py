# nodes are stored in a list
# their position in the list is their address - 1
# paths on the tree go from root to leaf
# readPath and writePath use 2d lists of blocks

import random
import Util
import Block
#import DBFileSys
import Bucket
import time
import math
from imaplib import Response_code

class Tree:
    _numAccesses = 0
    def __init__(self, nodeNumber, z, A, segmentSize):
        self.useRAM = True
        
        if self.useRAM:
            self._buckets = [Bucket.Bucket(z, A)] * nodeNumber 
        for bucket in self._buckets:
            bucket.insertBlocks([])
        print("buckets created")
        
        assert (nodeNumber % 2 == 1), "tree must have odd number of buckets"
        self._size = nodeNumber
        self._height = int(math.log(self._size+1,2))
        self._z = z
        self._segmentSize = segmentSize
        self.numGrowth = 0
        self.totalTimeGrowth = 0
        self._A = A #eviction frequency of ORAM
    
    def getSize(self):
        return self._size
    
    def randomLeaf(self):
        return random.randint(int(self._size / 2) + 1, self._size)
    
    def ringLeaf(self):

        binary = (bin(Tree._numAccesses)[2:]).zfill(self._height - 1) 
        #print (str(binary))

 
        binary = binary[::-1]
        Tree._numAccesses += 1
        Tree._numAccesses = (Tree._numAccesses)%(int(math.pow(2,self._height - 1)))
        resp = self._size -(int(binary,2))
        #print ("will return %d" %resp)
        return resp

    def readBucket(self, bucketID): #reads whole thing
        #print("BucketID is " + str(bucketID))
        if self.useRAM:
            return self._buckets[bucketID  -1].access([],0,3) #readAll
        else:
            return DBFileSys.readBucket(bucketID, self._segmentSize)
        
    def readBlock(self, segID, bucketID): #one block per bucket
        return self._buckets[bucketID - 1].access([],segID,2) #readOneBlock
    
    def writeBucket(self, bucketID, blocks):
        if self.useRAM:
            self._buckets[bucketID - 1].access(blocks,0,1) #insertBlocks
        else:
            DBFileSys.writeBucket(bucketID, blocks, self._segmentSize)
    
    def readPath(self, leaf, segID):
        result = []
        for addr in Util.getPathNodes(leaf):
            result.append(self.readBlock(segID, addr)) #needs fixins
        return result
    
    def readWholePath(self,leaf):
        result = []
        for addr in Util.getPathNodes(leaf):
            result.append(self.readBucket(addr))
        return result
    def writePath(self, leaf, blocks):
        for addr in Util.getPathNodes(leaf):
            self.writeBucket(addr, blocks.pop(0))
