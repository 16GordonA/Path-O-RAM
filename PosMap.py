import Util
import random

class PosMap :

    def __init__(self):
        self._posMap = {}

    def lookup(self, segID) :
        if not segID in self._posMap:
            return -1
        return self._posMap[segID]

    def insert(self, segID, leaf):
        self._posMap[segID] = leaf

    def delete(self, segID):
        del self._posMap[segID]

    def correctLeaves(self, treeSize):
        for segID in self._posMap:
            newLeaf = Util.correctLeaf(self._posMap[segID], treeSize, segID % 2)
            if newLeaf != None:
                self._posMap[segID] = newLeaf

    def randomSegID(self):
        return random.choice(list(self._posMap.keys()))

    def setMap(self, dictionary):
        self._posMap = dictionary

    def getMap(self):
        return self._posMap
