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



