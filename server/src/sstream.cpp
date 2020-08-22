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
