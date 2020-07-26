
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


