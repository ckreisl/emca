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

#include "emcaserver.h"
#include "scenedata.h"
#include "messages.h"
#include "dataapisingleton.h"

EMCA_NAMESPACE_BEGIN

EMCAServer::EMCAServer() {
	// default set DataApiSingleton
	m_dataApi = DataApiSingleton::getInstance();
	// default render system is mitsuba
	m_renderSystem = RenderSystem::mitsuba;
	m_renderer = nullptr;
	// init server and set callback functions
	m_server = new Server(50013);
	m_server->setRespondRenderSystemCallback([this](Stream *stream) { return respondRenderSystem(stream); });
	m_server->setRespondPluginRequest([this](short id, Stream *stream) { return respondPluginRequest(id, stream); });
	m_server->setRespondRenderInfoCallback([this](Stream *stream) { return respondRenderInfo(stream);} );
	m_server->setReadInfoCallback([this](Stream *stream) { return readRenderInfo(stream); });
	m_server->setRespondRenderImageCallback([this](Stream *stream) { return respondRenderImage(stream); });
	m_server->setRespondSceneDataCallback([this](Stream *stream) { return respondSceneData(stream); });
	m_server->setRespondRenderDataCallback([this](Stream *stream) { return respondRenderData(stream); });
	m_server->setRespondSupportedPluginsCallback([this](Stream *stream) { return respondSupportedPlugins(stream); });
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

bool EMCAServer::respondRenderSystem(Stream *stream) {
	try
	{
		std::cout << "Inform Client about Render System" << std::endl;
		stream->writeShort(getRenderSystem());
	}
	catch (...)
	{
		return false;
	}
	return true;
}

bool EMCAServer::respondSupportedPlugins(Stream *stream) {
	try
	{
		std::cout << "Inform Client about supported Plugins" << std::endl;
		m_dataApi->getPluginHandler()->printPlugins();
		std::vector<short> supportedPlugins = m_dataApi->getPluginHandler()->getPluginIds();
		unsigned int msgLen = supportedPlugins.size();
		stream->writeShort(Message::EMCA_SUPPORTED_PLUGINS);
		stream->writeUInt(msgLen);
		for (short &id : supportedPlugins) {
			stream->writeShort(id);
		}
	}
	catch (...)
	{
		return false;
	}
	return true;
}

bool EMCAServer::readRenderInfo(Stream *stream) {
	try {
		RenderInfo renderInfo;
		renderInfo.deserialize(stream);
		m_renderer->updateSampleCount(renderInfo.sampleCount);
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
		std::cout << "Send Camera Information ... !" << std::endl;
		m_renderer->sendCameraData(stream);
		std::cout << "done!" << std::endl;

		std::cout << "Send Mesh Information ... !" << std::endl;
		m_renderer->sendMeshData(stream);
		std::cout << "done!" << std::endl;
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
		std::cout << "Respond Pathdata of pixel: (" << x << ", " << y << ")" << std::endl;
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
	Plugin *plugin = m_dataApi->getPluginById(id);
	if(!plugin) return false;
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

