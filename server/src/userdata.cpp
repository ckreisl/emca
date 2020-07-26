
#include "userdata.h"

EMCA_NAMESPACE_BEGIN

UserData::UserData() {

}

UserData::~UserData() {

}

void UserData::addBool(std::string s, bool val) {
	if(m_boolData.find(s) == m_boolData.end()) {
		m_boolData.insert(std::make_pair(s, std::vector<bool>{val}));
	} else {
		m_boolData[s].push_back(val);
	}
}

void UserData::addFloat(std::string s, float val) {
	if(m_floatData.find(s) == m_floatData.end()) {
		m_floatData.insert(std::make_pair(s, std::vector<float>{val}));
	} else {
		m_floatData[s].push_back(val);
	}
}

void UserData::addDouble(std::string s, double val) {
	if(m_doubleData.find(s) == m_doubleData.end()) {
		m_doubleData.insert(std::make_pair(s, std::vector<double>{val}));
	} else {
		m_doubleData[s].push_back(val);
	}
}

void UserData::addInt(std::string s, int val) {
	if(m_intData.find(s) == m_intData.end()) {
		m_intData.insert(std::make_pair(s, std::vector<int>{val}));
	} else {
		m_intData[s].push_back(val);
	}
}

void UserData::addPoint2i(std::string s, int x, int y) {
	if(m_point2iData.find(s) == m_point2iData.end()) {
		m_point2iData.insert(std::make_pair(s, std::vector<Point2i>{Point2i(x, y)}));
	} else {
		m_point2iData[s].push_back(Point2i(x, y));
	}
}

void UserData::addPoint2f(std::string s, float x, float y) {
	if(m_point2fData.find(s) == m_point2fData.end()) {
		m_point2fData.insert(std::make_pair(s, std::vector<Point2f>{Point2f(x, y)}));
	} else {
		m_point2fData[s].push_back(Point2f(x, y));
	}
}

void UserData::addPoint3i(std::string s, int x, int y, int z) {
	if(m_point3iData.find(s) == m_point3iData.end()) {
		m_point3iData.insert(std::make_pair(s, std::vector<Point3i>{Point3i(x, y, z)}));
	} else {
		m_point3iData[s].push_back(Point3i(x, y, z));
	}
}

void UserData::addPoint3f(std::string s, float x, float y, float z) {
	if(m_point3fData.find(s) == m_point3fData.end()) {
		m_point3fData.insert(std::make_pair(s, std::vector<Point3f>{Point3f(x, y, z)}));
	} else {
		m_point3fData[s].push_back(Point3f(x, y, z));
	}
}

void UserData::addColor4f(std::string s, float r, float g, float b, float alpha) {
	if(m_color4fData.find(s) == m_color4fData.end()) {
		m_color4fData.insert(std::make_pair(s, std::vector<Color4f>{Color4f(r, g, b, alpha)}));
	} else {
		m_color4fData[s].push_back(Color4f(r, g, b, alpha));
    }
}

void UserData::addString(std::string s, std::string val) {
    if(m_stringData.find(s) == m_stringData.end()) {
        m_stringData.insert(std::make_pair(s, std::vector<std::string>{val}));
    } else {
        m_stringData[s].push_back(val);
    }
}

void UserData::clear() {
	m_boolData.clear();
	m_floatData.clear();
	m_doubleData.clear();
	m_intData.clear();
	m_point2iData.clear();
	m_point2fData.clear();
	m_point3fData.clear();
	m_point3iData.clear();
	m_color4fData.clear();
    m_stringData.clear();
}

void UserData::serialize(Stream *stream) {

	unsigned int msgLen = m_boolData.size();
	stream->writeUInt(msgLen);
	for(auto &d : m_boolData) {
		stream->writeString(d.first);
		stream->writeUInt((unsigned int) d.second.size());
		for(auto v : d.second)
			stream->writeBool(v);
	}

	msgLen = m_floatData.size();
	stream->writeUInt(msgLen);
	for(auto &d : m_floatData) {
		stream->writeString(d.first);
		stream->writeUInt((unsigned int) d.second.size());
		for(auto &v : d.second)
			stream->writeFloat(v);
	}

	msgLen = m_doubleData.size();
	stream->writeUInt(msgLen);
	for(auto &d : m_doubleData) {
		stream->writeString(d.first);
		stream->writeUInt((unsigned int) d.second.size());
		for(auto &v : d.second)
			stream->writeDouble(v);
	}

	msgLen = m_intData.size();
	stream->writeUInt(msgLen);
	for(auto &d : m_intData) {
		stream->writeString(d.first);
		stream->writeUInt((unsigned int) d.second.size());
		for(auto &v : d.second)
			stream->writeInt(v);
	}

	msgLen = m_point2iData.size();
	stream->writeUInt(msgLen);
	for(auto &d : m_point2iData) {
		stream->writeString(d.first);
		stream->writeUInt((unsigned int) d.second.size());
		for(auto &v : d.second)
			v.serialize(stream);
	}

	msgLen = m_point2fData.size();
	stream->writeUInt(msgLen);
	for(auto &d : m_point2fData) {
		stream->writeString(d.first);
		stream->writeUInt((unsigned int) d.second.size());
		for(auto &v : d.second)
			v.serialize(stream);
	}

	msgLen = m_point3iData.size();
	stream->writeUInt(msgLen);
	for(auto &d : m_point3iData) {
		stream->writeString(d.first);
		stream->writeUInt((unsigned int) d.second.size());
		for(auto &v : d.second)
			v.serialize(stream);
	}

	msgLen = m_point3fData.size();
	stream->writeUInt(msgLen);
	for(auto &d : m_point3fData) {
		stream->writeString(d.first);
		stream->writeUInt((unsigned int) d.second.size());
		for(auto &v : d.second)
			v.serialize(stream);
	}

	msgLen = m_color4fData.size();
	stream->writeUInt(msgLen);
	for(auto &d : m_color4fData) {
		stream->writeString(d.first);
		stream->writeUInt((unsigned int) d.second.size());
		for(auto &v : d.second)
			v.serialize(stream);
	}

    msgLen = m_stringData.size();
    stream->writeUInt(msgLen);
    for(auto &d : m_stringData) {
        stream->writeString(d.first);
        stream->writeUInt((unsigned int) d.second.size());
        for(auto &v : d.second)
            stream->writeString(v);
    }
}

EMCA_NAMESPACE_END

