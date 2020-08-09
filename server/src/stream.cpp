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

#include "stream.h"

EMCA_NAMESPACE_BEGIN

Stream::Stream() { }

/* write methods */
void Stream::writeBool(bool value) {
	writeUChar(value);
}

void Stream::writeShort(short value) {
	write(&value, sizeof(short));
}

void Stream::writeUShort(unsigned short value) {
	write(&value, sizeof(unsigned short));
}

void Stream::writeInt(int value) {
	write(&value, sizeof(int));
}

void Stream::writeUInt(unsigned int value) {
	write(&value, sizeof(unsigned int));
}

void Stream::writeLong(long value) {
	write(&value, sizeof(long));
}

void Stream::writeULong(unsigned long value) {
	write(&value, sizeof(unsigned long));
}

void Stream::writeLongLong(long long value) {
	write(&value, sizeof(long long));
}

void Stream::writeChar(char value) {
	write(&value, sizeof(char));
}

void Stream::writeUChar(unsigned char value) {
	write(&value, sizeof(unsigned char));
}

void Stream::writeFloat(float value) {
	write(&value, sizeof(float));
}

void Stream::writeDouble(double value) {
	write(&value, sizeof(double));
}

/* read methods */
inline bool Stream::readBool() {
	return static_cast<bool>(readUChar());
}

short Stream::readShort() {
	short value;
	read(&value, sizeof(short));
	return value;
}

unsigned short Stream::readUShort() {
	unsigned short value;
	read(&value, sizeof(unsigned short));
	return value;
}

int Stream::readInt() {
	int value;
	read(&value, sizeof(int));
	return value;
}

unsigned int Stream::readUInt() {
	unsigned int value;
	read(&value, sizeof(unsigned int));
	return value;
}

long Stream::readLong() {
	long value;
	read(&value, sizeof(long));
	return value;
}

unsigned long Stream::readULong() {
	unsigned long value;
	read(&value, sizeof(unsigned long));
	return value;
}

long long Stream::readLongLong() {
	long long value;
	read(&value, sizeof(long long));
	return value;
}

char Stream::readChar() {
	char value;
	read(&value, sizeof(char));
	return value;
}

unsigned char Stream::readUChar() {
	unsigned char value;
	read(&value, sizeof(unsigned char));
	return value;
}

float Stream::readFloat() {
	float value;
	read(&value, sizeof(float));
	return value;
}

double Stream::readDouble() {
	double value;
	read(&value, sizeof(double));
	return value;
}

/* specific write functions */
std::string Stream::readString() {
    std::string retval;
    char data;

    do {
        read(&data, sizeof(char));
        if (data != 0)
            retval += data;
    } while (data != 0);
    return retval;
}

void Stream::writeString(std::string value) {
	writeInt((int)value.length());
	write(value.c_str(), sizeof(char) * value.length());
}

void Stream::writeFloatArray(const float *data, size_t size) {
	write(data, sizeof(float)*size);
}

void Stream::writeIntArray(const int *data, size_t size) {
	write(data, sizeof(int)*size);
}

template <typename T>
std::string Stream::toString(T number) {
	std::ostringstream oss;
	oss << number;
	return oss.str();
}

EMCA_NAMESPACE_END
