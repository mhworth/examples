#ifndef SPINCAMERA_H_
#define SPINCAMERA_H_

/* Core Includes */
#include <iostream>

/* External Includes */
#include <Ogre.h>

/* Local Package Includes*/
#include "examples/Application.h"

namespace examples {
class SpinCamera : public examples::Application {
public:
	SpinCamera();
	virtual ~SpinCamera();
	
	void start();
	void stop();
	void createCameras();
};

}
#endif /*SPINCAMERA_H_*/
