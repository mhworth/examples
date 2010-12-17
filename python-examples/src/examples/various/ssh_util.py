"""
ssh_util.py: A few utility classes for dealing with ssh connections.

Requirements: paramiko

* Installing paramiko
Ubuntu: sudo apt-get install python-paramiko

SL4: Available through the "dag" repository, which is available at http://dag.wieers.com.  See http://dag.wieers.com/rpm/FAQ.php#B for installation instructions for the repository.
  $ yum install python-paramiko.noarch

Other:  Paramiko is available through the python package repository, so it may be installed using easy_install.  See http://peak.telecommunity.com/DevCenter/setuptools for usage and installation instructions.
  $ sudo easy_install -n  paramiko

Author: Matt Hollingsworth (hollings@cern.ch)
Date: 5-30-08

"""

import os,sys,re
from optparse import OptionParser
from urlparse import urlparse
from getpass import getuser, getpass
import paramiko
from tempfile import TemporaryFile
import cStringIO as sio
import select
import traceback

BLOCKSIZE = 256 #used for ssh io
USAGE = \
"""
scpget.py --ssh-host [username@]ssh.host.com [--username username] [--output filename|-] http://host.domain.tld/filename.file



"""

class SSHError(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class SSHBase:
    def __init__(self,ssh_host=None,port=22,username=None,password=None,paramiko_log=os.devnull):
        self._ssh_host = ssh_host
        self._username = username
        self._password = password
        self._port = port
        paramiko.util.log_to_file(paramiko_log)
    
    def port(self,port=None):
        if(port != None):
            self._port = port
        return self._port
    
    def hostname(self,hostname=None):
        """
        An alias for ssh_host()
        """
        return self.ssh_host(hostname)

    def ssh_host(self,ssh_host=None):
        if(ssh_host != None):
            self._ssh_host = ssh_host
        return self._ssh_host
    
    def username(self,username=None):
        if(username != None):
            self._username = username
        return self._username

    def password(self,password=None):
        if(password != None):
            self._password = password
        return self._password

    def get_hostkeys(self,hostname):
        # get host key, if we know one
        hostkeytype = None
        hostkey = None
        try:
                host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
                try:
                    # try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
                    host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
                except IOError:
                    print >> sys.stderr, '*** Unable to open host keys file'
                    host_keys = {}

        if host_keys.has_key(hostname):
                hostkeytype = host_keys[hostname].keys()[0]
                hostkey = host_keys[hostname][hostkeytype]
                #print >> sys.stderr, 'Using host key of type %s' % hostkeytype

        return (hostkeytype,hostkey)
    
    def setup_transport(self):
        
        """
        Returns a connected transport and an open session in a tuple:
        
        return (transport,channel)
        
        You must make sure that you've set the parameters properly before
        calling this function, or you'll get an exception.
        """
        #Setup the connection
        (hostkeytype,hostkey) = self.get_hostkeys(self.ssh_host())
        t = paramiko.Transport((self._ssh_host, self._port))
        
        try:
            t.connect(username=self._username,password=self._password,hostkey=hostkey)
        except Exception, e:
            t.close()
            raise
        
        self._transport = t
        return t
    def setup_session(self,transport = None):
        """
        Gets a Channel instance, using the transport that is
        returned via the setup_transport() function.  
        
        This should be called after setup_transport(), in which case
        you do not need to provide a transport arg to this function.
        
        However, if it makes you more comfortable, you can do
        
        t = ssh_instance.setup_transport()
        session = ssh_instance.setup_session(t)
        
        also.
        
        """
        if transport is None:
            transport = self._transport
        try:
            chan = transport.open_session()
        except Exception, e:
            transport.close()
            raise
        
        self._chan = chan
        return chan
    
    def setup_sftp_client(self,transport = None):
        ""
        if transport is None:
            transport = self._transport
        
        try:
            sftp = paramiko.SFTPClient.from_transport(transport)
        except Exception, e:
            transport.close()
            raise
        
        return sftp
    
    def prompt_for_missing(self,force=False,timeout=3,ignore_password=False,
                           host_prompt="SSH Host: ",host_msg="Hostname not specified.  Please enter hostname",
                           username_prompt="Username: ", username_msg="User name not specified.  Please enter a user name.",
                           password_prompt="Password: ", password_msg="Password not specified.  Please enter a password."):
        """
        For each required argument (ssh_host,username,password) that
        is currently = None, prompt the user for the proper values
        (from the console).
        
        If force=True, all parameters will be prompted for.
        
        timeout specifies the number of times to take blank input
        before throwing an SSHError.  I.e., if the user is
        prompted for ssh_host 3 times, and keeps only hitting
        enter instead of entering a host, and timeout=3,
        after 3 times of blank input, the function will throw 
        an SSHError.
        
        ignore_password=True is useful if you are using PKI for authentication.
        
        The different *_msg and *_prompt args specify the message that
        is printed before prompting the user and prompt itself for each
        parameter.
        """
        if force or (self.ssh_host() is None):
            self.ssh_host(None)
            counter = 0
            while(not bool(self.ssh_host())):
                if bool(host_msg):
                    print host_msg
                counter += 1
                if counter > timeout:
                    raise SSHException("ERROR: Hostname must not be blank!")
                
                self.ssh_host(raw_input(host_prompt))
                
        if force or (self.username() is None):
            self.username(None)
            counter = 0
            while(not bool(self.username())):
                if bool(host_msg):
                    print username_msg
                counter += 1
                if counter > timeout:
                    raise SSHException("ERROR: Hostname must not be blank!")
                
                self.username(raw_input(username_prompt))
        if (force or (self.password() is None)) & (not ignore_password):
            
            self.password(None)
            counter = 0
            while(not bool(self.password())):
                if bool(host_msg):
                    print password_msg
                counter += 1
                if counter > timeout:
                    raise SSHException("ERROR: Hostname must not be blank!")
                
                self.password(getpass(password_prompt))
                
class SSHCommandExecutor(SSHBase):
    def __init__(self,ssh_host=None,port=22,username=None,password=None):
        SSHBase.__init__(self,ssh_host=ssh_host,port=port,username=username,password=password)
    
    def quick_execute(self,command,interactive=False,stdin=None,stdout=sys.stdout,stderr=sys.stderr):
        """
        Another alias for execute_command(), except this one
        defaults to stdin=None, stdout=sys.stdout, stderr=sys.stderr.
        
        This is useful for piping things around, etc
        
        """
        self.execute_command(command=command,interactive=interactive,stdin=stdin,stdout=stdout,stderr=stderr)
        
    def execute(self,command,interactive=False,stdin=None,stdout=None,stderr=None):
        """
        A simple alias for execute_command()
        
        """
        self.execute_command(command=command,interactive=interactive,stdin=stdin,stdout=stdout,stderr=stderr)
        
    def execute_command(self,command,interactive=False,stdin=None,stdout=None,stderr=None):
        """Returns a tuple of the output of file objects representing
        the output of the command: (stdin,stdout,stderr) if the command is
        non-interactive, and if the command is interactive, it is connected
        to stdin, stdout, and stderr.  Make sure that
        the command is not going to wait for input, since that would cause
        the function to block.
        
        There is really no mechanism to figure out the order which things
        were written to the outputs... if you really need to know, you'll want
        to do redirection in the actual command:
        
        echo hi 2>&1
        
        for example, would write everything in "order" to stdout.
        """
        if(interactive):
            if stdin is None:
                stdin = sys.stdin
            if stdout is None:
                stdout = sys.stdout
            if stderr is None:
                stderr = sys.stderr
            return self._execute_interactive_command(command,stdin,stdout,stderr)
        else:
            if stdout is None:
                stdout = TemporaryFile()
            if stderr is None:
                stderr = TemporaryFile()
            return self._execute_noninteractive_command(command,stdin,stdout,stderr)
            
    def _execute_interactive_command(self,command,stdin,stdout,stderr):
        ""

        
        return (stdin,stdout,stderr)
    def _execute_noninteractive_command(self,command,stdin,stdout,stderr):
        ""
        t = self.setup_transport()
        chan = self.setup_session() 
        #(t,chan) = self.setup_connection()
        
        try:
            chan.exec_command(command)
            io = chan.makefile()
            err = chan.makefile_stderr()
            
            # Forward stdin
            if not (stdin is None):
                dat = stdin.read(BLOCKSIZE)
                while(dat):
                    io.write(dat)
                    dat = stdin.read(BLOCKSIZE)
                
            # Forward stdout
            dat = io.read(BLOCKSIZE)
            while(dat):
                stdout.write(dat)
                dat = io.read(BLOCKSIZE)
                
            # Forward stderr
            dat = err.read(BLOCKSIZE)
            while(dat):
                stderr.write(dat)
                dat = err.read(BLOCKSIZE)
                
        except Exception, e:
            t.close()
            raise
        
        t.close()
        
        try:
            stdout.seek(0)
        except:
            pass
        
        try:
            stderr.seek(0)
        except:
            pass
        
        return (stdin,stdout,stderr)
        
    
class UrlFileGetter(SSHCommandExecutor):
    """
    Uses an ssh wget call to get urls from a ssh server.
    
    :Author: Matt Hollingsworth
    :Date: 5-31-2008
    """
    def __init__(self,ssh_host=None,port=22,username=None,password=None):
        SSHCommandExecutor.__init__(self,ssh_host=ssh_host,port=port,username=username,password=password)

    def get_url(self,url,output=None):
        """Gets the url using the configured ssh server, username, and password to connect to the URL"""
        parsed_url = urlparse(url)
        hostname = parsed_url[1]
    
        #Make the command
        cmd = "wget %s -O -" % url
        (ssh_input,ssh_output,ssh_err) = self.execute_command(cmd)
        
        if(output==None):
            p = urlparse(url)[2]
            filename = os.path.split(p)[1] 
            output = filename
        # See if it's ok.
        err = sio.StringIO()
        dat = ssh_err.read(BLOCKSIZE)
        while(dat):
            err.write(dat)
            dat = ssh_err.read(BLOCKSIZE)
        
        err_out = err.getvalue()
        print >> sys.stderr, err_out
        err1 = re.compile(r"failed") # Failed to resolve hostname
        err2 = re.compile(r"404 Not Found") # File not found
        
        if(err1.search(err_out)):
            raise SSHError("ERROR: Failed to retrieve file!  Hostname unknown")
        elif(err2.search(err_out)):
            raise SSHError("ERROR: Failed to retrieve file.  File not found")
        # If it didn't fail, read the file.
        
        if(output=="-"):
            f = sys.stdout
        else:
            f = open(output,"w+b")
        dat = ssh_output.read(BLOCKSIZE)
        while(dat):
            f.write(dat)
            dat = ssh_output.read(BLOCKSIZE)
            
class SSHFileOps(SSHBase):
    """
    A class for SCP'ing files around.
    
    :Author: Matt Hollingsworth
    :Date: 5-31-08
    """
    def __init__(self,ssh_host=None,port=22,username=None,password=None):
        SSHBase.__init__(self,ssh_host=ssh_host,port=port,username=username,password=password)
        self._transport = None
        self._sftp = None
    
    def connect(self):
        ""
        t = self.setup_transport()
        sftp = self.setup_sftp_client()
        self._transport = t
        self._sftp = sftp
        
    def disconnect(self):
        """
        Disconnects
        
        """
        
        self.get_transport().close()
        self._transport = None
        self._sftp = None
    def get_transport(self):
        return self._transport
    def get_sftp(self):
        return self._sftp
    def scp(self,source,dest,recurse=True,follow_links=True):
        """
        Send a file or files from a source to a destination on the ssh server.
        
        The destination server is given in the constructor for the SCP class,
        or through subsequent calls to ssh_host(), port()
        """
        if isinstance(source,list):
            for s in source:
                self._copy(source=s,dest=dest,recurse=True,follow_links=True)
        
        #print dir(self.get_sftp())
    
    def _copy(self,source,dest):
        ""
        
    
    def ls(self,dir=".",recursive=False,maxlevel=1000):
        ""
        
        results = []
        #for r in root_contents:
        #    results.append(r)
        #results += root_contents
        if recursive:
            results = self._recurse_dir_tree(dir,results,0,maxlevel)
        else:
            results = self.get_sftp().listdir(dir)
            
        return results
    def _recurse_dir_tree(self,root,list,level=0,maxlevel=1000):
        ""
        print "maxlevel=%s, level=%s" % (maxlevel,level)
        
        if (level > maxlevel) & (maxlevel >= 0):
            return
        
        root_list = self.get_sftp().listdir(root)
        full_name_list = []
        for r in root_list:
            n = root + os.path.sep + r
            list.append(n)
            full_name_list.append(n)
                
        level+=1
        print "level=%s" % level
        for dir in full_name_list:
            
            try:
                results = self.get_sftp().listdir(dir)
                for result in results:
                    full_result = dir + os.path.sep + result
                    #if not full_result in list: list.append(full_result)
                    
                    self._recurse_dir_tree(full_result,list,level,maxlevel=maxlevel)
            except Exception, e:
                pass
        
        return list

# Some useful functions
def quick_execute(command,ssh_host=None,username=None,password=None,interactive=False,stdin=None,stdout=sys.stdout,stderr=sys.stderr,ignore_password=False):
        """
        Prompts the user for all necessary input (hostname,username,password)
        and returns a SSHCommandExecutor instance initialized with these
        parameters, first calling quick_execute on the instance before returning.
        
        """
        sce = SSHCommandExecutor()
        sce.ssh_host(ssh_host)
        sce.username(username)
        sce.password(password)
        sce.prompt_for_missing(ignore_password=ignore_password)
        sce.quick_execute(command,interactive=interactive,stdin=stdin,stdout=stdout,stderr=stderr)
        return sce