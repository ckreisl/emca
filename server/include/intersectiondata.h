#ifndef INCLUDE_EMCA_INTERSECTIONDATA_H_
#define INCLUDE_EMCA_INTERSECTIONDATA_H_

#include "platform.h"
#include "userdata.h"
#include "stream.h"

EMCA_NAMESPACE_BEGIN

class IntersectionData : public UserData {
public:

	IntersectionData();
	IntersectionData(int depthIdx);
	~IntersectionData();

	void setIntersectionPos(Point3f pos);
	void setNextEventEstimationPos(Point3f pos, bool occluded);
	void setIntersectionPosEnvmap(Point3f pos);
	void setIntersectionEstimate(Color4f li);

	void serialize(Stream *stream);

private:
	int m_depthIdx;			/* current path depth */
	Point3f m_pos;			/* intersection point in world coordinates */
	Point3f m_posNE;		/* next event estimation point in world coordinates */
	Point3f m_posEnvmap;	/* is set if last ray intersects with environment map */
	Color4f m_estimate;		/* current computed estimate at this intersection */

	bool m_setPos;
	bool m_setNE;
	bool m_occludedNE;
	bool m_hitEnvmap;
	bool m_setEstimate;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_INTERSECTIONDATA_H_ */
