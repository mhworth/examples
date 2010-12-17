#include <cstdlib>
#include <iostream>
#include <string>

using namespace std;

int main(int argc, char* argv[]) {
	string args;
	
	if(argc<2) {
		cerr << "You must specify the location of scons.bat" << endl;
		exit(1);
	}
	string location(argv[1]);
	
	for(int i = 2;i<argc;i++) {
		string str(argv[i]);
		args += str + " ";
	}
	string cmd;
	
	cmd += location + " " + args;
	system(cmd.c_str());
}



