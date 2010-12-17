#include "examples/Application.h"
/*See include/examples/Application.h for all other include dependencies*/

using namespace Ogre;
using namespace std;

namespace examples {

Application::Application() {

	


}

Application::~Application() {
	cout << "Application Destroyed" << endl;
	if(mRoot)
		delete mRoot;
}

void Application::messageLogged ( const String& message,
			LogMessageLevel lml,
			bool maskDebug,
			const String & logName) {
	cout << message << endl;
}


void Application::initialize() {
	// First and most important, create the Root object
    String pluginsPath;
    // only use plugins.cfg if not static
	#ifndef OGRE_STATIC_LIB
    	pluginsPath = mResourcePath + "config/plugins.cfg";
	#endif
	
    mRoot = new Root(pluginsPath,
    	    mResourcePath + "config/ogre.cfg", mResourcePath + "Ogre.log");
    
    //Then, setup the logging
    setupLogging();
    
    // Now, setup the resources by putting everything in resources.cfg into the
    // resource manager
    
    try {
    	this->setupResources();
    } catch(Ogre::InternalErrorException& e) {
    	mLog->logMessage("Failed to load resources when using resource file " + mResourcePath + ".  Exiting");
    	exit(1);
    	
    }
    
    // If configure returns true, then the user clicked ok on the dialog.  Otherwise, he/she clicked cancel
	if(!this->configure()) {
		mLog->logMessage("Exiting");
		exit(0);
	}
	this->loadSceneManager();
	this->loadResources();
	this->createCameras();
	this->createViewports();
}

bool Application::configure() {
	// Show the configuration dialog and initialise the system
    // You can skip this and use root.restoreConfig() to load configuration
    // settings if you were sure there are valid ones saved in ogre.cfg
    if(mRoot->showConfigDialog())
    {   
        // If returned true, user clicked OK so initialise
        // Here we choose to let the system create a default rendering window by passing 'true'
        mWindow = mRoot->initialise(true);
        return true;
    }   
    else
    {   
        return false;
    }
}

void Application::setupLogging() {
	mLog = LogManager::getSingleton().createLog("main");
	//mLog->addListener(this);
	mLog->logMessage("Logging Initialized");
	//_log->setLogDetail(LoggingLevel.LL_BOREME);
}

bool Application::setupResources() throw (Ogre::InternalErrorException) {
	
	// Get the config from the config file
	ConfigFile cf;
    cf.load(mResourcePath + "config/resources.cfg");

    // Go through all sections & settings in the file
    ConfigFile::SectionIterator seci = cf.getSectionIterator();

    String secName, typeName, archName;
    while (seci.hasMoreElements())
    {   
        secName = seci.peekNextKey();
        ConfigFile::SettingsMultiMap *settings = seci.getNext();
        ConfigFile::SettingsMultiMap::iterator i;
        for (i = settings->begin(); i != settings->end(); ++i)
        {   
            typeName = i->first;
            archName = i->second;
            
            ResourceGroupManager::getSingleton().addResourceLocation(
                archName, typeName, secName);

        }
    }

	return true;
}

void Application::loadSceneManager() {
	// Create the SceneManager, in this case a generic one
	mSceneMgr = mRoot->createSceneManager(ST_GENERIC, "ApplicationSceneManager");
}

void Application::loadResources() {
	ResourceGroupManager::getSingleton().initialiseAllResourceGroups();
}

void Application::createCameras() {
		cout << "Creating Camera from Application" << endl;
	
        // Create the camera
        mCamera = mSceneMgr->createCamera("PlayerCam");
        // Position it at 500 in Z direction
        mCamera->setPosition(Vector3(0,0,500));
        // Look back along -Z
        mCamera->lookAt(Vector3(0,0,-300));
        mCamera->setNearClipDistance(5);
        
}

void Application::createViewports() {
        // Create one viewport, entire window
        Viewport* vp = mWindow->addViewport(mCamera);
        vp->setBackgroundColour(ColourValue(0,0,0));
 
        // Alter the camera aspect ratio to match the viewport
        mCamera->setAspectRatio(
        Real(vp->getActualWidth()) / Real(vp->getActualHeight()));
}

}
