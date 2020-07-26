#ifndef INCLUDE_EMCA_USERDATA_H_
#define INCLUDE_EMCA_USERDATA_H_

#include "platform.h"
#include "datatypes.h"
#include "stream.h"

EMCA_NAMESPACE_BEGIN

class UserData {
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
	std::map<std::string, std::vector<bool> > m_boolData;
	std::map<std::string, std::vector<float> > m_floatData;
	std::map<std::string, std::vector<double> > m_doubleData;
	std::map<std::string, std::vector<int> > m_intData;
	std::map<std::string, std::vector<Point2i> > m_point2iData;
	std::map<std::string, std::vector<Point2f> > m_point2fData;
	std::map<std::string, std::vector<Point3i> > m_point3iData;
	std::map<std::string, std::vector<Point3f> > m_point3fData;
	std::map<std::string, std::vector<Color4f> > m_color4fData;
	std::map<std::string, std::vector<std::string> > m_stringData;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_USERDATA_H_ */
