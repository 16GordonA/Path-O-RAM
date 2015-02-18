from Crypto.Cipher import AES
from Crypto.Util import strxor, Counter
from random import randint
import os

def mask(key, maskNum):
    cipher = AES.new(key, AES.MODE_ECB) 
    return cipher.encrypt(maskNum)

def decrypt(data, key):	# I modified this function to match the change in write(). Look at write() for explanation
    seed = int.from_bytes(data[0:16], byteorder="big")
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128, initial_value=seed))
    result = cipher.decrypt(data[16:])	  
    return result

def encrypt(data, key): #lots of comments in Nathan's but I cut them out because... they were just comments
	# With this version, it is even hard to tell whether encryption is on or off! (PyCrypto did a great job!)
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128, initial_value=seed))
    result += cipher.encrypt(data)
    return result
