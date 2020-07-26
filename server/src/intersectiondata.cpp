
#include "intersectiondata.h"

EMCA_NAMESPACE_BEGIN

IntersectionData::IntersectionData() : UserData() {
	m_depthIdx = -1;
	m_setPos = false;
	m_setNE = false;
	m_occludedNE = false;
	m_hitEnvmap = false;
	m_setEstimate = false;
}

IntersectionData::IntersectionData(int depthIdx) : UserData() {
	m_depthIdx = depthIdx;
	m_setPos = false;
	m_setNE = false;
	m_occludedNE = false;
	m_hitEnvmap = false;
	m_setEstimate = false;
}

IntersectionData::~IntersectionData() {

}

void IntersectionData::setIntersectionPos(Point3f pos) {
	m_setPos = true;
	m_pos = pos;
}

void IntersectionData::setNextEventEstimationPos(Point3f pos, bool occluded) {
	m_setNE = true;
	m_posNE = pos;
	m_occludedNE = occluded;
}

void IntersectionData::setIntersectionPosEnvmap(Point3f pos) {
	m_hitEnvmap = true;
	m_posEnvmap = pos;
}

void IntersectionData::setIntersectionEstimate(Color4f li) {
	m_setEstimate = true;
	m_estimate = li;
}

void IntersectionData::serialize(Stream *stream) {
	UserData::serialize(stream);

	stream->writeInt(m_depthIdx);

	stream->writeBool(m_setPos);
	if(m_setPos)
		m_pos.serialize(stream);

	stream->writeBool(m_setNE);
	if(m_setNE) {
		m_posNE.serialize(stream);
		stream->writeBool(m_occludedNE);
	}

	stream->writeBool(m_hitEnvmap);
	if(m_hitEnvmap)
		m_posEnvmap.serialize(stream);

	stream->writeBool(m_setEstimate);
	if(m_setEstimate)
		m_estimate.serialize(stream);
}

EMCA_NAMESPACE_END


