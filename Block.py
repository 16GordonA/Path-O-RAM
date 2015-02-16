import Tree

class Block:
  
    def __init__(self, leaf, segID, data):
        self.path = path
        self.leaf = leaf
        self.segID = segID

    def getData(self):
        return data
  
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
