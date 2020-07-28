
#include "dataapisingleton.h"

EMCA_NAMESPACE_BEGIN

std::atomic<DataApiSingleton *> DataApiSingleton::m_ptrInstance;
std::mutex DataApiSingleton::m_mutex;

DataApiSingleton* DataApiSingleton::getInstance() {
	DataApiSingleton *singleton = m_ptrInstance.load(std::memory_order_acquire);
	if(!m_ptrInstance) {
		std::lock_guard<std::mutex> myLock(m_mutex);
		m_ptrInstance = new DataApiSingleton();
		if(!m_ptrInstance) {
			m_ptrInstance.store(singleton, std::memory_order_release);
		}
	}
	return m_ptrInstance;
}

EMCA_NAMESPACE_END



