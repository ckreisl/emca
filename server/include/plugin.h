#ifndef INCLUDE_EMCA_PLUGIN_H_
#define INCLUDE_EMCA_PLUGIN_H_

#include "platform.h"
#include "stream.h"

EMCA_NAMESPACE_BEGIN

class Plugin {
public:

	Plugin(std::string name, short id) : m_name(name), m_id(id) { }
	virtual ~Plugin() { }

	virtual void run() = 0;
	virtual void serialize(Stream *stream) = 0;
	virtual void deserialize(Stream *stream) = 0;

	inline std::string getName() const { return m_name; }
	inline short getId() const { return m_id; }

private:
	short m_id;
	std::string m_name;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_PLUGIN_H_ */
