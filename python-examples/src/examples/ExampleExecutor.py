import examples.basic
import string
import os
import sys

def execute(modname):
    
    path_info = string.split(modname,".")
    path = join_path_list(path_info)
    
    #loop through the sys path and see if we can open up the file to print it
    for p in sys.path:
    
        try:
            script_path = p + "/" + path + ".py"
            script_file = open(script_path)
            
            for l in script_file:
                print l[:-1]
            script_file.close()
            break
        except IOError, e:
            pass
        try:
            script_path = p + "/" + path + ".pyw"
            script_file = open(script_path)
            for l in script_file:
                print l[:-1]
            script_file.close()
            break
        except IOError,e:
            pass
    
    print "\n\n\nExecuting " + modname + "\n\n\n"
    mod = __import__(modname)
    return mod

def join_path_list(path_list):
    tmp = ""
    counter = 0
    tmp = path_list[0]
    for p in path_list:
       
        if counter == (len(path_list) - 1):
            return tmp
        else:
            tmp = os.path.join(tmp, path_list[counter+1])
            counter += 1

execute("examples.basic.SearchLists")
#execute("examples.basic.SearchList")