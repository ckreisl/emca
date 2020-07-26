
#include "server.h"
#include "sstream.h"
#include "messages.h"

#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define INVALID_SOCKET -1

EMCA_NAMESPACE_BEGIN

Server::Server(int port) {

	m_port = port;
	m_serverSocket = socket(AF_INET, SOCK_STREAM, 0);
	// default values
	m_lastSendMsg = -1;
	m_lastReceivedMsg = -1;
	m_clientSocket = -1;
	m_running = false;
	m_stream = nullptr;
	m_emcaServer = nullptr;

	if(m_serverSocket == INVALID_SOCKET) {
		// TODO throw exception invalid socket!
		std::cout << "Invalid Socket" << std::endl;
		exit(-1);
	}
}

Server::~Server() {
	delete m_stream;
}

void Server::start() {

	struct sockaddr_in server_addr, client_addr;
	bzero((char *) &server_addr, sizeof(server_addr));

	int option = 1;
	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.s_addr = INADDR_ANY;
	server_addr.sin_port = htons(m_port);

	if(setsockopt(m_serverSocket, SOL_SOCKET, (SO_REUSEPORT | SO_REUSEADDR), (char*)&option, sizeof(option)) < 0) {
		std::cout << "Server setsockopt failed" << std::endl;
		close(m_serverSocket);
		exit(2);
	}

	int isBind = bind(m_serverSocket, (struct sockaddr*)&server_addr, sizeof(server_addr));

	if(isBind < 0) {
		std::cout << "Server bind failed" << std::endl;
		close(m_serverSocket);
		exit(1);
	}

	LISTEN:int isListen = listen(m_serverSocket, 5);

	if(isListen < 0)
		exit(-1);

	std::cout << "Server is listening for connections ..." << std::endl;

	socklen_t len = sizeof(client_addr);
	m_running = true;

	while (m_running) {
		m_clientSocket = accept(m_serverSocket,
				(struct sockaddr*) (&client_addr), &len);
		if (m_clientSocket < 0)
			std::cout << "Client Socket Error" << std::endl;

		m_stream = new SocketStream(m_clientSocket);
		m_stream->writeShort(Message::EMCA_HELLO);
		m_lastSendMsg = Message::EMCA_HELLO;
		m_lastReceivedMsg = m_stream->readShort();

		if (m_lastReceivedMsg != Message::EMCA_HELLO) {
			m_running = false;
			break;
		}

		std::cout << "Handshake complete! Starting data transfer ..." << std::endl;

		try {
			while(m_running) {
				// read header of message
				m_lastReceivedMsg = m_stream->readShort();
				std::cout << "Received header msg = " << m_lastReceivedMsg << std::endl;

				if(m_emcaServer->respondPluginRequest(m_lastReceivedMsg, m_stream)) {
					continue;
				}

				switch(m_lastReceivedMsg) {
				case Message::EMCA_HEADER_RENDER_INFO:
					std::cout << "Respond render info msg" << std::endl;
					m_emcaServer->respondRenderInfo(m_stream);
					break;
				case Message::EMCA_SET_RENDER_INFO:
					std::cout << "Set render info msg" << std::endl;
					m_emcaServer->readRenderInfo(m_stream);
					break;
				case Message::EMCA_HEADER_SCENE_DATA:
					std::cout << "Respond scene data msg" << std::endl;
					m_emcaServer->respondSceneData(m_stream);
					break;
				case Message::EMCA_RENDER_IMAGE:
					std::cout << "Render image msg" << std::endl;
					m_emcaServer->respondRenderImage(m_stream);
					break;
				case Message::EMCA_RENDER_PIXEL:
					std::cout << "Render pixel msg" << std::endl;
					m_emcaServer->respondRenderData(m_stream);
					break;
				case Message::EMCA_DISCONNECT:
					std::cout << "Disconnect msg" << std::endl;
					m_stream->writeShort(Message::EMCA_DISCONNECT);
					m_lastSendMsg = Message::EMCA_DISCONNECT;
					close(m_clientSocket);
					m_running = false;
					break;
				case Message::EMCA_QUIT:
					std::cout << "Quit message!" << std::endl;
					m_stream->writeShort(Message::EMCA_QUIT);
					m_lastSendMsg = Message::EMCA_QUIT;
					close(m_clientSocket);
					close(m_serverSocket);
					m_running = false;
					break;
				default:
					std::cout << "Unknown message received!" << std::endl;
					break;
				}
			}
		} catch (std::exception &e) {
			// TODO handle exception
            std::cerr << "caught exception: " << e.what() << std::endl;
            m_stream->writeShort(Message::EMCA_DISCONNECT);
            close(m_clientSocket);
            m_running = false;
		} catch (...) {
			// TODO handle exception
            std::cerr << "caught exception." << std::endl;
            m_stream->writeShort(Message::EMCA_DISCONNECT);
            close(m_clientSocket);
            m_running = false;
		}

		// TODO remove goto command and go for a clean implementation if client disconnects.
		if(m_lastReceivedMsg == Message::EMCA_DISCONNECT)
			goto LISTEN;
	}
}

void Server::disconnect() {
	try {
		m_lastSendMsg = Message::EMCA_DISCONNECT;
		m_stream->writeShort(Message::EMCA_DISCONNECT);
		close(m_clientSocket);
		m_running = false;
	} catch(std::exception &e) {
		std::cout << "Exception: " << e.what() << std::endl;
	}
}

void Server::stop() {
	try {
		m_lastSendMsg = Message::EMCA_QUIT;
		m_stream->writeShort(Message::EMCA_QUIT);
		close(m_clientSocket);
		close(m_serverSocket);
	} catch(std::exception &e) {
		std::cout << "Exception: " << e.what() << std::endl;
	}

}

EMCA_NAMESPACE_END



