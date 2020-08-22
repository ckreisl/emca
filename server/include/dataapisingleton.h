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

#ifndef EXT_EMCA_DATAAPISINGLETON_H_
#define EXT_EMCA_DATAAPISINGLETON_H_

#include <atomic>
#include <mutex>

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
	static std::atomic<DataApiSingleton* > m_ptrInstance;
	static std::mutex m_mutex;
};

EMCA_NAMESPACE_END

#endif /* EXT_EMCA_DATAAPISINGLETON_H_ */
