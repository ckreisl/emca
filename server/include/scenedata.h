#ifndef INCLUDE_EMCA_EMCADATA_H_
#define INCLUDE_EMCA_EMCADATA_H_

#include "platform.h"
#include "datatypes.h"
#include "stream.h"
#include "messages.h"

EMCA_NAMESPACE_BEGIN

struct Camera
{
    float nearClip;
    float farClip;
    float focusDist;
    float fov;
    Vec3f up;
    Vec3f dir;
    Point3f origin;

    Camera() {}
    Camera(float _nearClip, float _farClip, float _focusDist, float _fov,
           Vec3f _up, Vec3f _dir, Point3f _origin)
        : nearClip(_nearClip), farClip(_farClip), focusDist(_focusDist),
          fov(_fov), up(_up), dir(_dir), origin(_origin) {}

    void serialize(Stream *stream)
    {
        stream->writeShort(Message::EMCA_HEADER_CAMERA);
        stream->writeFloat(nearClip);
        stream->writeFloat(farClip);
        stream->writeFloat(focusDist);
        stream->writeFloat(fov);
        up.serialize(stream);
        dir.serialize(stream);
        origin.serialize(stream);
    }
};

struct Mesh
{
    std::vector<Point3f> vertexPositions;
    std::vector<Vec3i> triangleIndices;
    Color4f specularColor;
    Color4f diffuseColor;

    Mesh() {}

    void addVertices(Point3f *p3f, size_t numPoints)
    {
        vertexPositions.reserve(vertexPositions.size() + numPoints);
        vertexPositions.insert(vertexPositions.end(), p3f, p3f + numPoints);
    }

    void addTriangles(Vec3i *vec3i, size_t numTriangles)
    {
        triangleIndices.reserve(triangleIndices.size() + numTriangles);
        triangleIndices.insert(triangleIndices.end(), vec3i, vec3i + numTriangles);
    }

    void addVertexPosition(Point3f &p3f) { vertexPositions.push_back(p3f); }
    void addTriangleIndices(Vec3i &vec3i) { triangleIndices.push_back(vec3i); }
    void clearVertexPositions() { vertexPositions.clear(); }
    void clearTriangleIndices() { triangleIndices.clear(); }
    size_t getVertexCount() { return vertexPositions.size(); }
    size_t getTriangleCount() { return triangleIndices.size(); }

    void serialize(Stream *stream)
    {
        stream->writeShort(Message::EMCA_HEADER_SCENE_DATA);
        stream->writeShort(MeshType::TriangleMesh);
        unsigned int msgLen = vertexPositions.size();
        stream->writeUInt(msgLen);
        stream->writeFloatArray(reinterpret_cast<float *>(vertexPositions.data()), vertexPositions.size() * 3);
        msgLen = triangleIndices.size();
        stream->writeUInt(msgLen);
        stream->writeIntArray(reinterpret_cast<int *>(triangleIndices.data()), triangleIndices.size() * 3);
        specularColor.serialize(stream);
        diffuseColor.serialize(stream);
    }
};

struct Meshes
{
    std::vector<Mesh> meshes;

    Meshes() { meshes = std::vector<Mesh>(); }

    void addMesh(Mesh &mesh) { meshes.push_back(mesh); }
    void clear() { meshes.clear(); }

    void serialize(Stream *stream)
    {
        stream->writeShort(Message::EMCA_HEADER_SCENE_DATA);
        unsigned int msgLen = meshes.size();
        stream->writeUInt(msgLen);
        for (unsigned int i = 0; i < msgLen; ++i)
            meshes[i].serialize(stream);
    }
};

struct Sphere
{
    float radius;
    Point3f center;
    Color4f diffuse;
    Color4f specular;

    Sphere() {}
    Sphere(Point3f _center, float _radius) : center(_center), radius(_radius) {}

    void serialize(Stream *stream) 
    {
        stream->writeShort(Message::EMCA_HEADER_SCENE_DATA);
        stream->writeShort(MeshType::SphereMesh);
        stream->writeFloat(radius);
        center.serialize(stream);
        diffuse.serialize(stream);
        specular.serialize(stream);
    }
};

struct RenderInfo 
{
    std::string sceneName;
    std::string outputFilepath;
    std::string outputFileExtension;
    int sampleCount;

    RenderInfo() { }
    RenderInfo(std::string _sceneName, std::string _pathToOutputFile,
               std::string _extension, int _sampleCount) 
               : sceneName(_sceneName), outputFilepath(_pathToOutputFile),
               outputFileExtension(_extension), sampleCount(_sampleCount) {}

    void serialize(Stream *stream)
    {
        stream->writeShort(Message::EMCA_HEADER_RENDER_INFO);
        stream->writeString(sceneName);
        stream->writeString(outputFilepath);
        stream->writeString(outputFileExtension);
        stream->writeInt(sampleCount);
    }

    void deserialize(Stream *stream)
    {
        sampleCount = stream->readInt();
    }
};

EMCA_NAMESPACE_END

#endif // INCLUDE_EMCA_EMCADATA_H_