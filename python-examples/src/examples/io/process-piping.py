from subprocess import Popen,PIPE
from random import randint

#Write output of echo to a file
echo_out = open("echo-output",'w')
Popen("echo Hello World",shell=True, stdout=echo_out)
echo_out.close()

ls_error_out = open("ls-error-out",'w')
Popen("ls asdfasdfasdf", shell=True,stderr=ls_error_out)
ls_error_out.close()

message = "Hello, my name is matt"
popen = Popen("grep Hello" ,shell=True,stdin=PIPE)
grep_input = popen.stdin 

grep_input.write(message);