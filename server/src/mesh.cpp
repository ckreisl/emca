
#include "mesh.h"
#include "messages.h"

EMCA_NAMESPACE_BEGIN

Mesh::Mesh() {
	m_spectrumColor = Color4f(0, 0, 0);
	m_diffuseColor = Color4f(0, 0, 0);
}

Mesh::~Mesh() { }

void Mesh::addVertices(Point3f *p3f, size_t numPoints) {
	m_vertexPositions.reserve(m_vertexPositions.size() + numPoints);
	m_vertexPositions.insert(m_vertexPositions.end(), p3f, p3f + numPoints);
}

void Mesh::addTriangles(Vec3i *vec3i, size_t numTriangles) {
	m_triangleIndices.reserve(m_triangleIndices.size() + numTriangles);
	m_triangleIndices.insert(m_triangleIndices.end(), vec3i, vec3i + numTriangles);
}

void Mesh::serialize(Stream *stream) {
	stream->writeShort(Message::EMCA_HEADER_SCENE_DATA);
	stream->writeShort(MeshType::TriangleMesh);
	unsigned int msgLen = m_vertexPositions.size();
	stream->writeUInt(msgLen);
	stream->writeFloatArray(reinterpret_cast<float *>(m_vertexPositions.data()), m_vertexPositions.size() * 3);
	msgLen = m_triangleIndices.size();
	stream->writeUInt(msgLen);
	stream->writeIntArray(reinterpret_cast<int *>(m_triangleIndices.data()), m_triangleIndices.size() * 3);
	m_spectrumColor.serialize(stream);
	m_diffuseColor.serialize(stream);
}

EMCA_NAMESPACE_END
