#ifndef INCLUDE_EMCA_EMCASERVER_H_
#define INCLUDE_EMCA_EMCASERVER_H_

#include "platform.h"
#include "stream.h"
#include "renderinterface.h"
#include "dataapi.h"
#include "plugin.h"
#include "server.h"

EMCA_NAMESPACE_BEGIN

enum RenderSystem { 
	mitsuba		= 0x01,
	smallpt 	= 0x02,
	other 		= 0xff
};

class EMCAServer {
public:

	EMCAServer();
	~EMCAServer();

	void setRenderer(RenderInterface *renderer);
	void setDataApi(DataApi *dataApi);
	void addPlugin(Plugin *plugin);

	void setRenderSystem(RenderSystem renderSystem);
	RenderSystem getRenderSystem();
	void setPort(int port);

	void start();
	void stop();

private:
	bool respondRenderSystem(Stream *stream);
	bool respondSupportedPlugins(Stream *stream);
	bool readRenderInfo(Stream *stream);
	bool respondRenderInfo(Stream *stream);
	bool respondRenderImage(Stream *stream);
	bool respondSceneData(Stream *stream);
	bool respondRenderData(Stream *stream);
	bool respondPluginRequest(short id, Stream *stream);

	Server *m_server;
	RenderInterface *m_renderer;
	DataApi *m_dataApi;
	RenderSystem m_renderSystem;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_EMCASERVER_H_ */
