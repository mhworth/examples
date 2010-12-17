class DictPublisher(object):
        def __init__(self,d):
                for (k,v) in d.items():
                        self.__setattr__(k,v)

def find_home(globals):
    file = globals["__file__"]
    home = os.path.abspath(os.path.split(file)[0])
    return home
