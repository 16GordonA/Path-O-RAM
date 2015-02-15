import Oram
import UserFileSys
import random
import time
import os
import shutil
import cProfile
import Encryptor
import pickle

from os.path import expanduser
home = expanduser("~")

key = "16characterslong"


def TestBasic() :
    oramsize = 1 << 4 - 1
    oram = Oram.Oram(oramsize, 4, 100)
    for key in range(0, oramsize) :
        oram.write(key, str(key))
    for key in range(0, oramsize) :
        try :
            getvalue = oram.read(key).decode("utf-8")
            assert (getvalue == str(key))
        except :
            print( "[TestBasic] key=%d. expecting %s but got %s" % (key, str(key), getvalue) )
            print( "TestBasic failed." )

        print(oram._stash.getSize())
    print( "TestBasic Passed." )

def TestRepeatRW() :
    oramsize = 1 << 4 - 1
    oram = Oram.Oram(oramsize, 4, 100)
    db = {}
    for key in range(0, oramsize) :
        oram.write(key, str(key))
    for key in range(0, oramsize) :
        try :
            getvalue = oram.read(key).decode("utf-8")
            assert (getvalue == str(key))
            oram.write(key, 'v')
        except :
            print( "[TestRepeatRW] key=%d. expecting %s but got %s" % (key, str(key), getvalue) )
            return
    

def TestGeneral() :
	
    random.seed(1)	# this guarantees we get the same random numbers, and thus same results on every run
					# Comment: When you fixed this bug, remove the previous line so you can test with random input again.
	
    oramsize = 101
    #minoramsize = 7
    z = 3
    maxStashSize = 30
    segSize = 4096
    oram = Oram.Oram(oramsize, z, segSize, maxStashSize, 1.8, 2, 2.2)
    
    check  = {}
    numKeys = 1000
    numTests = 1000
    
    lastStashSize = 0
    currentStashSize = 0
	
    for key in range(1, numKeys) :                 # writes a "random" string to each key from 0 to N
        data = "v" + str(random.randint(1,1000))
        oram.write(key, data)
        check[key] = data	
		
        currentStashSize = oram._stash.getSize()
        #print ("ORAM Stash Size: ", currentStashSize)		
        if 	currentStashSize - lastStashSize > 1:
            print("Stash increases by more than 1")			
            exit(0)
        lastStashSize = currentStashSize			
    
    start = time.clock()    
    for i in range(0, numTests):        # does a random operation
        operation = random.random()
        key = random.randint(1, numKeys-1)
        # if ((operation * 10) % 1 < .1):
        #     oram.grow(2)
        #     oramsize += 2
        # elif ((operation * 10) % 1 < .2 and oramsize > minoramsize):
        #     oram.shrink(2)
        #     oramsize -= 2
        if (operation < .2):
            data = "x" + str(random.randint(1,1000))
            oram.write(key, data)
            check[key] = data

        elif (operation <.6):
            if (check[key] != ""):
                try:
                    getValue = oram.read(key).decode("utf-8")	
                    assert (getValue == check[key])
                except:
                    print( "[TestGeneral] key=%d. expecting %s but got %s" % (key, check[key], getValue) )
                    return

        else:
            if (check[key] != ""):
                oram.delete(key)
                check[key] = ""
        
        currentStashSize = oram._stash.getSize()
        #print ("ORAM Stash Size: ", currentStashSize)		
        # if currentStashSize - lastStashSize > 1:
        #     print("Stash increases by more than 1")			
        #     exit(0)
            
        lastStashSize = currentStashSize
    
    timeTaken = time.clock() - start   
    print("final stash size:", currentStashSize)
    print("Elapsed time: " + str(timeTaken))
    print("TestGeneral Passed")

def TestBackEv():
    oramsize = 4095
    segSize = 100
    z = 2
    
    #numKeys = 64
    #numTests = 10000
    
    print ("z = " + str(z) + ", oram size = " + str(oramsize))
    numKeys = int(oramsize*z / 2)
    for maxStashSize in range(5, 50, 5):
        oram = Oram.Oram(oramsize, z, segSize, maxStashSize, 1.8, 2.0, 2.2)
        numBackEv = 0
        for key in range(1, numKeys+1) :                 # writes a "random" string to each key from 0 to N
            while (oram._stash.getSize() > oram._c):
                oram.access("backEv", 0, None)
                #print ("backEv")
                numBackEv+=1
            data = "v" + str(random.randint(1,1000))
            oram.write(key, data)			
        
        for i in range (oramsize*2):
            key = i%numKeys + 1
            while (oram._stash.getSize() > oram._c):
                oram.access("backEv", 0, None)
                numBackEv+=1
            oram.read(key)

        print ("\tMax Stash Size = " + str(maxStashSize) + ": dummy- " + str(numBackEv) + ", actual- " + str(2*oramsize + numKeys))
        print ("\t\tRatio = " + str(numBackEv / (2*oramsize + numKeys)))

def createTestFile(size):
    file = open("TestFiles/test" + str(size) + ".txt", "w")
    file.write('0' * size * 1024)
    file.close()			
		
def ORAMvsNormal():
    numTests = 1000
    oram = UserFileSys.UserFileSys(1301, 3, 65536, 100, 1.8, 2.0, 2.2, 1)
    oram._oram.autoResize = False
	
    for i in range (2,13):
        createTestFile(1 << i)		
        oram.write("TestFiles/test" + str(1 << i) + ".txt")
        
    total = 0
    totalSize = 0
    for i in range(numTests):
        fileName = getFile()
        totalSize += int(fileName[14:fileName.index(".")])
        start = time.clock()
        oram.read(fileName)
        timeTaken = time.clock() - start    
        total += timeTaken
    print(total)
    print ("Throughput Disk + ORAM + Encryption: " + str(totalSize/total))


    total = 0
    totalSize = 0
    for i in range(numTests):
        fileName = getFile()
        totalSize += int(fileName[14:fileName.index(".")])
        inputFile = open(fileName, "rb")
        data = inputFile.read()
        inputFile.close()
        start = time.clock()
        data = Encryptor.encrypt(data, key)
        outputFile = open(fileName[:-4] + "_encrypted.txt", "wb")
        pickle.dump(data, outputFile)
        outputFile.close()
        inputFile = open(fileName[:-4] + "_encrypted.txt", "rb")
        data = pickle.load(inputFile)
        inputFile.close()
        data = Encryptor.decrypt(data, key)
        timeTaken = time.clock() - start
        total += timeTaken
    print(total)
    print("Throughput Disk + Encryption: " + str(totalSize/total))

        
    total = 0
    totalSize = 0
    for i in range(numTests):
        start = time.clock()
        fileName = getFile()
        totalSize += int(fileName[14:fileName.index(".")])
        file = open(fileName, "r")
        data = file.read()
        file.close()
        file = open(fileName, "w")
        file.write(data)
        file.close()		
        total += (time.clock()-start)
    avg = total/numTests
    print(total)
    print ("Throughput Disk: " + str(totalSize/total))

    
def TestSegSize():    # optimal = 64kB
    numTests = 1000
    segSize = 1024 * 8
    while segSize <= 1024 * 2048:
        total = 0
        totalSize = 0
        oram = UserFileSys.UserFileSys(1301, 3, segSize, 100, 1.8, 2.0, 2.2, 1)
        oram._oram.autoResize = False
        for i in range (2,13):
            createTestFile(1 << i)		
            oram.write("TestFiles/test" + str(1 << i) + ".txt")
            
        for i in range(numTests):
            fileName = getFile()
            totalSize += int(fileName[14:fileName.index(".")])
            start = time.clock()
            oram.read(fileName)
            timeTaken = time.clock() - start
            total+=timeTaken
            
        print(str(segSize) + " " + str(totalSize/total))
        segSize *= 2

def TestMultiBlock():
    numTrials = 1000
    numTests = 5
    for i in range(1, numTests+1):
        total = 0
        totalSize = 0
        oram = UserFileSys.UserFileSys(101, 3, 65536, 10, 1.8, 2.0, 2.2, i)
        oram._oram.autoResize = False
        for k in range (2,13):
            createTestFile(1 << k)		
            oram.write("TestFiles/test" + str(1 << k) + ".txt")
            
        for j in range(numTrials):
            fileName = getFile()
            totalSize += int(fileName[14:fileName.index(".")])
            start = time.clock()
            oram.read(fileName)
            timeTaken = time.clock() - start
            total+=timeTaken
            
        print(str(i) + ": " + str(totalSize/total))

def TestBlockPack(testFile):
    #random.seed(5)
    numTests = 100
    totalSize = 0
    oram = UserFileSys.UserFileSys(201, 3, 65536, 100, 1.8, 2.0, 2.2, 1)            # change segSize, and write appropriate file
    for i in range(0, numTests):
        shutil.copyfile(testFile, testFile + "_" + str(i) + ".txt")
        totalSize += int(testFile[14:testFile.index(".")])

    for i in range(0, numTests):
        oram.write(testFile + "_" + str(i) + ".txt")
        
    start = time.clock()
    for i in range(numTests):
        oram.read(testFile + "_" + str(i) + ".txt")
    timeTaken = time.clock() - start
    print("Without Block Packing: " + str(oram._oram._tree.getSize()) + "  " + str(totalSize/timeTaken))


    oram = UserFileSys.UserFileSys(201, 3, 65536, 100, 1.8, 2.0, 2.2, 1)
    oram.blockPack = True

    for i in range(0, numTests):
        oram.write(testFile + "_" + str(i) + ".txt")
    start = time.clock()
    for i in range(numTests):
        oram.read(testFile + "_" + str(i) + ".txt")
    timeTaken = time.clock() - start
    print("With Block Packing: " + str(oram._oram._tree.getSize()) + "  " + str(totalSize/timeTaken))
    
def TestGrowShrink(version):
    if version == "utilization":
        numTests = 1000
        
        for j in range(numTests):
            shutil.copyfile("test32.txt", "test32_" + str(j) + ".txt")
            
        for i in range(3):
            if i==0:   # 0.45 - 0.55
                oram = UserFileSys.UserFileSys(3, 3, 65536, 100, 1.8, 2.0, 2.2, 1)
            elif i==1:  #0.42 - 0.58
                oram = UserFileSys.UserFileSys(3, 3, 65536, 100, 1.72, 2.0, 2.38, 1)
            elif i==2:  #0.48 - 0.52
                oram = UserFileSys.UserFileSys(3, 3, 65536, 100, 1.92, 2.0, 2.08, 1)

            start = time.clock()
            for j in range(numTests):
                oram.write("test32_" + str(j) + ".txt")
            timeTaken = time.clock() - start

            print(str(i) + " " + str(timeTaken))

    if version == "overhead":
        numTests = 1000
        for i in range(numTests):
            shutil.copyfile("TestFiles/test64.txt", "TestFiles/test64_" + str(i) + ".txt")

        oram = UserFileSys.UserFileSys(3, 3, 65536, 100, 1.8, 2.0, 2.2, 1)
        start = time.clock()
        for i in range(numTests):
            oram.write("TestFiles/test64_" + str(i) + ".txt")
        timeTaken = time.clock() - start
        avgGrowthTime = oram._oram._tree.totalTimeGrowth / oram._oram._tree.numGrowth
        print("Avg growth time: " + str(avgGrowthTime))
        print("Auto Resize ON: " + str(timeTaken))

        oram = UserFileSys.UserFileSys(1501, 3, 65536, 100, 1.8, 2.0, 2.2, 1)
        oram._oram.autoResize = False
        start = time.clock()
        for i in range(numTests):
            oram.write("TestFiles/test64_" + str(i) + ".txt")
        timeTaken = time.clock() - start
        print("Auto Resize OFF: " + str(timeTaken))
                

    
def getFile():     # returns name of file based on distribution graph
    prob = random.random()
    probTable = [0.0, 0.5, 0.6, 0.8, 0.9, 0.92, 0.95, 0.97, 0.98, 0.99, 0.995, 1.0]
    for i in range(len(probTable)-1):
        if prob	>= probTable[i] and prob < probTable[i+1]:
            return ("TestFiles/test" + str(4 << i) + ".txt")

def TestVCache():
    oram = UserFileSys.UserFileSys(101, 3, 4096, 100, 1.8, 2.0, 2.2, 1)
    for i in range(1000):
        shutil.copyfile("test4.txt", "test4_" + str(i) + ".txt")
        oram.write("test4_" + str(i) + ".txt")
        oram.read("test4_" + str(i) + ".txt")

    print(oram._oram.VCacheCounter)
    print(oram._oram.totalCounter)

def PlotGS():
    oram = UserFileSys.UserFileSys(3, 3, 4096, 100, 1.8, 2.0, 2.2, 1)
    numTests = 32
    files = []
    for i in range(numTests):
        rand = random.random()
        if len(files) > 0 and rand < 0.4:
            target = random.choice(files)
            files.remove(target)
            oram.delete("temp/" + str(target) + ".txt")
        else:
            files.append(i)
            os.system("cp " + getFile() + " temp/" + str(i) + ".txt")
            oram.write("temp/" + str(i) + ".txt")
        print(i)
    oram._oram.GSOut.close()
 
#TestBasic()
#TestRepeatRW()
#TestGeneral()
#cProfile.run('TestGeneral()')
#TestBackEv()
#cProfile.run('ORAMvsNormal()')
# ORAMvsNormal()
# print()
# TestSegSize()
# print()
# TestMultiBlock()
# print()
TestBlockPack("TestFiles/test16.txt")
# TestBlockPack("TestFiles/test32.txt")
# TestBlockPack("TestFiles/test70.txt")
#TestGrowShrink("overhead")
#PlotGS()
