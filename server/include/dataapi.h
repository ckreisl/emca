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

#ifndef INCLUDE_EMCA_DATAAPI_H_
#define INCLUDE_EMCA_DATAAPI_H_

#include "platform.h"
#include "stream.h"
#include "pluginhandler.h"
#include "pathdata.h"

EMCA_NAMESPACE_BEGIN

class DataApi {
public:

	DataApi();
	virtual ~DataApi();

	void setSampleIdx(int sampleIdx);
	void setDepthIdx(int depthIdx);

	void setPathOrigin(float x, float y, float z);
	void setIntersectionPos(float x, float y, float z);
	void setNextEventEstimationPos(float x, float y, float z, bool occluded);
	void setIntersectionPosEnvmap(float x, float y, float z);
	void setIntersectionEstimate(float r, float g, float b, float alpha = 1.0);
	void setFinalEstimate(float r, float g, float b, float alpha = 1.0);

	void addIntersectionData(std::string s, bool val);
	void addIntersectionData(std::string s, float val);
	void addIntersectionData(std::string s, double val);
	void addIntersectionData(std::string s, int val);
	void addIntersectionData(std::string s, int x, int y);
	void addIntersectionData(std::string s, float x, float y);
	void addIntersectionData(std::string s, int x, int y, int z);
	void addIntersectionData(std::string s, float x, float y, float z);
	void addIntersectionData(std::string s, float r, float g, float b, float alpha);
	void addIntersectionData(std::string s, std::string val);

	void addPathData(std::string s, bool val);
	void addPathData(std::string s, float val);
	void addPathData(std::string s, double val);
	void addPathData(std::string s, int val);
	void addPathData(std::string s, int x, int y);
	void addPathData(std::string s, float x, float y);
	void addPathData(std::string s, int x, int y, int z);
	void addPathData(std::string s, float x, float y, float z);
	void addPathData(std::string s, float r, float g, float b, float alpha);
	void addPathData(std::string s, std::string val);

	void serialize(Stream *stream);

	void clear();
	void enable();
	void disable();

	void addPlugin(Plugin *plugin) { m_pluginHandler->addPlugin(plugin); }
	Plugin* getPluginByName(std::string name) { return m_pluginHandler->getPluginByName(name); }
	Plugin* getPluginById(short id) { return m_pluginHandler->getPluginById(id); }
	PluginHandler* getPluginHandler() { return m_pluginHandler; }

	inline bool isCollecting() { return m_isCollecting; }

private:
	bool m_isCollecting;
	int m_currentSampleIdx = -1;
	int m_currentDepthIdx = -1;
	std::map<int, PathData> m_paths;
	PluginHandler *m_pluginHandler;
};

EMCA_NAMESPACE_END

#endif // INCLUDE_EMCA_DATAAPI_H_
