/*
	EMCA - Explorer Monte-Carlo based Alorithm (Shared Server Library)
	comes with an Apache License 2.0
	(c) Christoph Kreisl 2020

	Licensed to the Apache Software Foundation (ASF) under one
	or more contributor license agreements.  See the NOTICE file
	distributed with this work for additional information
	regarding copyright ownership.  The ASF licenses this file
	to you under the Apache License, Version 2.0 (the
	"License"); you may not use this file except in compliance
	with the License.  You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing,
	software distributed under the License is distributed on an
	"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
	KIND, either express or implied.  See the License for the
	specific language governing permissions and limitations
	under the License.
*/

#ifndef INCLUDE_EMCA_SERVER_H_
#define INCLUDE_EMCA_SERVER_H_

#include <mutex>
#include <functional>
#include "platform.h"
#include "stream.h"

EMCA_NAMESPACE_BEGIN

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

	void setRespondPluginRequest(const std::function<bool(short, Stream *)> &callback);
	void setRespondRenderInfoCallback(const std::function<bool(Stream *)> &callback);
	void setReadInfoCallback(const std::function<bool(Stream *)> &callback);
	void setRespondRenderImageCallback(const std::function<bool(Stream *)> &callback);
	void setRespondSceneDataCallback(const std::function<bool(Stream *)> &callback);
	void setRespondRenderDataCallback(const std::function<bool(Stream *)> &callback);
	void setRespondRenderSystemCallback(const std::function<bool(Stream *)> &callback);
	void setRespondSupportedPluginsCallback(const std::function<bool(Stream *)> &callback);

private:
	int m_port;
	short m_lastSendMsg;
	short m_lastReceivedMsg;
	bool m_running;
	socket_t m_clientSocket;
	socket_t m_serverSocket;
	Stream *m_stream;
	std::mutex m_mutex;

	std::function<bool(short, Stream*)> m_callbackRespondPluginRequest;
	std::function<bool(Stream *)> m_callbackRespondRenderInfo;
	std::function<bool(Stream *)> m_callbackReadRenderInfo;
	std::function<bool(Stream *)> m_callbackRespondRenderImage;
	std::function<bool(Stream *)> m_callbackRespondSceneData;
	std::function<bool(Stream *)> m_callbackRespondRenderData;
	std::function<bool(Stream *)> m_callbackRespondRenderSystem;
	std::function<bool(Stream *)> m_callbackRespondSupportedPlugins;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_SERVER_H_ */
