import Util
import Block
from Tree import Tree
import Stash
import PosMap

class Oram:
    def __init__(self, treeSize, z, segmentSize, maxStashSize, growR, targetR, shrinkR): # grow/shrink triggered by ratio (buckets * z) / (# of segments)
        self._z = z
        self._tree = Tree(treeSize, z, segmentSize) #changed to fix the existing constructor on the tree class I (akiva) wrote
        self._stash = Stash.Stash(z)
        self._posMap = PosMap.PosMap()
        self._c = maxStashSize

        self._segCounter = 0

        self.useVCache = True
        self.debug = False
        
        self.VCacheCounter = 0
        self.totalCounter= 0

		# Comment: You may find it helpful to print out stash content when debugging
		
    def access(self, action, segIDList, dataList):
        self.totalCounter += 1
		# Comment: also need back ground eviction on a read operation       
		# TODO: try to get the background eviction rate under different Z and tree size

        while (action == "read" or action == "write") and self._stash.getSize() > self._c:              # background eviction
            if self.debug:
                print("backEv")
            self.access("backEv", [0], [None])

        for i in range(len(dataList)):
            if isinstance(dataList[i], str):
                dataList[i] = dataList[i]#.encode("utf-8")
        
        newLeaf = self.pickLeaf()

        for i in range(len(dataList)):
            reqResult = self._stash.request(segIDList[i])
            if reqResult != "not found":
                self.VCacheCounter += 1

                reqResult.setLeaf(newLeaf)
                self._posMap.insert(segIDList[i], newLeaf)
                if self.debug == True:
                    print("found in stash")
                if action == "write":
                    reqResult.setData(dataList[i])
                if action != "delete":
                    self._stash.addNode(reqResult)
                else:
                    self._posMap.delete(segIDList[i])
                    self._segCounter -= 1
                if self.useVCache == False:
                    self.treeAccess("dummy", segIDList, dataList)
                segIDList[i] = None
                if action == "write":
                    dataList[i] = None
                else:
                    dataList[i] = reqResult.getData()

        if all(x is None for x in segIDList):
            return dataList
        else:
            segID = segIDList[0]
            segID = next(x for x in segIDList if x is not None)
            leaf = self._posMap.lookup(segID)
            if leaf == -1:
                assert ((action != "read" and segID > 0) or action == "backEv" or action == "dummy"), "tried to " + action + " nonexistent segID: " + str(segID)
                leaf = self.pickLeaf()
            if self.debug:
                print("\treading from path ", leaf)

            return self.treeAccess(action, segIDList, dataList, leaf, newLeaf)
    
    def pickLeaf(self):
        newLeaf=self._tree.ringLeaf()
        #newLeaf = self._tree.randomLeaf()
        
        return newLeaf
    
    def treeAccess(self, action, segIDList, dataList, leaf, newLeaf):
        transfer = self._tree.readPath(leaf)
        result = dataList

        for bucket in transfer:
            for block in bucket:
                if self.debug:
                    print("\t\t", block.getLeaf(), block.getSegID(), block.getData())
                if block.getSegID() != 0:
                    if block.getSegID() in segIDList:
                        ind = segIDList.index(block.getSegID())
                        if action == "write":
                            block.setData(dataList[ind])
                            result[ind] = None
                        else:
                            result[ind] = block.getData()
                        if action == "read" or action == "write":
                            block.setLeaf(newLeaf)
                            self._posMap.insert(segIDList[ind], block.getLeaf())
                        if action != "delete":
                            self._stash.addNode(block)
                        else:
                            self._posMap.delete(segIDList[ind])
                            self._segCounter -= 1
                    else:
                        block.setLeaf(self._posMap.lookup(block.getSegID()))
                        self._stash.addNode(block)
            if self.debug:
                print("")
                    
        for i in range(len(segIDList)):
            if result[i] != None and action == "write":
                newBlock = Block.Block(newLeaf, segIDList[i], dataList[i])
                self._stash.addNode(newBlock)
                self._posMap.insert(segIDList[i], newLeaf)
                self._segCounter += 1
                result[i] = None
                if self.debug:
                    print("new block inserted")
                
        outPath = self._stash.evict(leaf)
        if self.debug:
            print("\twriting to path", leaf)
            for bucket in outPath:
                for block in bucket:
                    print("\t\t", block.getLeaf(), block.getSegID(), block.getData())
                print("")
        self._tree.writePath(leaf, outPath)
        return result

    def read(self, segID):
        return self.access("read", [segID], [None])[0]

    def write(self, segID, data):
        return self.access("write", [segID], [data])

    def delete(self, segID):
        return self.access("delete", [segID], [None])

    def multiRead(self, segIDList):
        return self.access("read", segIDList, [None] * len(segIDList))

    def multiWrite(self, segIDList, dataList):
        return self.access("write", segIDList, dataList)

    def multiDelete(self, segIDList):
        return self.access("delete", segIDList, [None] * len(segIDList))    

    def setPosMap(self, dictionary):
        self._posMap.setMap(dictionary)

    def getPosMap(self):
        return self._posMap

    def setStash(self, nodes):
        self._stash.setNodes(nodes)

    def getStash(self):
        return self._stash
