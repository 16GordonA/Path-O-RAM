import Block
class Tree:
    def __init__ (self, layers, bucket_size, path):
        self.path = path
        self.l = layers
        self.z = bucket_size
        self.blocks = [Block(path + [math.randomint(0,1) for j in range(self.l)], 'dummy') 
                       for i in range(0,self.z)] 
                        #I think this is the right way to do this
        
        self.blockCt = 0
        for b in self.blocks:
            if b is not None:
                blockCt += 1
        
        if(self.l > 2):
            self.node1 = Tree(layers-1, bucket_size, path + [0]) #use recursive tree (left branch)
            self.node2 = Tree(layers-1, bucket_size, path + [1]) #use recursive tree (right branch)
        else:
            self.node1 = Leaf(bucket_size, path)
            self.node2 = Leaf(bucket_size, path)
    
    def pushDown(self):
        if self.l > 2:
            self.node1.pushDown()
            self.node2.pushDown()
            
        for b in self.blocks:
            if not b.dummy: 
                if node1.blockCt < self.z and b.getpath()[len(self.path)] == 0:
                    node1.addBlock(b)
                    self.blockCt -= 1
                if node2.blockCt < self.z and b.getpath()[len(self.path)] == 1:
                    node2.addBlock(b)
                    self.blockCt -= 1            
                    
        #do what it takes to push everything down...
        
    def addBlock(self, b):
        if self.orderSpaces():
            self.blocks[len(blocks) - 1] = b
            self.blockCt += 1
            return True
        return False
        
    def readBlock(self, path):
        print "need to implement"
        #some sort of recursive thing
        
    def writeBlock(self, path, data):
        print "need to implement"
        #write to the new block, then call
  
    def moveBlock(self, new_path, old_path):
        print "need to implement"
        #some sort of recursive thing involving getBlock(old_path)
    
    def getZ(self):
        return self.z
    
    def setZ(self, new_z):
        self.z = new_z
        return self.z
  
    def getL(self):
        return self.l
    
    def orderSpaces(self): #places spaces as final blocks
        new_blocks = self.blocks
        
        i = 0
        j = len(self.blocks) - 1
        for b in self.blocks:
            if b is None:
                new_blocks[j] = b
                j -= 1
            else:
                new_blocks[i] = b
                i += 1        
        self.blocks = new_blocks
        
        if j == len(self.blocks) - 1:   #if no empty spaces
            return False
        return True

class Leaf(Tree):
    def __init__ (self, bucket_size, path):
        self.z = bucket_size
        self.path = path
        self.blocks = [Block(path + [math.randomint(0,1) for j in range(self.l)], 'dummy') 
                       for i in range(0,self.z)] 
                        #I think this is the right way to do this
        
        self.blockCt = 0
        for b in self.blocks:
            if b is not None:
                blockCt += 1