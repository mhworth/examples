#Make an exception class
class MyException:
    def __init__(self, message):
        self.__message__ = message;
    def __str__(self):
        return self.__message__;
    
def raiseException():
    raise MyException("Here's an exception!")

try:
    raiseException()
except MyException, e:
    print "MyException occured!"
    print e