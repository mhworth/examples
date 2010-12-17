"""
This module defines a number of utilities that are useful
for executing command-line commands.

The main class is the CommandExecutor, which defines the method
execute(command,arg_spec,stdout,stderr,stdin,kwargs**).

"""

import os,sys,re
from subprocess import Popen,PIPE
from logging import Logger

logger = Logger(__name__)
logger.disabled = True #Keep the logging off by default

class CommandError(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.msg
    
class ICommandExecutor:
    """
    An interface for an object that may execute commands.
    
    :Author: Matt Hollingsworth
    :Date: 8-6-2008
    
    """
    def execute(self,command_to_execute,arg_spec,stdout,stderr,stdin,**kwargs):
        """
        Executes a command given the proper parameters.
        
        :Parameters:
            - command_to_execute : (string)
                The command to execute.  Should be only one string which specifies the 
                executable command (the program to execute.  Arguments should
                be given using keyword arguments
            - arg_spec : string
                A spec string for the arguments that are to be passed
                to the executed command.  It specifies the way that the
                keyword args are turned into command line arguments.
                See the function parse_arg_spec() for an example and more 
                details.
            - stdout : file
                A file-like object to use for output
            - stdin : file
                A file-like object to use for input
            - stderr : file
                A file-like object to use for error output
            - kwargs 
                The keyword args to use as arguments for the command to execute
                These are turned into arguments using the arg_spec string
                (see parse_arg_spec() for more details on how this works).
                
                Basically, in order to pass arguments to a command, you will
                specify python keyword arguments like so:
                
                execute(command_to_execute="my_command",my_option="my value", my_multi_option=["my","multi","value])
                
                Which would execute (according to your arg_spec) somewhat like so:
                
                my_command --my_option "my value" --my_multi_option my --my_multi_option multi --my_multi_option value


            :Returns:
                tuple 
                    Returns a tuple that is of the form (stdout,stderr,stdin)
            """
            
    def parse_arg_spec(self,arg_spec,kwargs):
        """
        
        Parses an argument specification string, using the dictionary specified by
        the kwargs argument, and returns a list of the resulting arguments.
        
        An arg_spec string is a string that tells the execute() command
        how to turn python keyword arguments into options to be passed
        to a command.  The string contains a list of newline-seperated
        entries, each of which can either qualify one single argument, 
        or multiple arguments by specifying a regular expression to 
        match multiple keyword arguments.  Here is an example of an arg spec string:
        
        ?*command*
        my_option:--:optarg
        my_second_option:--:optarg:2
        .*:--:optarg:1
        
        So, lets say that the execute function was called with the following python keyword arguments:
        
        execute(command_to_execute="my-command", command="dump",my_option="my value",my_second_option=("a","b"),hello="value")
        
        The following would be the argument list that is constructed:
        
        my-command dump --my_option "my value" --my_second_option a b --hello value
        
        And the list that would be returned:
        ["dump","--my_option", "my value", "--my_second_option","a","b","--hello","value"]
        
        Now to describe what happened:
        
        A line in an argument specification can define one of two things:
        
        1) A argument (referred to as an argument entry)
        2) A option/argument pair  (referred to as an option entry)
        
        A named argument is simply a mapping between a python keyword argument
        and a command line argument.  If you define *command* as an argument spec entry,
        then the value of the "command" python keyword argument will be appended
        to the list of arguments.
        
        An option argument specifies a way of transforming the keyword argument's
        name and value into an arg entry.  It takes the form
        [?]<name>:<prefix>:[type]:[count]
        
        ([]'s denote optional entries)
        
        <name> is the name of the python keyword argument
        <prefix> is a part of what will be used to construct the actual argument
        [type] specifies the way that the name, value, prefix, and count all translate into an actual argument
        [count] is another modifier that means different things, according to the [type]
        
        There are four [type]'s available:
            optarg
            boolean
            compressed
            meta
            
        * optarg: will result in appending the following to the arg list:
            ["<prefix><name>", "value1","value2","valueN",...]
        where N = count.  This type will expect either a string or a tuple as
        an argument to the python keyword.  If it is a string, the series will
        terminate with just ["<prefix><name>", "value1"].  Otherwise, the
        parser will keep appending each part of the tuple to the arg list for
        [count] number of times.
        * boolean: only checks for the presence of the keyword, and then appends
        the following to the argument list:
            ["<prefix><name>"]
        The value of the python keyword argument is not checked.
        * compressed: similar to optarg, except only one value is possible
        (the python keyword value that is expected is a string), and the formatting
        is a bit different:
            ["<prefix><name><value>"]
        For example, prefix="-",name="D" and value="hi" would result in "-Dhi" being
        appended.
        * meta: Similar to compressed, except with an = sign:
            ["<prefix><name>=<value"]
        
        Order is important.  The order 
        in which the arguments will be passed to the command is determined
        by the order in which the argument specification defines them.  The parser
        reads each line, looks for any keyword arguments that match the line,
        and appends the appropriate results to the arg list.  This means you must
        be careful when constructing multiple regular expressions, as it is possible for
        an argument to be specified twice.  
        
        """
class CommandExecutor(ICommandExecutor,object):
    """
    
    :Author: Matt Hollingsworth
    :Date: 8-6-2008
    """
    def __init__(self):
        ""
        
    def execute(self,command_to_execute,arg_spec="*.**",stdout=sys.stdout,stderr=sys.stderr,stdin=sys.stdin,**kwargs):
        """
        Executes a command using pythons subprocess.Popen.
        
        If you wish, you may pass the keyword argument pass_to_shell=True in order
        to have the command_to_execute passed directly to a shell as-is.  Otherwise,
        you will need to provide a list of arguments by python keywords and argument
        specs.  See the documentation of ICommandExecutor for an explanation of
        argument specs.  
        """
        
        # Need to keep the interface intact, while still allowing users to pass it directly to the shell
        try:
            pass_to_shell = kwargs["pass_to_shell"]
        except:
            pass_to_shell = False
        
        args = self.parse_arg_spec(arg_spec,kwargs)
        
        logger.debug( "Executing %s %s" % (command_to_execute,"".join(args)))
        
        args.insert(0,command_to_execute)
        
        return Popen(args,shell=pass_to_shell,stdin=stdin,stdout=stdout,stderr=stderr)
        
    def parse_arg_spec(self,arg_spec,kwargs):
        """
        Parses an argument spec and returns the list of arguments as the result.
        
        >> kwargs = {"command" : "my_command", "my_option" : "my value",
        "my_multi_option" : ("a","b","c"),
        "random" : "rnd"}
        >> executor = CommandExecutor()
        >> arg_spec = \"""
            *command*
            my_option:--:optarg
            my_multi_option:--:optarg:3
            ?.*:--:optarg:1
        \"""
        >> args = executor.parse_arg_spec(arg_spec,kwargs)
        >> print args
        >> args == ["my_command","--my_option","my value","--my_multi_option","a","b","c","--random","rnd"]
        """
        
        # return value
        args = []
        
        # First, trim down the whitespace
        arg_spec = arg_spec.strip()
        
        logger.debug("Parsing the following arg spec:\n%s " % arg_spec)
        
        # Now, take each line and look in the kwargs for the appropriate keys
        optional_regex = re.compile(r"^\?(.*)")
        arg_regex = re.compile(r"\*(.*)\*")
        opt_regex = re.compile(r"(.*):(.*)")
        
        lines = arg_spec.split("\n")
        logger.debug("There are %s lines in this arg spec" % len(lines))
        for line in lines:
            line = line.strip()
            
            # First, see if the arg is optional
            m = optional_regex.match(line)
            if(m): optional = True;line=m.groups()[0]
            else: optional=False
            
            #Next, check to see if it is a standalone *arg* style argument
            m = arg_regex.match(line)
            if(m):
                regex = m.groups()[0]
                
                new_args = self.handle_arg_entry(regex=regex,
                                                 kwargs=kwargs,
                                                 optional=optional)
                
                args += new_args
                
                # Ok, done parsing arg entry... now on to the next one
                continue
                
            # Next, see if the line is a option arg spec
            m = opt_regex.match(line)
            if(m):
                
                # This is what we'll be appending to the retval (args) at the end
                new_args = []
                
                spec = line.split(":")
                
                # Option-regex match is required:
                regex = spec[0].strip()
                
                prefix = "--"
                try:
                    prefix = spec[1].strip()
                except:
                    pass
                
                # Type isn't required, and defaults to optarg
                type = "optarg"
                try:
                    type = spec[2].strip()
                    if type=="":
                        type="optarg"
                except:
                    pass
                
                # Count is also not required, and defaults to 1
                count = 1
                try:
                    count = int(spec[3].strip())
                except:
                    pass
                
                type = type.lower()
                
                new_args += self.handle_option_entry(regex=regex,
                                                     prefix=prefix,
                                                     type=type,
                                                     count=count,
                                                     kwargs=kwargs,
                                                     optional=optional)
                args += new_args
                
                # Ok, it was an option entry... keep going to the next entry
                continue
                
        return args
                
    
    def find_options(self,regex,kwargs):
        """
        Searches a dictionary (presumably from a **kwargs argument) and
        returns a list of all keys which match the regex argument.
        """
        ret = []
        
        r = re.compile(regex)
        for (k,v) in kwargs.items():
            if(r.match(k)):
                ret.append(k)
        
        return ret
    
    def handle_arg_entry(self,regex,kwargs,optional):
        ""
        # Use the regex to find the appropriate options
        args = []
        opts = self.find_options(regex,kwargs)
        
        if((len(opts) == 0) & (not optional) ):
            raise CommandError("Non-Optional *arg*-style argument %s was specified in the arg spec, but was not found in the keyword arguments." % regex)
        
        for opt in opts:
            
            value = kwargs[opt]
            if isinstance(value,list):
                for v in value:
                    args.append(v)
            else:
                args.append(value)
            
        return args
    def handle_option_entry(self,regex,prefix,type,count,kwargs,optional):
        """
        This function is called when an option arg spec line is encountered.
        
        For example, if the arg spec parser reads a line like
        
        ?my_opt:--:optarg:2
        
        The following is passed to this function:
        
        handle_option_entry(regex="my_opt",prefix="--",type="optarg",count=2,kwargs=**kwargs,optional=True
        
        This function proceeds to pass these arguments onto a function that has the following footprint:
        
        def handle_<type>_type(regex,prefix,count,kwargs,optional)
        
        , where <type> = type  (for example, optarg, compressed, meta, etc.)
        
        Thus, if one wants to, one can always add new types.
        
        """
        # Now to start parsing
        new_args = []
        
        #Calls a function with the name handle_<type>_type(regex,prefix,count,kwargs,optional)
        try:
            
            f = getattr(self,"handle_%s_type" % type.strip())
        except:
            logger.error("Type %s not recognized" % type)
            raise
        
        new_args += f(  regex=regex,
            prefix=prefix,
            count=count,
            kwargs=kwargs,
            optional=optional)
        
        return new_args
    
    def handle_optarg_type(self,regex,prefix,count,kwargs,optional):
        ""
        ret = []
        
        opts = self.find_options(regex,kwargs)
        
        if (len(opts) == 0) & (not optional):
            raise CommandError("Non-Optional option entry %s was specified in the arg spec, but was not found in the keyword arguments." % regex)
        
        for opt in opts:
            val = kwargs[opt] # Could be a list or a tuple
            
            #Force it to be a list to make supporting kw=[1,2,3] styple stuff
            if not isinstance(val,list):
                val = [val]
            
            for v in val:      
                values = []
                
                if count > 1:
                    # It's a tuple
                    for i in range(count):
                        values.append(str(v[i])) # also make sure it's a string
                else:
                    # It's just a string
                    values.append(str(v))
                
                # First append the properly formatted option
                option = "%s%s" % (prefix,opt)
                ret.append(option)
                
                # Then append each value
                for v in values:
                    ret.append(v)
                    
                #done
            
        return ret
    
    def handle_boolean_type(self,regex,prefix,count,kwargs,optional):
        """
        Handles an argspec entry of type "boolean"
        
        This example corresponds to an argspec entry of
        verbose:--:boolean
        
        >>> regex = "D"
        >>> prefix = "-"
        >>> count = 1 #ignored
        >>> kwargs = {"D" : "value"}
        >>> optional = False
        >>> c = CommandExecutor()
        >>> c.handle_compressed_type(regex,prefix,count,kwargs,optional)
        ['-Dvalue']
        
        """
        ret = []
        
        opts = self.find_options(regex,kwargs)
        
        if (len(opts) == 0) & (not optional):
            raise CommandError("Non-Optional option entry %s was specified in the arg spec, but was not found in the keyword arguments." % regex)
        
        for opt in opts:
            #val = kwargs[opt]
            # Value is irrelavent; just append the option
            option = "%s%s" % (prefix,opt)
            ret.append(option)
            
            #done
            
        return ret
    
    def handle_compressed_type(self,regex,prefix,count,kwargs,optional):
        """
        Handles an argspec entry of type "compressed".
        
        This example corresponds to an argspec entry of 
        D:-:compressed
        
        >>> regex = "D"
        >>> prefix = "-"
        >>> count = 1 #ignored
        >>> kwargs = {"D" : "value"}
        >>> optional = False
        >>> c = CommandExecutor()
        >>> c.handle_compressed_type(regex,prefix,count,kwargs,optional)
        ['-Dvalue']
        
        """
        ret = []
        
        opts = self.find_options(regex,kwargs)
        
        if (len(opts) == 0) & (not optional):
            raise CommandError("Non-Optional option entry %s was specified in the arg spec, but was not found in the keyword arguments." % regex)
        
        for opt in opts:
            val = kwargs[opt]
            val = str(val) # Convert to string
            
            # First append the properly formatted option
            option = "%s%s%s" % (prefix,opt,val)
            ret.append(option)
            
            #done
            
        return ret
    
    def handle_meta_type(self,regex,prefix,count,kwargs,optional):
        """
        Handles an argspec entry of type "meta" or type "property".
        
        This example corresponds to an example of arg spec 
        
        my_meta_arg:--:meta
        
        or
        
        my_meta_arg:--:property
        
        >>> regex = "my_meta_arg"
        >>> prefix = "--"
        >>> count = 1 #ignored
        >>> kwargs = {"my_meta_arg" : "value"}
        >>> optional = False
        >>> c = CommandExecutor()
        >>> c.handle_meta_type(regex,prefix,count,kwargs,optional)
        ['--my_meta_arg=value']
        """
        ret = []
        
        opts = self.find_options(regex,kwargs)
        
        if (len(opts) == 0) & (not optional):
            raise CommandError("Non-Optional option entry %s was specified in the arg spec, but was not found in the keyword arguments." % regex)
        
        for opt in opts:
            val = kwargs[opt]
            val = str(val) # Convert to string
            # We have everything we need
            option = "%s%s=%s" % (prefix,opt,val)
            ret.append(option)
            
            #done
            
        return ret
    
    def handle_property_type(self,regex,prefix,count,kwargs,optional):
        """
        
        Simply calls handle_meta_type
        
        """
        
        return self.handle_meta_type(regex=regex,prefix=prefix,count=count,kwargs=kwargs,optional=optional)
    
    def __call__(self,command_to_execute,arg_spec,stdout=sys.stdout,stderr=sys.stderr,stdin=sys.stdin,**kwargs):
        return self.execute(command_to_execute=command_to_execute,arg_spec=arg_spec,stdout=stdout,stderr=stderr,stdin=stdin,**kwargs)
    
    
def command_wrapper(command,arg_spec="*.**",stdout=sys.stdout,stderr=sys.stderr,stdin=sys.stdin):
    """
    Returns a function that wraps the specified command using the specified
    arg_spec
    
    >>> echo = command_wrapper("echo","*string*",stdout=PIPE)
    >>> ret = echo(string="Hello World")
    >>> val = ret.stdout.readline().strip()
    >>> val
    'Hello World'
    """
    def command_wrapper_function(**kwargs):
        c = CommandExecutor()
        return c.execute(command_to_execute=command,arg_spec=arg_spec, stdout=stdout,stderr=stderr,stdin=stdin, **kwargs)
        
    return command_wrapper_function

def cmdline2list(cmdline):
    """
    Unquotes a command line and then breaks it into an argument list.                                                                             )
    """
    
    ret = []
    
    quote_chars = ['"']
    
    for char in quote_chars:
    
        p = r'[^ \t\n\v\f"]+|"[^"]*"'
        #p = r'[^ \t\n\v\f"]+|' + char + r'[^"]*' + char
    
        results = re.findall(p,cmdline)
    
    # Remove the quotes
    for result in results:
        if (result[0] == '"') & (result[-1] == '"'):
            result = result[1:-1]
        ret.append(result)  
    return ret

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

                