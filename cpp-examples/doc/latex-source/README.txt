


   README  File  for  mhworth.com  cpp-examples



                                     Matt Hollingsworth


                                       October 26, 2007

1       Introduction


This  README  file  attempts  to  introduce  the  user  to  the  usefulness  of  this
package  and  to  provide  instructions  that  are  necessary  for  building  and  run-
ning the different examples.  The different examples are divided into categories,
which  shall  be  enumerataed  in  the  next  section.   The  instructions  included
in this README apply to all categories;  however, each category of examples
has its own specific build requirements, which are explained externally to this
README.



2       Packages


cpp-examples is made up of multiple categories of examples-each category, in
general, corresponds to a specific library.  Here are the categories:


     o  ACE: The Adaptive Communications Framework
        URL: http://www.cs.wustl.edu/ schmidt/ACE.html

     o  boost:  The Boost C++ framework
        URL: http://www.boost.org

     o  corba:  CORBA examples based on ACE+TAO
        URL: http://www.cs.wustl.edu/ schmidt/ACE.html

     o  scons:  A build utility that is compatible with C++ and Java
        URL: http://www.scons.org

     o  xdaq:  A C++-based framework for distributed data acquisition
        URL: http://xdaqwiki.cern.ch



3       Preparing  to  build


To    build    the    targets,     you    must    download    and    install    scons
(http://www.scons.org).  scons  is  a  wonderful  python-based  build  utility  that
runs circles around make and friends, in my opinion.
     If you are using eclipse, you'll have to do a tiny bit of hacking to get it to work
right.  Most of the work is part of the project itself already; all you really have
to do is set the proper command to run scons by setting the eclipse workspace
variable "scons_cmd."  You may do this by going to project properties > C++



                                                   1
^L

build > and adding scons_cmd to the list.  On windows, you will need to look in
the bin directory for scons.cpp, which is a simple wrapper to execute scons.bat
from  eclipse.  This  is  necessary  because  eclipse  will  only  execute  executables.
scons.cpp is standalone, so all you should have to do is run


>  CL  scons.cpp
with  Visual  C++  or
>  g++  scons.cpp


for MinGW and friends to get the executable.  You then need to put scons.exe in
your PATH somewhere.  To do this, right click My Computer, go to properties
-> Advanced, and look for an Environment Variables button.  Here, you would
need  to  append  ";<your  scons  directory>"  to  the  existing  PATH  variable
under "User Environment Variables".
     After this is done, your scons_cmd eclipse variable will look something like


scons  C:\Python25\scons.bat  <arguments>


     The C:\Python25\scons.bat is the location of your scons.bat file so that
scons.exe  can  execute  it.   All  other  arguments  to  scons.exe  are  forwarded  to
scons.
     Afterward, you are ready to build whatever you wish.  Make sure you read
the  package-specific  build  instructions  for  dependency  information,  necessary
environment variables, etc.  If you are using eclipse, you can open up the Make
Targets window and simply right click each of the premade make targets for the
particular target that you wish to build.  Otherwise, you'll simply need to cd to
the appropriate directory and run


>  scons  <target  name>


to build the proper target.
     Any    questions    should    be    forwarded    to    Matt    Hollingsworth    at
hollings@cern.ch.


                                                   2
