
#include "pathdata.h"

EMCA_NAMESPACE_BEGIN

UserData::UserData()
{
}

UserData::~UserData()
{
}

void UserData::addBool(std::string s, bool val)
{
    if (m_boolData.find(s) == m_boolData.end())
    {
        m_boolData.insert(std::make_pair(s, std::vector<bool>{val}));
    }
    else
    {
        m_boolData[s].push_back(val);
    }
}

void UserData::addFloat(std::string s, float val)
{
    if (m_floatData.find(s) == m_floatData.end())
    {
        m_floatData.insert(std::make_pair(s, std::vector<float>{val}));
    }
    else
    {
        m_floatData[s].push_back(val);
    }
}

void UserData::addDouble(std::string s, double val)
{
    if (m_doubleData.find(s) == m_doubleData.end())
    {
        m_doubleData.insert(std::make_pair(s, std::vector<double>{val}));
    }
    else
    {
        m_doubleData[s].push_back(val);
    }
}

void UserData::addInt(std::string s, int val)
{
    if (m_intData.find(s) == m_intData.end())
    {
        m_intData.insert(std::make_pair(s, std::vector<int>{val}));
    }
    else
    {
        m_intData[s].push_back(val);
    }
}

void UserData::addPoint2i(std::string s, int x, int y)
{
    if (m_point2iData.find(s) == m_point2iData.end())
    {
        m_point2iData.insert(std::make_pair(s, std::vector<Point2i>{Point2i(x, y)}));
    }
    else
    {
        m_point2iData[s].push_back(Point2i(x, y));
    }
}

void UserData::addPoint2f(std::string s, float x, float y)
{
    if (m_point2fData.find(s) == m_point2fData.end())
    {
        m_point2fData.insert(std::make_pair(s, std::vector<Point2f>{Point2f(x, y)}));
    }
    else
    {
        m_point2fData[s].push_back(Point2f(x, y));
    }
}

void UserData::addPoint3i(std::string s, int x, int y, int z)
{
    if (m_point3iData.find(s) == m_point3iData.end())
    {
        m_point3iData.insert(std::make_pair(s, std::vector<Point3i>{Point3i(x, y, z)}));
    }
    else
    {
        m_point3iData[s].push_back(Point3i(x, y, z));
    }
}

void UserData::addPoint3f(std::string s, float x, float y, float z)
{
    if (m_point3fData.find(s) == m_point3fData.end())
    {
        m_point3fData.insert(std::make_pair(s, std::vector<Point3f>{Point3f(x, y, z)}));
    }
    else
    {
        m_point3fData[s].push_back(Point3f(x, y, z));
    }
}

void UserData::addColor4f(std::string s, float r, float g, float b, float alpha)
{
    if (m_color4fData.find(s) == m_color4fData.end())
    {
        m_color4fData.insert(std::make_pair(s, std::vector<Color4f>{Color4f(r, g, b, alpha)}));
    }
    else
    {
        m_color4fData[s].push_back(Color4f(r, g, b, alpha));
    }
}

void UserData::addString(std::string s, std::string val)
{
    if (m_stringData.find(s) == m_stringData.end())
    {
        m_stringData.insert(std::make_pair(s, std::vector<std::string>{val}));
    }
    else
    {
        m_stringData[s].push_back(val);
    }
}

void UserData::clear()
{
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

void UserData::serialize(Stream *stream)
{

    unsigned int msgLen = m_boolData.size();
    stream->writeUInt(msgLen);
    for (auto &d : m_boolData)
    {
        stream->writeString(d.first);
        stream->writeUInt((unsigned int)d.second.size());
        for (auto v : d.second)
            stream->writeBool(v);
    }

    msgLen = m_floatData.size();
    stream->writeUInt(msgLen);
    for (auto &d : m_floatData)
    {
        stream->writeString(d.first);
        stream->writeUInt((unsigned int)d.second.size());
        for (auto &v : d.second)
            stream->writeFloat(v);
    }

    msgLen = m_doubleData.size();
    stream->writeUInt(msgLen);
    for (auto &d : m_doubleData)
    {
        stream->writeString(d.first);
        stream->writeUInt((unsigned int)d.second.size());
        for (auto &v : d.second)
            stream->writeDouble(v);
    }

    msgLen = m_intData.size();
    stream->writeUInt(msgLen);
    for (auto &d : m_intData)
    {
        stream->writeString(d.first);
        stream->writeUInt((unsigned int)d.second.size());
        for (auto &v : d.second)
            stream->writeInt(v);
    }

    msgLen = m_point2iData.size();
    stream->writeUInt(msgLen);
    for (auto &d : m_point2iData)
    {
        stream->writeString(d.first);
        stream->writeUInt((unsigned int)d.second.size());
        for (auto &v : d.second)
            v.serialize(stream);
    }

    msgLen = m_point2fData.size();
    stream->writeUInt(msgLen);
    for (auto &d : m_point2fData)
    {
        stream->writeString(d.first);
        stream->writeUInt((unsigned int)d.second.size());
        for (auto &v : d.second)
            v.serialize(stream);
    }

    msgLen = m_point3iData.size();
    stream->writeUInt(msgLen);
    for (auto &d : m_point3iData)
    {
        stream->writeString(d.first);
        stream->writeUInt((unsigned int)d.second.size());
        for (auto &v : d.second)
            v.serialize(stream);
    }

    msgLen = m_point3fData.size();
    stream->writeUInt(msgLen);
    for (auto &d : m_point3fData)
    {
        stream->writeString(d.first);
        stream->writeUInt((unsigned int)d.second.size());
        for (auto &v : d.second)
            v.serialize(stream);
    }

    msgLen = m_color4fData.size();
    stream->writeUInt(msgLen);
    for (auto &d : m_color4fData)
    {
        stream->writeString(d.first);
        stream->writeUInt((unsigned int)d.second.size());
        for (auto &v : d.second)
            v.serialize(stream);
    }

    msgLen = m_stringData.size();
    stream->writeUInt(msgLen);
    for (auto &d : m_stringData)
    {
        stream->writeString(d.first);
        stream->writeUInt((unsigned int)d.second.size());
        for (auto &v : d.second)
            stream->writeString(v);
    }
}

IntersectionData::IntersectionData() : UserData()
{
    m_depthIdx = -1;
    m_setPos = false;
    m_setNE = false;
    m_occludedNE = false;
    m_hitEnvmap = false;
    m_setEstimate = false;
}

IntersectionData::IntersectionData(int depthIdx) : UserData()
{
    m_depthIdx = depthIdx;
    m_setPos = false;
    m_setNE = false;
    m_occludedNE = false;
    m_hitEnvmap = false;
    m_setEstimate = false;
}

IntersectionData::~IntersectionData()
{
}

void IntersectionData::setIntersectionPos(Point3f pos)
{
    m_setPos = true;
    m_pos = pos;
}

void IntersectionData::setNextEventEstimationPos(Point3f pos, bool occluded)
{
    m_setNE = true;
    m_posNE = pos;
    m_occludedNE = occluded;
}

void IntersectionData::setIntersectionPosEnvmap(Point3f pos)
{
    m_hitEnvmap = true;
    m_posEnvmap = pos;
}

void IntersectionData::setIntersectionEstimate(Color4f li)
{
    m_setEstimate = true;
    m_estimate = li;
}

void IntersectionData::serialize(Stream *stream)
{
    UserData::serialize(stream);

    stream->writeInt(m_depthIdx);

    stream->writeBool(m_setPos);
    if (m_setPos)
        m_pos.serialize(stream);

    stream->writeBool(m_setNE);
    if (m_setNE)
    {
        m_posNE.serialize(stream);
        stream->writeBool(m_occludedNE);
    }

    stream->writeBool(m_hitEnvmap);
    if (m_hitEnvmap)
        m_posEnvmap.serialize(stream);

    stream->writeBool(m_setEstimate);
    if (m_setEstimate)
        m_estimate.serialize(stream);
}

PathData::PathData() : UserData()
{
    m_sampleIdx = -1;
    m_pathDepth = -1;
    m_setFinalEstimate = false;
    m_visualizePath = false;
    m_visualizeNE = false;
}

PathData::PathData(int sampleIdx) : UserData()
{
    m_sampleIdx = sampleIdx;
    m_pathDepth = -1;
    m_setFinalEstimate = false;
    m_visualizePath = false;
    m_visualizeNE = false;
}

PathData::~PathData() {}

void PathData::setDepthIdx(int depthIdx)
{
    m_segments.insert(std::make_pair(depthIdx, IntersectionData(depthIdx)));
    m_pathDepth = m_segments.size();
}

void PathData::setIntersectionPos(int depthIdx, Point3f pos)
{
    m_segments[depthIdx].setIntersectionPos(pos);
    if (!m_visualizePath)
    {
        m_visualizePath = true;
    }
}

void PathData::setNextEventEstimationPos(int depthIdx, Point3f pos, bool occluded)
{
    m_segments[depthIdx].setNextEventEstimationPos(pos, occluded);
    if (!m_visualizeNE)
    {
        m_visualizeNE = true;
    }
}

void PathData::setIntersectionPosEnvmap(int depthIdx, Point3f pos)
{
    m_segments[depthIdx].setIntersectionPosEnvmap(pos);
}

void PathData::setIntersectionEstimate(int depthIdx, Color4f li)
{
    m_segments[depthIdx].setIntersectionEstimate(li);
}

void PathData::setPathOrigin(Point3f origin)
{
    m_pathOrigin = origin;
}

void PathData::setFinalEstimate(Color4f li)
{
    m_setFinalEstimate = true;
    m_finalEstimate = li;
}

void PathData::addIntersectionData(int depthIdx, std::string s, bool val)
{
    m_segments[depthIdx].addBool(s, val);
}

void PathData::addIntersectionData(int depthIdx, std::string s, float val)
{
    m_segments[depthIdx].addFloat(s, val);
}

void PathData::addIntersectionData(int depthIdx, std::string s, double val)
{
    m_segments[depthIdx].addDouble(s, val);
}

void PathData::addIntersectionData(int depthIdx, std::string s, int val)
{
    m_segments[depthIdx].addInt(s, val);
}

void PathData::addIntersectionData(int depthIdx, std::string s, int x, int y)
{
    m_segments[depthIdx].addPoint2i(s, x, y);
}

void PathData::addIntersectionData(int depthIdx, std::string s, float x, float y)
{
    m_segments[depthIdx].addPoint2f(s, x, y);
}

void PathData::addIntersectionData(int depthIdx, std::string s, int x, int y, int z)
{
    m_segments[depthIdx].addPoint3i(s, x, y, z);
}

void PathData::addIntersectionData(int depthIdx, std::string s, float x, float y, float z)
{
    m_segments[depthIdx].addPoint3f(s, x, y, z);
}

void PathData::addIntersectionData(int depthIdx, std::string s, float r, float g, float b, float alpha)
{
    m_segments[depthIdx].addColor4f(s, r, g, b, alpha);
}

void PathData::addIntersectionData(int depthIdx, std::string s, std::string val)
{
    m_segments[depthIdx].addString(s, val);
}

void PathData::serialize(Stream *stream)
{
    UserData::serialize(stream);

    stream->writeInt(m_sampleIdx);
    stream->writeInt(m_pathDepth);

    m_pathOrigin.serialize(stream);

    stream->writeBool(m_setFinalEstimate);
    if (m_setFinalEstimate)
        m_finalEstimate.serialize(stream);

    /* depending on boolean draw paths or
	 * next event estimations on client */
    stream->writeBool(m_visualizePath);
    stream->writeBool(m_visualizeNE);

    stream->writeUInt((unsigned int)m_segments.size());
    for (auto &seg : m_segments)
    {
        stream->writeInt(seg.first);
        seg.second.serialize(stream);
    }
}

void PathData::clear()
{
    m_visualizeNE = false;
    m_visualizePath = false;
    m_segments.clear();
}

EMCA_NAMESPACE_END
