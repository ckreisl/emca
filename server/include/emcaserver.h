#ifndef INCLUDE_EMCA_EMCASERVER_H_
#define INCLUDE_EMCA_EMCASERVER_H_

#include "platform.h"
#include "stream.h"
#include "renderinterface.h"
#include "dataapi.h"
#include "server.h"
#include "plugin.h"

EMCA_NAMESPACE_BEGIN

enum RenderSystem { 
	mitsuba		= 0x01,
	smallpt 	= 0x02,
	other 		= 0xff
};

class Server;
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

	std::vector<short> getPluginIds();

	void start();
	void stop();

	bool readRenderInfo(Stream *stream);
	bool respondRenderInfo(Stream *stream);
	bool respondRenderImage(Stream *stream);
	bool respondSceneData(Stream *stream);
	bool respondRenderData(Stream *stream);
	bool respondPluginRequest(short id, Stream *stream);

private:
	Server *m_server;
	RenderInterface *m_renderer;
	DataApi *m_dataApi;
	RenderSystem m_renderSystem;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_EMCASERVER_H_ */
