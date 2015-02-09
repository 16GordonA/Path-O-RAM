class Tree:
    def __init__ (self, layers, bucket_size):
        self.l = layers
        self.z = bucket_size
        self.blocks = [for i in range(self.z)] #I think this is the right way to do this
    
        if(self.l > 2):
            self.node1 = Tree(layers-1, bucket_size) #use recursive tree (left branch)
            self.node2 = Tree(layers-1, bucket_size) #use recursive tree (right branch)
        else:
            self.node1 = Leaf(bucket_size)
            self.node2 = Leaf(bucket_size)
    
    def pushDown(self):
        #do what it takes to push everything down...
    
    def readBlock(self, path):
        #some sort of recursive thing
        
    def writeBlock(self, path, data):
        #write to the new block, then call
  
    def moveBlock(self, new_path, old_path):
        #some sort of recursive thing involving getBlock(old_path)
    
    def getZ(self):
        return self.z
    
    def setZ(self, new_z):
        self.z = new_z
        return self.z
  
    def getL(self):
        return self.l
