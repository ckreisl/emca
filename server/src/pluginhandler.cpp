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

#include "pluginhandler.h"

EMCA_NAMESPACE_BEGIN

PluginHandler::PluginHandler()  {
	m_plugins = std::map<short, Plugin*>();
}

PluginHandler::~PluginHandler() {
	std::map<short, Plugin*>::iterator it;
	for(it = m_plugins.begin(); it != m_plugins.end(); it++) {
		delete it->second;
	}
}

void PluginHandler::addPlugin(Plugin *plugin) {
	Plugin *temp = getPluginById(plugin->getId());
	if (temp) {
		throw "Plugin ID is already occupied";
	} else {
		m_plugins.insert(std::make_pair(plugin->getId(), plugin));
	}
}

Plugin* PluginHandler::getPluginByName(std::string name) {
	std::map<short, Plugin*>::iterator it;
	for(it = m_plugins.begin(); it != m_plugins.end(); it++) {
		if(it->second->getName() == name)
			return it->second;
	}
	return NULL;
}

Plugin* PluginHandler::getPluginById(short id) {
	return m_plugins.find(id) == m_plugins.end() ? NULL : m_plugins.find(id)->second;
}

std::vector<short> PluginHandler::getPluginIds()
{
	std::vector<short> ret;
	std::map<short, Plugin *>::iterator it;
	for(it = m_plugins.begin(); it != m_plugins.end(); ++it) {
		ret.push_back(it->first);
	}
	return ret;
}

void PluginHandler::serialize(Stream *stream) {
	std::map<short, Plugin*>::iterator it;
	for(it = m_plugins.begin(); it != m_plugins.end(); it++)
		it->second->serialize(stream);
}

void PluginHandler::printPlugins() {
	std::map<short, Plugin*>::iterator it;
	for(it = m_plugins.begin(); it != m_plugins.end(); it++) {
		std::cout << "PluginName: " << it->second->getName() << " PluginID: " << it->second->getId() << std::endl;
	}
}

EMCA_NAMESPACE_END


