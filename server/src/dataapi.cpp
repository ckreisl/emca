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

#include "dataapi.h"
#include "messages.h"

EMCA_NAMESPACE_BEGIN

DataApi::DataApi() {
	m_isCollecting = false;
	m_pluginHandler = new PluginHandler();
}

DataApi::~DataApi() {
	delete m_pluginHandler;
}

void DataApi::enable() {
	m_isCollecting = true;
}

void DataApi::disable() {
	m_isCollecting = false;
}

void DataApi::clear() {
	m_paths.clear();
}

void DataApi::setSampleIdx(int sampleIdx) {
	if(!m_isCollecting) return;
	m_currentSampleIdx = sampleIdx;
	m_paths.insert(std::make_pair(sampleIdx, PathData(sampleIdx)));
}

void DataApi::setDepthIdx(int depthIdx) {
	if(!m_isCollecting) return;
	m_currentDepthIdx = depthIdx;
	m_paths[m_currentSampleIdx].setDepthIdx(depthIdx);
}

void DataApi::setPathOrigin(float x, float y, float z) {
	if(!m_isCollecting) return;
	m_paths[m_currentSampleIdx].setPathOrigin(Point3f(x, y, z));
}

void DataApi::setIntersectionPos(float x, float y, float z) {
	if(!m_isCollecting) return;
	m_paths[m_currentSampleIdx].setIntersectionPos(m_currentDepthIdx, Point3f(x, y, z));
}

void DataApi::setNextEventEstimationPos(float x, float y, float z, bool occluded) {
	if(!m_isCollecting || m_currentDepthIdx == -1) return;
	m_paths[m_currentSampleIdx].setNextEventEstimationPos(m_currentDepthIdx, Point3f(x, y, z), occluded);
}

void DataApi::setIntersectionPosEnvmap(float x, float y, float z) {
	if(!m_isCollecting || m_currentDepthIdx == -1) return;
	m_paths[m_currentSampleIdx].setIntersectionPosEnvmap(m_currentDepthIdx, Point3f(x, y, z));
}

void DataApi::setIntersectionEstimate(float r, float g, float b, float alpha) {
	if(!m_isCollecting || m_currentDepthIdx == -1) return;
	m_paths[m_currentSampleIdx].setIntersectionEstimate(m_currentDepthIdx, Color4f(r, g, b, alpha));
}

void DataApi::setFinalEstimate(float r, float g, float b, float alpha) {
	if(!m_isCollecting) return;
	m_paths[m_currentSampleIdx].setFinalEstimate(Color4f(r, g, b, alpha));
}

void DataApi::addIntersectionData(std::string s, bool val) {
	if(!m_isCollecting || m_currentDepthIdx == -1) return;
	m_paths[m_currentSampleIdx].addIntersectionData(m_currentDepthIdx, s, val);
}

void DataApi::addIntersectionData(std::string s, float val) {
	if(!m_isCollecting || m_currentDepthIdx == -1) return;
	m_paths[m_currentSampleIdx].addIntersectionData(m_currentDepthIdx, s, val);
}

void DataApi::addIntersectionData(std::string s, double val) {
	if(!m_isCollecting || m_currentDepthIdx == -1) return;
	m_paths[m_currentSampleIdx].addIntersectionData(m_currentDepthIdx, s, val);
}

void DataApi::addIntersectionData(std::string s, int val) {
	if(!m_isCollecting || m_currentDepthIdx == -1) return;
	m_paths[m_currentSampleIdx].addIntersectionData(m_currentDepthIdx, s, val);
}

void DataApi::addIntersectionData(std::string s, int x, int y) {
	if(!m_isCollecting || m_currentDepthIdx == -1) return;
	m_paths[m_currentSampleIdx].addIntersectionData(m_currentDepthIdx, s, x, y);
}

void DataApi::addIntersectionData(std::string s, float x, float y) {
	if(!m_isCollecting || m_currentDepthIdx == -1) return;
	m_paths[m_currentSampleIdx].addIntersectionData(m_currentDepthIdx, s, x, y);
}

void DataApi::addIntersectionData(std::string s, int x, int y, int z) {
	if(!m_isCollecting || m_currentDepthIdx == -1) return;
	m_paths[m_currentSampleIdx].addIntersectionData(m_currentDepthIdx, s, x, y, z);
}

void DataApi::addIntersectionData(std::string s, float x, float y, float z) {
	if(!m_isCollecting || m_currentDepthIdx == -1) return;
	m_paths[m_currentSampleIdx].addIntersectionData(m_currentDepthIdx, s, x, y, z);
}

void DataApi::addIntersectionData(std::string s, float r, float g, float b, float alpha) {
	if(!m_isCollecting || m_currentDepthIdx == -1) return;
	m_paths[m_currentSampleIdx].addIntersectionData(m_currentDepthIdx, s, r, g, b, alpha);
}

void DataApi::addIntersectionData(std::string s, std::string val) {
	if(!m_isCollecting || m_currentDepthIdx == -1) return;
	m_paths[m_currentSampleIdx].addIntersectionData(m_currentDepthIdx, s, val);
}

void DataApi::addPathData(std::string s, bool val) {
	if(!m_isCollecting) return;
	m_paths[m_currentSampleIdx].addBool(s, val);
}

void DataApi::addPathData(std::string s, float val) {
	if(!m_isCollecting) return;
	m_paths[m_currentSampleIdx].addFloat(s, val);
}

void DataApi::addPathData(std::string s, double val) {
	if(!m_isCollecting) return;
	m_paths[m_currentSampleIdx].addDouble(s, val);
}

void DataApi::addPathData(std::string s, int val) {
	if(!m_isCollecting) return;
	m_paths[m_currentSampleIdx].addInt(s, val);
}

void DataApi::addPathData(std::string s, int x, int y) {
	if(!m_isCollecting) return;
	m_paths[m_currentSampleIdx].addPoint2i(s, x, y);
}

void DataApi::addPathData(std::string s, float x, float y) {
	if(!m_isCollecting) return;
	m_paths[m_currentSampleIdx].addPoint2f(s, x, y);
}

void DataApi::addPathData(std::string s, int x, int y, int z) {
	if(!m_isCollecting) return;
	m_paths[m_currentSampleIdx].addPoint3i(s, x, y, z);
}

void DataApi::addPathData(std::string s, float x, float y, float z) {
	if(!m_isCollecting) return;
	m_paths[m_currentSampleIdx].addPoint3f(s, x, y, z);
}

void DataApi::addPathData(std::string s, float r, float g, float b, float alpha) {
	if(!m_isCollecting) return;
	m_paths[m_currentSampleIdx].addColor4f(s, r, g, b, alpha);
}

void DataApi::addPathData(std::string s, std::string val) {
	if(!m_isCollecting) return;
	m_paths[m_currentSampleIdx].addString(s, val);
}

void DataApi::serialize(Stream *stream) {
	stream->writeShort(Message::EMCA_RENDER_PIXEL);
	stream->writeUInt((unsigned int)m_paths.size());
	/* serialize path data */
	for(auto& path : m_paths) {
		path.second.serialize(stream);
	}
}

EMCA_NAMESPACE_END

