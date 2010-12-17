#include "examples/ace/OpenSocket.h"

#include <string>
#include <set>

namespace examples
{

namespace ace
{

OpenSocket::OpenSocket()
{
}

OpenSocket::~OpenSocket()
{
}

void OpenSocket::openSocket(int port) {
	//Just call openSocket(std::set<std::string>&, int) with an empty set
	std::set<std::string> stringSet;
	openSocket(stringSet, port);
}

void OpenSocket::openSocket(std::set<std::string>& ipAddressList, int port) {
	//Check to see if the socket is already open
	//If it isn't, open it, if it is, just return
	if(!isOpen_) {
		if(ipAddressList.size()==0) {
			//bind all addresses
		} else {
			//bind specific addresses
		}
		isOpen_ = true;
	} else {
		return;
	}
}

void OpenSocket::closeSocket() {
	
}

}

}
