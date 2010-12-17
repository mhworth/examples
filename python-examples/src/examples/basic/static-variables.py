"""Demonstrates how to make a "static variable" in python"""

class MyClass:
    @staticmethod
    def setStaticVariable(var):
        MyClass.getStaticVariable.var = var
    @staticmethod
    def getStaticVariable():
        return MyClass.getStaticVariable.var
        
#initialize variable

if (not MyClass.getStaticVariable.__dict__.has_key("var")):
    MyClass.getStaticVariable.var = "Initial Value"
    
if(__name__ == "__main__"):
    print MyClass.getStaticVariable()
    MyClass.setStaticVariable("New var")
    if (not MyClass.getStaticVariable.__dict__.has_key("var")):
        MyClass.getStaticVariable.var = "Initial Value"
    print MyClass.getStaticVariable()