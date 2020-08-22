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

#ifndef INCLUDE_EMCA_MESSAGES_H_
#define INCLUDE_EMCA_MESSAGES_H_

#include "platform.h"

EMCA_NAMESPACE_BEGIN

enum Message {
	EMCA_HELLO 		 		= 0x0001,
	EMCA_HEADER_RENDER_INFO = 0x000A,
	EMCA_SET_RENDER_INFO 	= 0x000B,
	EMCA_RENDER_IMAGE 		= 0x000D,
	EMCA_RENDER_PIXEL 		= 0x000E,
	EMCA_HEADER_SCENE_DATA	= 0x000F,
	EMCA_HEADER_CAMERA		= 0x0010,
	EMCA_SUPPORTED_PLUGINS	= 0x0011,
	EMCA_DISCONNECT			= 0x1bcc,
	EMCA_QUIT		 		= 0x1bcd
};

enum MeshType
{
	TriangleMesh 			= 0,
	SphereMesh 				= 1
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_MESSAGES_H_ */
