#ifndef INCLUDE_EMCA_PATHDATA_H_
#define INCLUDE_EMCA_PATHDATA_H_

#include "platform.h"
#include "datatypes.h"
#include "stream.h"

EMCA_NAMESPACE_BEGIN

class UserData
{
public:
    UserData();
    virtual ~UserData();

    void addBool(std::string s, bool val);
    void addFloat(std::string s, float val);
    void addDouble(std::string s, double val);
    void addInt(std::string s, int val);
    void addPoint2i(std::string s, int x, int y);
    void addPoint2f(std::string s, float x, float y);
    void addPoint3i(std::string s, int x, int y, int z);
    void addPoint3f(std::string s, float x, float y, float z);
    void addColor4f(std::string s, float r, float g, float b, float alpha);
    void addString(std::string s, std::string val);

    void serialize(Stream *stream);
    void clear();

private:
    std::map<std::string, std::vector<bool>> m_boolData;
    std::map<std::string, std::vector<float>> m_floatData;
    std::map<std::string, std::vector<double>> m_doubleData;
    std::map<std::string, std::vector<int>> m_intData;
    std::map<std::string, std::vector<Point2i>> m_point2iData;
    std::map<std::string, std::vector<Point2f>> m_point2fData;
    std::map<std::string, std::vector<Point3i>> m_point3iData;
    std::map<std::string, std::vector<Point3f>> m_point3fData;
    std::map<std::string, std::vector<Color4f>> m_color4fData;
    std::map<std::string, std::vector<std::string>> m_stringData;
};

class IntersectionData : public UserData
{
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
    int m_depthIdx;      /* current path depth */
    Point3f m_pos;       /* intersection point in world coordinates */
    Point3f m_posNE;     /* next event estimation point in world coordinates */
    Point3f m_posEnvmap; /* is set if last ray intersects with environment map */
    Color4f m_estimate;  /* current computed estimate at this intersection */

    bool m_setPos;
    bool m_setNE;
    bool m_occludedNE;
    bool m_hitEnvmap;
    bool m_setEstimate;
};

class PathData : public UserData
{
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
    int m_sampleIdx;                            /* Current sample index */
    int m_pathDepth;                            /* Path length, amount of Intersections */
    Point3f m_pathOrigin;                       /* Path origin */
    Color4f m_finalEstimate;                    /* final light estimation of path */
    std::map<int, IntersectionData> m_segments; /* data dictionary about each segment (intersection) */

    bool m_setFinalEstimate;
    bool m_visualizePath;
    bool m_visualizeNE;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_VSDPATHDATA_H_ */