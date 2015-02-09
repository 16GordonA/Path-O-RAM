import Tree

class Block:
  
    def __init__(self, path, data):
        self.path = path
        self.data = data
        if data is None or data == "dummy":
            self.dummy = True
        else:
            self.dummy = False
        self.moveDown()
    
    def moveDown(self):
        print "whee"
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
