#ifndef INCLUDE_EMCA_MESH_H_
#define INCLUDE_EMCA_MESH_H_

#include "platform.h"
#include "datatypes.h"
#include "stream.h"

EMCA_NAMESPACE_BEGIN

class Mesh {
public:
	Mesh();
	~Mesh();

	void addVertices(Point3f* p3f, size_t numPoints);
    void addTriangles(Vec3i* vec3i, size_t numTriangles);

	void addVertexPosition(Point3f &p3f) { m_vertexPositions.push_back(p3f); }
	void addTriangleIndices(Vec3i &vec3i) { m_triangleIndices.push_back(vec3i); }
	void clearVertexPositions() { m_vertexPositions.clear(); }
	void clearTriangleIndices() { m_triangleIndices.clear(); }
    size_t getVertexCount() { return m_vertexPositions.size(); }
    size_t getTriangleCount() { return m_triangleIndices.size(); }

	void setDiffuseColor(Color4f &c) { m_diffuseColor = c; }
	void setSpecularColor(Color4f &c) { m_spectrumColor = c; }

	void serialize(Stream *stream);

private:
	std::vector<Point3f> m_vertexPositions;
	std::vector<Vec3i> m_triangleIndices;
	Color4f m_spectrumColor;
	Color4f m_diffuseColor;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_MESH_H_ */
