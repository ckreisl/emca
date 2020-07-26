

#include "camera.h"
#include "messages.h"

EMCA_NAMESPACE_BEGIN

Camera::Camera() {
	m_nearClip = 0.0;
	m_farClip = 100.0;
	m_focusDist = 7.0;
	m_fov = 39.0;
	m_up = Vec3f(0, 0, 1);
	m_dir = Vec3f(0, 1, 0);
	m_origin = Point3f(0, 0, 0);
}

Camera::Camera(float nearClip, float farClip, float focusDist, float fov,
		Vec3f up, Vec3f dir, Point3f origin) {
	m_nearClip = nearClip;
	m_farClip = farClip;
	m_focusDist = focusDist;
	m_fov = fov;
	m_up = up;
	m_dir = dir;
	m_origin = origin;
}

Camera::~Camera() {

}

void Camera::serialize(Stream *stream) {
	stream->writeShort(Message::EMCA_HEADER_CAMERA);
	stream->writeFloat(m_nearClip);
	stream->writeFloat(m_farClip);
	stream->writeFloat(m_focusDist);
	stream->writeFloat(m_fov);
	m_up.serialize(stream);
	m_dir.serialize(stream);
	m_origin.serialize(stream);
}


EMCA_NAMESPACE_END


