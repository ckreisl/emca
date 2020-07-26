#ifndef INCLUDE_EMCA_SPHERE_H_
#define INCLUDE_EMCA_SPHERE_H_

#include "platform.h"
#include "datatypes.h"
#include "stream.h"

EMCA_NAMESPACE_BEGIN

class Sphere {
public:
    Sphere();
    Sphere(Point3f center, float radius);
    ~Sphere();

    inline void setCenter(Point3f center) { m_center = center;}
    inline void setRadius(float radius) { m_radius = radius; }
    inline void setDiffuse(Color4f diffuse) { m_diffuse = diffuse; }
    inline void setSpecular(Color4f specular) { m_specular = specular; }

    inline Point3f getCenter() const { return m_center; }
    inline float getRadius() const { return m_radius; }

    void serialize(Stream *stream);

private:
    float m_radius;
    Point3f m_center;
    Color4f m_diffuse;
    Color4f m_specular;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_SPHERE_H_ */