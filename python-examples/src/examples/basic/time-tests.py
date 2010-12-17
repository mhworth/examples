from time import localtime,strftime,time

#Get seconds since the "epoch"
print time()

#Get the date in the form (year, month, day)
print localtime()[0:3]

#Get the time in the form (hour, minute, second)
print localtime()[3:6]

#Get a nicely formatted time
print strftime("%m-%d-%Y", localtime())

