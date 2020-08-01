#ifndef EMCA_INCLUDE_RENDERINTERFACE_H_
#define EMCA_INCLUDE_RENDERINTERFACE_H_

#include "platform.h"
#include "stream.h"

EMCA_NAMESPACE_BEGIN

class RenderInterface {
public:
	virtual ~RenderInterface() { }
	virtual void renderImage() = 0;
	virtual void renderPixel(unsigned int x, unsigned int y, int sampleCount) = 0;
	virtual void sendRenderInformation(Stream *stream) = 0;
	virtual void sendCameraData(Stream *stream) = 0;
	virtual void sendMeshData(Stream *stream) = 0;
	virtual void updateSampleCount(int sampleCount) = 0;
};

EMCA_NAMESPACE_END

#endif /* EMCA_INCLUDE_EMCARENDERINTERFACE_H_ */
