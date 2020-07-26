

#include "meshes.h"
#include "messages.h"

EMCA_NAMESPACE_BEGIN

Meshes::Meshes() {

}

Meshes::~Meshes() {

}

void Meshes::serialize(Stream *stream) {
	stream->writeShort(Message::EMCA_HEADER_SCENE_DATA);
	unsigned int msgLen = m_meshes.size();
	stream->writeUInt(msgLen);
	for(unsigned int i = 0; i < msgLen; ++i)
		m_meshes[i].serialize(stream);
}

EMCA_NAMESPACE_END


