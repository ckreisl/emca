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
