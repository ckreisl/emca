
#include "dataapisingleton.h"

EMCA_NAMESPACE_BEGIN

DataApiSingleton* DataApiSingleton::m_ptrInstance = 0;

DataApiSingleton* DataApiSingleton::getInstance() {
	if(!m_ptrInstance)
		m_ptrInstance = new DataApiSingleton;
	return m_ptrInstance;
}

EMCA_NAMESPACE_END



