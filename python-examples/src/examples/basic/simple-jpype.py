from jpype import *
import os

def initJVM():
    JAVA_HOME = os.environ['JAVA_HOME']
    CLASSPATH = os.environ['CLASSPATH']
    javaArgs = "-Djava.class.path=" + CLASSPATH
    #javaArgs = ""
    print "Java VM Arguments are: " + javaArgs
    startJVM(JAVA_HOME + "/jre/lib/i386/client/libjvm.so",javaArgs)
    java.lang.System.out.println("Started JVM")

initJVM()

ArrayList = JClass("java.util.ArrayList")
myList = ArrayList()
myList.add(2);
myList.add(3);
it = myList.iterator()

while(it.hasNext()):
    print it.next();

Util = JPackage("java.util")
HashMap = Util.HashMap
myMap = HashMap()
myMap.put(1,"Hello World")
print myMap.get(1)

shutdownJVM()