class Tree:
  def __init__ (self, layers, bucket_size):
    self.l = layers
    self.z = bucket_size
    
    if(self.l > 1):
      self.tL = Tree(layers-1, bucket_size) #use recursive tree (left branch)
      self.tR = Tree(layers-1, bucket_size) #use recursive tree (right branch)
    else:
      self.leaf = Leaf(bucket_size)
    
  def pushDown(self):
    #do what it takes to push everything down...
    
  def getBlock(self, path):
    #some sort of recursive thing
  
  def setBlock(self, new_path, old_path):
    #some sort of recursive thing involving getBlock(old_path)
    
  def getZ(self):
    return self.z
    
  def setZ(self, new_z):
    self.z = new_z
    return self.z
  
  def getL(self):
    return self.l
