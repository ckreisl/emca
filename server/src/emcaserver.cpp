
#include "emcaserver.h"
#include "renderinfo.h"
#include "messages.h"
#include "dataapisingleton.h"

EMCA_NAMESPACE_BEGIN

EMCAServer::EMCAServer() {
	// init server and set msg callback
	m_server = new Server(50013);
	m_server->setEMCAServer(this);
	// default set DataApiSingleton
	m_dataApi = DataApiSingleton::getInstance();
	// default render system is mitsuba
	m_renderSystem = RenderSystem::mitsuba;
	m_renderer = nullptr;
}

EMCAServer::~EMCAServer() {
	delete m_server;
	delete m_dataApi;
	if(m_renderer)
		delete m_renderer;
}

void EMCAServer::setRenderSystem(RenderSystem renderSystem) {
	m_renderSystem = renderSystem;	
}

RenderSystem EMCAServer::getRenderSystem() {
	return m_renderSystem;
}

void EMCAServer::setRenderer(RenderInterface *renderer) {
	if(m_renderer) {
		delete m_renderer;
		m_renderer = nullptr;
	}
	m_renderer = renderer;
}

void EMCAServer::setDataApi(DataApi *dataApi) {
	if(m_dataApi) {
		delete m_dataApi;
		m_dataApi = nullptr;
	}
	m_dataApi = dataApi;
}

void EMCAServer::addPlugin(Plugin *plugin) {
	m_dataApi->addPlugin(plugin);
}

bool EMCAServer::readRenderInfo(Stream *stream) {
	try {
		RenderInfo renderInfo;
		renderInfo.deserialize(stream);
		m_renderer->updateSampleCount(renderInfo.getSampleCount());
	} catch(...) {
		return false;
	}
	return true;
}

bool EMCAServer::respondRenderInfo(Stream *stream) {
	try {
		m_renderer->sendRenderInformation(stream);
	} catch (...) {
		return false;
	}
	return true;
}

bool EMCAServer::respondRenderImage(Stream *stream) {
	try {
		m_renderer->renderImage();
		stream->writeShort(Message::EMCA_RENDER_IMAGE);
	} catch(...) {
		return false;
	}
	return true;
}

bool EMCAServer::respondSceneData(Stream *stream) {
	try {
		m_renderer->sendCameraData(stream);
		std::cout << "Send Camera Information DONE!" << std::endl;
		m_renderer->sendMeshData(stream);
		std::cout << "Send Mesh Information DONE!" << std::endl;
	} catch(...) {
		return false;
	}
	return true;
}

bool EMCAServer::respondRenderData(Stream *stream) {
	try {
		m_dataApi->enable();
		int x = stream->readInt();
		int y = stream->readInt();
		int sampleCount = stream->readInt();
		m_renderer->renderPixel(x, y, sampleCount);
		m_dataApi->serialize(stream);
		m_dataApi->disable();
		// no caching at the moment
		m_dataApi->clear();
	} catch(...) {
		return false;
	}
	return true;
}

bool EMCAServer::respondPluginRequest(short id, Stream *stream) {
	std::cout << "Plugin ID: " << id << std::endl;
	Plugin *plugin = m_dataApi->getPluginById(id);
	if(!plugin) return false;
	std::cout << "Running Plugin: " << plugin->getName() << std::endl;
	std::cout << "PluginRef: " << plugin << std::endl;
	plugin->deserialize(stream);
	bool finished = false;
	try {
		plugin->run();
		finished = true;
	} catch (std::exception &e) {
		std::cerr << e.what() << std::endl;
	}

	if (finished) {
		plugin->serialize(stream);
		return true;
	}

	return false;
}

std::vector<short> EMCAServer::getPluginIds() {
	return m_dataApi->getPluginHandler()->getPluginIds();
}

void EMCAServer::setPort(int port) {
	m_server->setPort(port);
}

void EMCAServer::start() {
	m_server->start();
}

void EMCAServer::stop() {
	m_server->stop();
}

EMCA_NAMESPACE_END

