#ifndef INCLUDE_EMCA_CAMERA_H_
#define INCLUDE_EMCA_CAMERA_H_

#include "platform.h"
#include "datatypes.h"
#include "stream.h"

EMCA_NAMESPACE_BEGIN

class Camera {
public:

	Camera();
	Camera(float nearClip, float farClip, float focusDist, float fov,
			Vec3f up, Vec3f dir, Point3f origin);
	~Camera();

	void setNearClip(float nearClip) { m_nearClip = nearClip; }
	void setFarClip(float farClip) { m_farClip = farClip; }
	void setFocusDist(float focusDist) { m_focusDist = focusDist; }
	void setFov(float fov) { m_fov = fov; }
	void setUpVector(Vec3f up) { m_up = up; }
	void setDirectionVector(Vec3f dir) { m_dir = dir; }
	void setOrigin(Point3f origin) { m_origin = origin; }

	void serialize(Stream *stream);

private:
	float m_nearClip;
	float m_farClip;
	float m_focusDist;
	float m_fov;
	Vec3f m_up;
	Vec3f m_dir;
	Point3f m_origin;
};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_CAMERA_H_ */
