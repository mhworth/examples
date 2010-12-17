#ifndef SHOWCUBE_H_
#define SHOWCUBE_H_

/* Core Includes */
#include <iostream>

/* External Includes */
#include <Ogre.h>

/* Local Package Includes*/
#include "examples/Application.h"

namespace examples {
class ShowCube : public examples::Application {
public:
	ShowCube();
	virtual ~ShowCube();
	
	void start();
	void stop();
};

}
#endif /*SHOWCUBE_H_*/
