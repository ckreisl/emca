#ifndef EXT_EMCA_DATAAPISINGLETON_H_
#define EXT_EMCA_DATAAPISINGLETON_H_

#include "platform.h"
#include "dataapi.h"

EMCA_NAMESPACE_BEGIN

/**
 * Singleton Pattern
 */

class DataApiSingleton : public DataApi {
public:
	static DataApiSingleton* getInstance();

private:
	DataApiSingleton() : emca::DataApi() { }
	DataApiSingleton(DataApiSingleton const&) = delete;
	~DataApiSingleton() { }
	void operator=(const DataApiSingleton &) = delete;
	static DataApiSingleton *m_ptrInstance;
};

EMCA_NAMESPACE_END

#endif /* EXT_EMCA_DATAAPISINGLETON_H_ */
