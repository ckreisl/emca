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

#ifndef EMCA_INCLUDE_RENDERINTERFACE_H_
#define EMCA_INCLUDE_RENDERINTERFACE_H_

#include "platform.h"
#include "stream.h"

EMCA_NAMESPACE_BEGIN

class RenderInterface {
public:
	virtual ~RenderInterface() { }
	virtual void renderImage() = 0;
	virtual void renderPixel(unsigned int x, unsigned int y, int sampleCount) = 0;
	virtual void sendRenderInformation(Stream *stream) = 0;
	virtual void sendCameraData(Stream *stream) = 0;
	virtual void sendMeshData(Stream *stream) = 0;
	virtual void updateSampleCount(int sampleCount) = 0;
};

EMCA_NAMESPACE_END

#endif /* EMCA_INCLUDE_EMCARENDERINTERFACE_H_ */
