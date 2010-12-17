README file for the cpp-examples package

* Introduction * 

* Preparing to build *
To build the targets, you must download and install scons (http://www.scons.org).
scons is a wonderful python-based build utility that runs circles around make and friends, in my opinion.

If you are using eclipse, you'll have to do a tiny bit of hacking to get it to work right.  Most of the work is part
of the project itself already; all you really have to do is set the proper command to run scons by setting the eclipse
workspace variable "scons_cmd."  You may do this by going to project properties -> C++ build -> Variables and adding scons_cmd
to the list.  On windows, you will need to look in the bin directory for scons.cpp, which is a simple
wrapper to execute scons.bat from eclipse.  This is necessary because eclipse will only execute executables.  scons.cpp is
standalone, so all you should have to do is run

> CL scons.cpp
with Visual C++ or
> g++ scons.cpp

for MinGW and friends to get the executable.  You then need to put scons.exe in your PATH somewhere.  To do this, 
right click My Computer, go to properties -> Advanced, and look for an Environment Variables button.
Here, you would need to append ";<your scons directory>" to the existing PATH variable under "User Environment Variables"

After this is done, your scons_cmd eclipse variable will look something like

scons C:\Python25\scons.bat <arguments>

The C:\Python25\scons.bat is the location of your scons.bat file so that scons.exe can execute it.  All other arguments
to scons.exe are forwarded to scons.

Afterward, you are ready to build whatever you wish.  Make sure you read the package-specific build instructions for dependency information, necessary environment variables, etc.
If you are using eclipse, you can open up the Make Targets window and simply right click each of the premade
make targets for the particular target that you wish to build.  Otherwise, you'll simply need to cd to the appropriate directory and run

scons <target name>

to build the proper target.

Any questions should be forwarded to Matt Hollingsworth at hollings@cern.ch.