
#include "sphere.h"
#include "messages.h"

EMCA_NAMESPACE_BEGIN

Sphere::Sphere() {
    m_radius = 1.f;
    m_center = Point3f(0,0,0);
    m_diffuse = Color4f(1,1,1);
    m_specular = Color4f(0,0,0);
}

Sphere::Sphere(Point3f center, float radius)
    : m_center(center), m_radius(radius) { }

Sphere::~Sphere() { }

void Sphere::serialize(Stream *stream) {
    stream->writeShort(Message::EMCA_HEADER_SCENE_DATA);
    stream->writeShort(MeshType::SphereMesh);
    stream->writeFloat(m_radius);
    m_center.serialize(stream);
    m_diffuse.serialize(stream);
    m_specular.serialize(stream);
}

EMCA_NAMESPACE_END