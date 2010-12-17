"""
sconsx.py

This module is meant to be sourced in via an SCons script.
It is basically a collection of all the useful SCons functions/classes/etc
that I have used in scons over time.
"""
import os,sys,re
import distutils.sysconfig
import SCons


if os.name == "posix":
    INCLUDE_LOCATIONS = ["/include","/usr/include","/usr/local/include"]
    LIB_LOCATIONS = ["/lib","/usr/lib","/usr/local/lib"]
    LIB_PATTERN = "lib%s.so"
else:
    INCLUDE_LOCATIONS = []
    LIB_LOCATIONS = []
    LIB_PATTERN = "%s.dll"
    
class Sconsx:
    """
    The base class for sconsx
    """
    def __init__(self):
        pass
    def get_home(self,glbs):
        if glbs:
            return os.path.split(glbs["__file__"])[0]
        else:
            return os.path.split(__file__)[0]

class SconsxError(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.msg
    
class Builder(Sconsx):
    """
    Another builder
    """
    def __init__(self,env=None):
        Sconsx.__init__(self)
        self._env = env


class Configurer(Sconsx):
    """
    A high-level interface to the Configure package.  Just pass
    a Configure() object to the init.
    """
    def __init__(self,conf):
        Sconsx.__init__(self)
        self._conf = conf
        self._libs = []
        self._headers = []
        self._files = []
        self._header_locations = []
        self._lib_locations = []
        self._file_locations = []
        
    def add_lib(self,lib,required=True):
        ""
        self._libs.append((str(lib),required))
    
    def add_header(self,header,required=True):
        ""
        self._headers.append((str(header),required))
    
    def add_file(self,file,required=True):
        ""
        self._files.append((str(file),required))
    
    def add_header_location(self,location):
        ""
        if not location in self._header_locations:
            self._header_locations.append(location)
    
    def add_lib_location(self,location):
        ""
        if not location in self._lib_locations:
            self._lib_locations.append(location)
    
    def add_file_location(self,location):
        ""
        if not location in self._file_locations:
            self._file_locations.append(location)
        
    def find_header(self,header,locations):
        """
        locations is a list of possible locations for the header file to
        be
        
        This function will either return None if it isn't found, or
        the path to the file that it found.
        
        Priority is given by order.... the last ones override the 
        early ones
        """
        ret = None
        
        locations = locations[:]
        locations.reverse()
        for location in locations:
            full_path = os.path.join(location,header)
            if os.path.exists(full_path):
                ret = full_path
                break
        
        return ret
    
    def find_lib(self,lib,locations):
        """
        locations is a list of possible locations for the header file to
        be
        
        This function will either return None if it isn't found, or
        the path to the file that it found.
        """
        ret = None
        
        locations = locations[:]
        locations.reverse()
        for location in locations:
            full_path = os.path.join(location,LIB_PATTERN % lib)
            if os.path.exists(full_path):
                ret = full_path
                break
        
        return ret
    
    def find_file(self,file,locations):
        """
        locations is a list of possible locations for the header file to
        be
        
        This function will either return None if it isn't found, or
        the path to the file that it found.
        """
        ret = None
        
        locations = locations[:]
        locations.reverse()
        for location in locations:
            full_path = os.path.join(location,file)
            if os.path.exists(full_path):
                ret = full_path
                break
        
        return ret
    def configure(self):
        "Runs all the checks and returns the proper env"
        conf = self._conf
        successes = []
        failures = []
        
        # Initialize CPPPATH
        try:
            conf.env["CPPPATH"]
        except:
            conf.env["CPPPATH"] = []
        
        # Initialize LIBPATH
        try:
            conf.env["LIBPATH"]
        except:
            conf.env["LIBPATH"] = []
        
        self.check_headers()
        self.check_libs()
        self.check_files()
        
        return self._conf
        
    def check_headers(self):
        ""
        conf = self._conf
        successes = []
        failures = []
        
        for header in self._headers:
            found = self.find_header(header[0],self._header_locations)
            if found:
                if not found in conf.env["CPPPATH"]:
                    conf.env["CPPPATH"].append(found.replace(header[0],""))
            
            try: conf.CheckCXXHeader(header[0]);successes.append(header)
            except: 
                if header[1]: failures.append(header[0])
        
        for success in successes:
            print "Success: %s" % str(success)
        for failure in failures:
            print "Failure: %s" % str(failure)
        
    def check_libs(self):
        ""
        conf = self._conf
        successes = []
        failures = []
        
        for lib in self._libs:
            found = self.find_lib(lib[0],self._lib_locations)
            if found:
                if not found in conf.env["CPPPATH"]:
                    conf.env["CPPPATH"].append(found.replace(lib[0],""))
            try: conf.CheckLib(lib[0]);successes.append(lib[0])
            except: 
                if header[1]: failures.append(header[0])
        
        for success in successes:
            print "Success: %s" % str(success)
        for failure in failures:
            print "Failure: %s" % str(failure)
            
    def check_files(self):
        ""


class SwigBuilder(Sconsx):
    
    def __init__(self):
        Sconsx.__init__(self)
        self.i_files = []
        
    def add_i_file(self,i_file):
        self.i_files.append(i_file)

class Installer(Sconsx):
    """ A basic installer. """
    PREFIX = "prefix"
    EPREFIX = "eprefix"
    BINDIR = "bindir"
    LIBDIR = "libdir"
    INCLUDEDIR = "includedir"
    def __init__( self, env ):
        """ Initialize the installer.

        @param configuration A dictionary containing the configuration.
        @param env The installation environment.
        """
        Sconsx.__init__(self)
        self._prefix = env.get( PREFIX, "/usr" )
        self._eprefix = env.get( EPREFIX, self._prefix )
        self._bindir = env.get( BINDIR, os.path.join( self._eprefix, "bin" ) )
        self._libdir = env.get( LIBDIR, os.path.join( self._eprefix, "lib" ) )
        self._includedir = env.get( INCLUDEDIR, os.path.join( self._prefix, "include" ) )
        self._env = env
	self._installs = []
    

    def AddOptions( opts ):
            """ Adds the installer options to the opts.  """
            opts.Add( PREFIX, "Directory of architecture independant files.", "/usr" )
            opts.Add( EPREFIX, "Directory of architecture dependant files.", "${%s}" % PREFIX )
            opts.Add( BINDIR, "Directory of executables.", "${%s}/bin" % EPREFIX )
            opts.Add( LIBDIR, "Directory of libraries.", "${%s}/lib" % EPREFIX )
            opts.Add( INCLUDEDIR, "Directory of header files.", "${%s}/include" % PREFIX )
    
    def Add( self, destdir, name, basedir="", perm=0644 ):
        destination = os.path.join( destdir, basedir )
        obj = self._env.Install( destination, name )
	self._installs.append(obj)
        #self._env.Alias( "install", destination )
        for i in obj:
            self._env.AddPostAction( i, SCons.Defaults.Chmod( str(i), perm ) )

    def AddProgram( self, program ):
        """ Install a program.

        @param program The program to install.
        """
        self.Add( self._bindir, program, perm=0755 )

    def AddLibrary( self, library ):
        """ Install a library.

        @param library the library to install.
        """
        self.Add( self._libdir, library )

    def AddHeader( self, header, basedir="" ):
        self.Add( self._includedir, header, basedir )

    def AddHeaders( self, parent, pattern, basedir="", recursive=False ):
        """ Installs a set of headers.

        @param parent The parent directory of the headers.
        @param pattern A pattern to identify the files that are headers.
        @param basedir The subdirectory in which to install the headers.
        @param recursive Search recursively for headers.
        """
        for entry in os.listdir( parent ):
            entrypath = os.path.join( parent, entry )
            if os.path.isfile( entrypath ) and fnmatch.fnmatch( entry, pattern ):
                self.AddHeader( entrypath, basedir )
            elif os.path.isdir( entrypath ) and recursive:
                self.AddHeaders( entrypath, pattern, os.path.join( basedir, entry ), recursive )
    def getInstalls(self):
	return self._installs
