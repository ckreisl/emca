#ifndef INCLUDE_EMCA_PLUGINHANDLER_H_
#define INCLUDE_EMCA_PLUGINHANDLER_H_

#include "platform.h"
#include "stream.h"
#include "plugin.h"

EMCA_NAMESPACE_BEGIN

class PluginHandler {
public:

	PluginHandler();
	~PluginHandler();

	void addPlugin(Plugin *plugin);

	Plugin* getPluginByName(std::string name);
	Plugin* getPluginById(short id);

	std::vector<short> getPluginIds();

	void serialize(Stream *stream);
	void printPlugins();

private:
	std::map<short, Plugin*> m_plugins;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_PLUGINHANDLER_H_ */
