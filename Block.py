import Tree

class Block:
    blockCount = 0
    
    def __init__(self, leaf, segID, data):
        self.data = data
        self.leaf = leaf
        self.segID = segID
        #self.identifier = Block.blockCount
        Block.blockCount += 1

    def getData(self):
        return self.data
  
    def setData(self, new_data):
        self.data = new_data
        return self.data
    
    def getLeaf(self):
        return self.leaf
  
    def setLeaf(self, new_leaf):
        self.leaf = new_leaf
        return self.leaf
    
    def getSegID(self):
        return self.segID
    
    #def getID(self):
        #return self.identifier
