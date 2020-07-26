#ifndef INCLUDE_EMCA_PATHDATA_H_
#define INCLUDE_EMCA_PATHDATA_H_

#include "platform.h"
#include "userdata.h"
#include "stream.h"
#include "intersectiondata.h"

EMCA_NAMESPACE_BEGIN

class PathData : public UserData {
public:

	PathData();
	PathData(int sampleIdx);
	~PathData();

	void setDepthIdx(int depthIdx);
	void setIntersectionPos(int depthIdx, Point3f pos);
	void setNextEventEstimationPos(int depthIdx, Point3f pos, bool occluded);
	void setIntersectionPosEnvmap(int depthIdx, Point3f pos);
	void setIntersectionEstimate(int depthIdx, Color4f li);

	void setPathOrigin(Point3f origin);
	void setFinalEstimate(Color4f li);

	void addIntersectionData(int depthIdx, std::string s, bool val);
	void addIntersectionData(int depthIdx, std::string s, float val);
	void addIntersectionData(int depthIdx, std::string s, double val);
	void addIntersectionData(int depthIdx, std::string s, int val);
	void addIntersectionData(int depthIdx, std::string s, int x, int y);
	void addIntersectionData(int depthIdx, std::string s, float x, float y);
	void addIntersectionData(int depthIdx, std::string s, int x, int y, int z);
	void addIntersectionData(int depthIdx, std::string s, float x, float y, float z);
	void addIntersectionData(int depthIdx, std::string s, float r, float g, float b, float alpha);
    void addIntersectionData(int depthIdx, std::string s, std::string val);

	void serialize(Stream *stream);
	void clear();

private:
	int m_sampleIdx; 							/* Current sample index */
	int m_pathDepth; 							/* Path length, amount of Intersections */
	Point3f m_pathOrigin;						/* Path origin */
	Color4f m_finalEstimate;					/* final light estimation of path */
	std::map<int, IntersectionData> m_segments;	/* data dictionary about each segment (intersection) */

	bool m_setFinalEstimate;
	bool m_visualizePath;
	bool m_visualizeNE;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_VSDPATHDATA_H_ */
