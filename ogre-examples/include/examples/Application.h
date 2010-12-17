#ifndef APPLICATION_H_
#define APPLICATION_H_

/* Core Includes */
#include <iostream>

/*External Dependencies*/
#include <Ogre.h>
#include <OgreConfigFile.h>
#include <OgreLogManager.h>
#include <OgreLog.h>
#include <OIS/OIS.h>

/*Platform Specific Code*/

#if OGRE_PLATFORM == OGRE_PLATFORM_APPLE
#include <CoreFoundation/CoreFoundation.h>

// This function will locate the path to our application on OS X,
// unlike windows you can not rely on the curent working directory
// for locating your configuration files and resources.
std::string macBundlePath()
{
    char path[1024];
    CFBundleRef mainBundle = CFBundleGetMainBundle();
    assert(mainBundle);

    CFURLRef mainBundleURL = CFBundleCopyBundleURL(mainBundle);
    assert(mainBundleURL);

    CFStringRef cfStringRef = CFURLCopyFileSystemPath( mainBundleURL, kCFURLPOSIXPathStyle);
    assert(cfStringRef);

    CFStringGetCString(cfStringRef, path, 1024, kCFStringEncodingASCII);

    CFRelease(mainBundleURL);
    CFRelease(cfStringRef);

    return std::string(path);
}
#endif

/*End Platform Specific Code*/

/*Class Declaration*/

namespace examples {

/**
 * The base class for all the applications.  It provides a logging
 * mechanism, etc.
 * 
 * Here is how you use the class:
 * 
 * 1) Instantiate a subclass of it (the subclass must override start() and stop())
 * 2) Call setResourcePath with the base path which contains your resources (probably the cwd)
 * 3) Call #initialize()
 * 4) Call #start()
 */
class Application : public Ogre::LogListener  {
public:
	Application();
	virtual ~Application();
	
	/*Core functions*/
	void initialize();
	
	/*Start/stop the application*/
	virtual void start() = 0;
	virtual void stop() = 0;
	/**
	 * Configures the graphics system.  This will show
	 * the config dialog box for the user to choose resolution etc.
	 */
	bool configure();
	
	/**
	 *	This function uses the resources.cfg to add all
	 * the resources to the resource manager.
	 */
	bool setupResources() throw (Ogre::InternalErrorException);
	virtual void setupLogging();
	virtual void loadSceneManager();
	virtual void loadResources();
	virtual void createCameras();
	virtual void createViewports();
	
	/*Getters/Setters*/
	inline void setResourcePath(Ogre::String path) {mResourcePath = path;}
	inline Ogre::String& getResourcePath(Ogre::String path) {return mResourcePath;}
	
	/*Implements LogListener*/
	virtual void messageLogged ( const Ogre::String& message,
			Ogre::LogMessageLevel lml,
			bool maskDebug,
			const Ogre::String & logName);
protected:
	Ogre::Log* mLog;
	Ogre::Root *mRoot;
	Ogre::Camera* mCamera;
	Ogre::SceneManager* mSceneMgr;
	Ogre::RenderWindow* mWindow;
	Ogre::String mResourcePath;
};

}
/*End Class Declaration*/
#endif /*APPLICATION_H_*/
