
#include "sstream.h"
#include <cstddef>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>

#define INVALID_SOCKET -1
#define SOCKET_ERROR   -1

EMCA_NAMESPACE_BEGIN

SocketStream::SocketStream(socket_t socket) : m_clientSocket(socket) { }

SocketStream::~SocketStream() {
	if(close(m_clientSocket))
		std::cout << "Error by closing socket" << std::endl;
}

void SocketStream::read(void *ptr, size_t size) {
	char *data = (char *) ptr;
	while(size > 0) {
		ssize_t n = recv(m_clientSocket, data, size, 0);

		if(n == 0) {
			// TODO throw exception
		} else if(n == SOCKET_ERROR) {
			// TODO throw exception
		}

		size -= n;
		data += n;
	}
}

void SocketStream::write(const void *ptr, size_t size) {
	char *data = (char *) ptr;
	while(size > 0) {
		ssize_t n = send(m_clientSocket, data, size, MSG_NOSIGNAL);

		if (n == SOCKET_ERROR) {
			// TODO throw exception
		}

		size -= n;
		data += n;
	}
}

EMCA_NAMESPACE_END
