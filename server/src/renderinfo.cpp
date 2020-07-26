
#include "renderinfo.h"
#include "messages.h"

EMCA_NAMESPACE_BEGIN

RenderInfo::RenderInfo() {
	// default values
	m_sceneName = "";
	m_outputFilepath = "";
	m_outputFileExtension = "";
	m_sampleCount = -1;
}

RenderInfo::RenderInfo(std::string sceneName, std::string pathToOutputFile,
		std::string extension, int sampleCount) {
	m_sceneName = sceneName;
	m_outputFilepath = pathToOutputFile;
	m_outputFileExtension = extension;
	m_sampleCount = sampleCount;
}

RenderInfo::~RenderInfo() {

}

void RenderInfo::serialize(Stream *stream) {
	stream->writeShort(Message::EMCA_HEADER_RENDER_INFO);
	stream->writeString(m_sceneName);
	stream->writeString(m_outputFilepath);
	stream->writeString(m_outputFileExtension);
	stream->writeInt(m_sampleCount);
}

void RenderInfo::deserialize(Stream *stream) {
	m_sampleCount = stream->readInt();
}

EMCA_NAMESPACE_END


