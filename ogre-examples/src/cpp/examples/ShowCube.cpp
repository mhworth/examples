#include "examples/Application.h"
#include "examples/ShowCube.h"

using namespace std;
using namespace Ogre;

namespace examples {


	ShowCube::ShowCube() {}
	ShowCube::~ShowCube() {}
	
	void ShowCube::start() {
		this->mLog->logMessage("Starting");
		
		// Set up the light
		mSceneMgr->setAmbientLight( ColourValue( 1, 1, 1 ) );
		
		// Get an entity
		Entity *ent1 = mSceneMgr->createEntity( "Robot", "robot.mesh" );

		// Creates a node in the render tree.  This is a child of the root node
		SceneNode *node1 = mSceneMgr->getRootSceneNode()->createChildSceneNode( "RobotNode" );

		// Attach the entity to the node
		node1->attachObject( ent1 );
		
		//Do it again
		Entity *ent2 = mSceneMgr->createEntity( "Cube", "Cube.mesh" );
		SceneNode *node2 = mSceneMgr->getRootSceneNode()->createChildSceneNode( "RobotNode2", Vector3( 50, 0, 0 ) );
		node2->attachObject( ent2 );
		node2->setScale(10,10,10);
		
		node1->setPosition(Vector3( 50, 50, 0 ));
		// Start rendering
		mRoot->startRendering();
	}
	
	void ShowCube::stop() {
		this->mLog->logMessage("Stopping");
	}

}
