#pragma once
#ifndef INCLUDE_EMCA_SSTREAM_H_
#define INCLUDE_EMCA_SSTREAM_H_

#include "platform.h"
#include "stream.h"

EMCA_NAMESPACE_BEGIN

class SocketStream : public Stream {
public:
	typedef int socket_t;

	SocketStream(socket_t socket);
	void write(const void *ptr, size_t size);
	void read(void *ptr, size_t size);

protected:
	virtual ~SocketStream();

private:
	socket_t m_clientSocket;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_SSTREAM_H_ */
