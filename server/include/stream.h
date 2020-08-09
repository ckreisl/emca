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

#ifndef INCLUDE_EMCA_STREAM_H
#define INCLUDE_EMCA_STREAM_H

#include "platform.h"

EMCA_NAMESPACE_BEGIN

class Stream {
public:

	Stream();
	virtual ~Stream() { }

	virtual void read(void *ptr, size_t size) = 0;
	virtual void write(const void *ptr, size_t size) = 0;

	/* write methods */
	void writeShort(short value);
	void writeUShort(unsigned short value);
	void writeInt(int value);
	void writeUInt(unsigned int value);
	void writeLong(long value);
	void writeULong(unsigned long value);
	void writeLongLong(long long value);
	void writeChar(char value);
	void writeUChar(unsigned char value);
	void writeBool(bool value);
	void writeFloat(float value);
	void writeDouble(double value);

	/* read methods */
	bool readBool();
	short readShort();
	unsigned short readUShort();
	int readInt();
	unsigned int readUInt();
	long readLong();
	unsigned long readULong();
	long long readLongLong();
	char readChar();
	unsigned char readUChar();
	float readFloat();
	double readDouble();

	/* specific write functions */
	std::string readString();
	void writeString(std::string value);
	void writeFloatArray(const float *data, size_t size);
	void writeIntArray(const int *data, size_t size);

	template <typename T> void writeArray(const T *array, size_t count);
	template <typename T, size_t N> inline void writeArray(const T (&arr)[N]) {
		writeArray(&arr[0], N);
	}

private:
	template <typename T>
	std::string toString(T number);
};

template<> inline void Stream::writeArray(const float *array, size_t count) { return writeFloatArray(array, count); }
template<> inline void Stream::writeArray(const int *array, size_t count) { return writeIntArray(array, count); }

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_STREAM_H */
