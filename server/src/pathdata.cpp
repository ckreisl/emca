
#include "pathdata.h"

EMCA_NAMESPACE_BEGIN

PathData::PathData() : UserData() {
	m_sampleIdx = -1;
	m_pathDepth = -1;
	m_setFinalEstimate = false;
	m_visualizePath = false;
	m_visualizeNE = false;
}

PathData::PathData(int sampleIdx) : UserData() {
	m_sampleIdx = sampleIdx;
	m_pathDepth = -1;
	m_setFinalEstimate = false;
	m_visualizePath = false;
	m_visualizeNE = false;
}

PathData::~PathData() { }

void PathData::setDepthIdx(int depthIdx) {
	m_segments.insert(std::make_pair(depthIdx, IntersectionData(depthIdx)));
	m_pathDepth = m_segments.size();
}

void PathData::setIntersectionPos(int depthIdx, Point3f pos) {
	m_segments[depthIdx].setIntersectionPos(pos);
	if (!m_visualizePath) { m_visualizePath = true; }
}

void PathData::setNextEventEstimationPos(int depthIdx, Point3f pos, bool occluded) {
	m_segments[depthIdx].setNextEventEstimationPos(pos, occluded);
	if (!m_visualizeNE) { m_visualizeNE = true; }
}

void PathData::setIntersectionPosEnvmap(int depthIdx, Point3f pos) {
	m_segments[depthIdx].setIntersectionPosEnvmap(pos);
}

void PathData::setIntersectionEstimate(int depthIdx, Color4f li) {
	m_segments[depthIdx].setIntersectionEstimate(li);
}

void PathData::setPathOrigin(Point3f origin) {
	m_pathOrigin = origin;
}

void PathData::setFinalEstimate(Color4f li) {
	m_setFinalEstimate = true;
	m_finalEstimate = li;
}

void PathData::addIntersectionData(int depthIdx, std::string s, bool val) {
	m_segments[depthIdx].addBool(s, val);
}

void PathData::addIntersectionData(int depthIdx, std::string s, float val) {
	m_segments[depthIdx].addFloat(s, val);
}

void PathData::addIntersectionData(int depthIdx, std::string s, double val) {
	m_segments[depthIdx].addDouble(s, val);
}

void PathData::addIntersectionData(int depthIdx, std::string s, int val) {
	m_segments[depthIdx].addInt(s, val);
}

void PathData::addIntersectionData(int depthIdx, std::string s, int x, int y) {
	m_segments[depthIdx].addPoint2i(s, x, y);
}

void PathData::addIntersectionData(int depthIdx, std::string s, float x, float y) {
	m_segments[depthIdx].addPoint2f(s, x, y);
}

void PathData::addIntersectionData(int depthIdx, std::string s, int x, int y, int z) {
	m_segments[depthIdx].addPoint3i(s, x, y, z);
}

void PathData::addIntersectionData(int depthIdx, std::string s, float x, float y, float z) {
	m_segments[depthIdx].addPoint3f(s, x, y, z);
}

void PathData::addIntersectionData(int depthIdx, std::string s, float r, float g, float b, float alpha) {
	m_segments[depthIdx].addColor4f(s, r, g, b, alpha);
}

void PathData::addIntersectionData(int depthIdx, std::string s, std::string val) {
    m_segments[depthIdx].addString(s, val);
}

void PathData::serialize(Stream *stream) {
	UserData::serialize(stream);

	stream->writeInt(m_sampleIdx);
	stream->writeInt(m_pathDepth);

	m_pathOrigin.serialize(stream);

	stream->writeBool(m_setFinalEstimate);
	if(m_setFinalEstimate)
		m_finalEstimate.serialize(stream);

	/* depending on boolean draw paths or
	 * next event estimations on client */
	stream->writeBool(m_visualizePath);
	stream->writeBool(m_visualizeNE);

	stream->writeUInt((unsigned int)m_segments.size());
	for(auto &seg : m_segments) {
		stream->writeInt(seg.first);
		seg.second.serialize(stream);
	}
}

void PathData::clear() {
	m_visualizeNE = false;
	m_visualizePath = false;
	m_segments.clear();
}

EMCA_NAMESPACE_END

