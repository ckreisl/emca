#ifndef INCLUDE_EMCA_MESHES_H_
#define INCLUDE_EMCA_MESHES_H_

#include "platform.h"
#include "datatypes.h"
#include "stream.h"
#include "mesh.h"

EMCA_NAMESPACE_BEGIN

class Meshes {
public:

	Meshes();
	~Meshes();

	void addMesh(Mesh &mesh) { m_meshes.push_back(mesh); }
	void clear() { m_meshes.clear(); }

	void serialize(Stream *stream);

private:
	std::vector<Mesh> m_meshes;

};

EMCA_NAMESPACE_END

#endif /* INCLUDE_EMCA_MESHES_H_ */
