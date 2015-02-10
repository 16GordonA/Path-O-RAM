import random
import math

#utility functions

def levelNumber(leaf):#returns the level a leaf is on (used in getMaxLevel)
	return int(math.log(leaf,2))

def revBin(num): #reversed binary of non-binary num
	return int(bin(num)[::-1][:-2],2) #what does this notation mean?

def getMaxLevel(leaf1, leaf2):
	if levelNumber(leaf1) > levelNumber(leaf2):
		leaf1  =leaf1 >> 1
		#todo