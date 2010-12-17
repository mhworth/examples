/*Core Includes*/
#include <iostream>

/*Application Includes*/
#include "examples/Application.h"
#include "examples/ShowCube.h"

using namespace std;
using namespace examples;

int main(int argc,char** argv) {
	cout << "Hello World!" << endl;
	cout << argv[0] << endl;
	//Instantiate
	Application* app;
	if(argc > 0)
		app = new ShowCube();
	
	//Set resource path
	app->setResourcePath("");
	
	// Initialize everything
	app->initialize();
	
	// Start the app
	app->start();
}
