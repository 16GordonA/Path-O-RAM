import random
import math

#utility functions

def levelNumber(leaf):#returns the level a leaf is on (used in getMaxLevel)
	#print ("Leaf is " + str(leaf))
	a = int(math.log(leaf,2))
	if(leaf == 2**a):
		return a #- 1
	return a
def revBin(num): #reversed binary of non-binary num
	return int(bin(num)[::-1][:-2],2) #what does this notation mean?

def getMaxLevel(leaf1, leaf2):
	#print (str(leaf1) + " and " + str(leaf2))
	if levelNumber(leaf1) > levelNumber(leaf2):
		return levelNumber(leaf1)
		leaf1 = leaf1 >> 1
	elif levelNumber(leaf1) < levelNumber(leaf2):
		return levelNumber(leaf2)
		leaf2 = leaf2>>1
#how does this ensure that they are on the same level? what if one is 2 higher than the next
	if leaf1==leaf2:
		return levelNumber(leaf1);

	else:
		leaf1=revBin(leaf1)
		leaf2=revBin(leaf2)
		diff = leaf1^leaf2 #bitwise difference
		t = (diff & (-diff))-1
		assert t>0, "t = " + str(t)
		return int(math.log(t,2))


def getPathNodes(leaf):
	result = []
	while (leaf>0):
		result.insert(0,leaf)
		leaf = leaf>>1
	return result

def correctLeaf(leaf, treeSize, bit):
    assert (leaf != 0), "0 leaf"
    newLeaf = leaf
    while newLeaf < int(treeSize / 2) + 1:
        newLeaf = (newLeaf * 2) + bit
    while newLeaf > treeSize:
        newLeaf = int(newLeaf / 2)
    if newLeaf != leaf:
        return newLeaf