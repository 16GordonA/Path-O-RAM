class Block:
  
  def __init__(self, path, data):
    self.path = path
    self.data = data
    self.moveDown()
    
  def moveDown(self):
    #follow the path
    
  def getData(self):
    return data
  
  def setData(self, new_data):
    self.data = new_data
    return self.data
    
  def getPath(self):
    return self.path
  
  def setPath(self, new_path):
    self.path = new_path
    return self.path
