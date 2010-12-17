
#Define the callable class object
class CallableClass:
    def __call__(self, args):
        print args
    pass

#bind the class callback
def myCallback():
    print "Hello from CallableClass"

callable_class = CallableClass()
callable_class(['arg1', 'arg2'])