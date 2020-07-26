#ifndef INCLUDE_EMCA_EMCASERVER_H_
#define INCLUDE_EMCA_EMCASERVER_H_

#include "platform.h"
#include "dataapi.h"
#include "renderinterface.h"
#include "server.h"

EMCA_NAMESPACE_BEGIN

class Server;
class EMCAServer {
public:

	EMCAServer();
	~EMCAServer();

	void setRenderer(RenderInterface *renderer);
	void setDataApi(DataApi *dataApi);
	void addPlugin(Plugin *plugin);

	void setPort(int port);
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
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_EMCASERVER_H_ */
