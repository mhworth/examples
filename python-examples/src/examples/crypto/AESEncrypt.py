from Crypto.Cipher import AES
from getpass import getpass
from tempfile import TemporaryFile
from random import randrange
import string
from StringIO import StringIO
import sys

BLOCK_SIZE = 16

def writePad(input,desired_length=BLOCK_SIZE):
    if(len(input)==desired_length):
        return input
    else:
        #Figure out how far off the string is from being a multiple of the block length
        length = len(input)
        num_bytes = desired_length - (length % desired_length)
        
        #Pad the string, but leave a byte left over that can specify the number of bad bytes
        for i in range(num_bytes-1):
            input+=chr(randrange(8,248))
        
        #Finish it up with a flag
        rand = randrange(8,248)
        pad_flag = rand - (rand % desired_length) + num_bytes
        
        input+=chr(pad_flag)
        print "String length = " + str(len(input))
        return input
        
def removePad(input, desired_length=BLOCK_SIZE):
    if (len(input)==desired_length):
        return input
    pad_flag = ord(str[-1])
    num_pad_bytes = pad_flag % 8
    input = input[:-num_pad_bytes]
    return input

def encrypt(password,infile,outfile):
    block_size = BLOCK_SIZE
    
    #Get the cipher object, using the specified pass
    cipher = AES.new(password)
    while(True):
        input = infile.read(block_size)
        if (input==""):
            break
        input = writePad(input,block_size)
        print "String size: " + str(len(input))
        outfile.write(cipher.encrypt(input))
        
    #Just in case someone wants to do something else with the files
    infile.seek(0)
    outfile.seek(0)
    
def decrypt(password,infile,outfile):
    block_size = BLOCK_SIZE
    cipher = AES.new(password)
    
    while(True):
        input = infile.read(block_size)
        if (input==""):
            break
        input = removePad(input,block_size)
        outfile.write(cipher.decrypt(input))
        
    #just in case someone wants to do something else with the files
    infile.seek(0)
    outfile.seek(0)
    
def getPassword(desired_length=BLOCK_SIZE):
    password = getpass()
    if(len(password)==desired_length):
        return password
    num_pad_bytes = desired_length - (len(password) % desired_length)
    for i in range(num_pad_bytes):
        password+=chr(100)
    return password
#Create some temporary files, just to demonstrate how one could encrypt large files if need be
tmp_out = TemporaryFile()
tmp_in = TemporaryFile()

#Get the password
print "Please input an encryption password"
password=getPassword(BLOCK_SIZE)
print "Password length is " + str(len(password))
print "Your password was: " + password

#Get a line to encrypt... could be any string, including a buffered file
print "Input a line to encrypt"
buf = sys.stdin.readline()

#Give it some stuff to encrypt
for i in range(100):
    tmp_in.write(buf)
    
tmp_in.seek(0)

#Encrypt tmp_in
encrypt(password,tmp_in,tmp_out)

#print it
while(True):
    char = tmp_out.read(1)
    if(char==""):
        break
    print str(ord(char))
    
tmp_out.seek(0)

#Decrypt it
print "Please input a decryption password"
password = getPassword(BLOCK_SIZE)

sio = StringIO()
decrypt(password,tmp_out, sio)

#print it
for line in sio:
    print string.strip(line)
