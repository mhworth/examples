import tarfile
import os
import string
from random import randint

#Get a temporary file (when it goes out of scope, it is deleted)
tmp_file = os.tmpfile()

#Get a "normal" file
normal_file = open("normal-file.txt","w+b")

#Write some random data to the file
for i in range(5):
    tmp_file.write(str(randint(0,10)) + "\n");
    normal_file.write("hi" + str(i) + "\n")

#necessary to seek back to the beginning to prepare for reading
tmp_file.seek(0)
normal_file.seek(0)

#Create a new tar file in write: gzip mode
#Other available modes:
#    r or r:* opens for "transparent" decompression, read only
#    r: open explictly for compressionless reading
#    r:gz, r:bz2 open for gzip and bzip2 reading respectively
#    a or a: opens for appending with no compression
#    w, w: opens for uncompressed writing
#    w:gz, w:bz2 opens for gzip and bzip2 compression writing, respectively
filename = "sample-tar.tar.gz"
tar = tarfile.open(filename,"w:gz")

#Get a tar info object by the name of "random-file" that will be in the directory called "random" in the tarfile
rnd_info = tar.gettarinfo(fileobj=tmp_file, arcname="random-file.txt")
normal_info = tar.gettarinfo(fileobj=normal_file)

#Write the file pointed to by the TarInfo object
#tar.addfile(rnd_info)
tar.addfile(rnd_info, tmp_file)
tar.addfile(normal_info, normal_file)

#close the streams
tar.close()
tmp_file.close()
normal_file.close()

#Open it up again and print out its contents
tar = tarfile.open(filename,"r")
tar.list(verbose=True)
tar.close()

#delete the tarfile
#os.remove(filename)
