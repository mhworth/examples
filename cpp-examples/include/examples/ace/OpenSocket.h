#ifndef OPENSOCKET_H_
#define OPENSOCKET_H_

#import <string>
#import <set>

namespace examples
{

namespace ace {

/** \brief Open a socket
 * 
 * This class simply opens and closes sockets using the ACE framework.
 * 
 * You may check to make sure that it worked by telnetting to the port you
 * opened; for example,
 * 
 * <pre>
 * telnet localhost 5000
 * </pre>
 * 
 * would connect you locally to port 5000.  If it connects, the socket has been
 * opened successfully.
 * 
 */
class OpenSocket
{
public:
	OpenSocket();
	virtual ~OpenSocket();
	
	/**Open a socket that is listening to all interfaces on the port specified.
	 * This function simply returns if a socket is already open.  
	 */
	void openSocket(int port);
	
	/**
	 * Open a socket that is listening on the interfaces specified by
	 * a set of ip addresses.  The set should contain string representations
	 * of the ip addresses that you wish to listen with; i.e., "127.0.0.1"
	 */
	void openSocket(std::set<std::string>& ipAddressList, int port);
	
	/**Closes the socket that was opened previously by openSocket.  If there is
	 * no socket open, this function simply returns.
	 */
	void closeSocket();
	
private:
	bool isOpen_;
};

}

}

#endif /*OPENSOCKET_H_*/
