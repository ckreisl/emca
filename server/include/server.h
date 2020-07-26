#ifndef INCLUDE_EMCA_SERVER_H_
#define INCLUDE_EMCA_SERVER_H_

#include "platform.h"
#include "stream.h"
#include "emcaserver.h"

EMCA_NAMESPACE_BEGIN

class EMCAServer;
class Server {
public:

	typedef int socket_t;

	Server(int port);
	~Server();

	void start();
	void stop();
	void disconnect();

	inline int getPort() { return m_port; }
	inline void setPort(int port) { m_port = port; }

	socket_t getClientSocket() { return m_clientSocket; }
	socket_t getServerSocket() { return m_serverSocket; }
	Stream* getStream() { return m_stream; }

	void setEMCAServer(EMCAServer *emcaServer) {m_emcaServer = emcaServer; }

private:
	int m_port;
	short m_lastSendMsg;
	short m_lastReceivedMsg;
	bool m_running;
	socket_t m_clientSocket;
	socket_t m_serverSocket;
	Stream *m_stream;
	EMCAServer *m_emcaServer;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_SERVER_H_ */
