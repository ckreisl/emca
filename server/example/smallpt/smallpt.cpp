#include <math.h>   // smallpt, a Path Tracer by Kevin Beason, 2008
#include <stdlib.h> // Make : g++ -O3 -fopenmp smallpt.cpp -o smallpt
#include <stdio.h>  //        Remove "-fopenmp" for g++ version < 4.2

#define TINYEXR_IMPLEMENTATION
#include "tinyexr.h" // external lib to save result as EXR file

#include <emca/renderinterface.h>
#include <emca/camera.h>
#include <emca/mesh.h>
#include <emca/sphere.h>
#include <emca/emcaserver.h>
#include <emca/renderinfo.h>
#include <emca/dataapisingleton.h>

struct Vec
{                 // Usage: time ./smallpt 5000 && xv image.ppm
  double x, y, z; // position, also color (r,g,b)
  Vec(double x_ = 0, double y_ = 0, double z_ = 0)
  {
    x = x_;
    y = y_;
    z = z_;
  }
  Vec operator+(const Vec &b) const { return Vec(x + b.x, y + b.y, z + b.z); }
  Vec operator-(const Vec &b) const { return Vec(x - b.x, y - b.y, z - b.z); }
  Vec operator*(double b) const { return Vec(x * b, y * b, z * b); }
  Vec mult(const Vec &b) const { return Vec(x * b.x, y * b.y, z * b.z); }
  Vec &norm() { return *this = *this * (1 / sqrt(x * x + y * y + z * z)); }
  double dot(const Vec &b) const { return x * b.x + y * b.y + z * b.z; } // cross:
  Vec cross(const Vec &a) { return Vec(
    a.y * z - a.z * y,
    a.z * x - a.x * z,
    a.x * y - a.y * x
  ); }
  Vec operator%(Vec &b) { return Vec(y * b.z - z * b.y, z * b.x - x * b.z, x * b.y - y * b.x); }
};

struct Ray
{
  Vec o, d;
  Ray(Vec o_, Vec d_) : o(o_), d(d_) {}
};

enum Refl_t
{
  DIFF,
  SPEC,
  REFR
}; // material types, used in radiance()

struct Sphere
{
  double rad;  // radius
  Vec p, e, c; // position, emission, color
  Refl_t refl; // reflection type (DIFFuse, SPECular, REFRactive)
  Sphere(double rad_, Vec p_, Vec e_, Vec c_, Refl_t refl_) : rad(rad_), p(p_), e(e_), c(c_), refl(refl_) {}
  double intersect(const Ray &r) const
  {                   // returns distance, 0 if nohit
    Vec op = p - r.o; // Solve t^2*d.d + 2*t*(o-p).d + (o-p).(o-p)-R^2 = 0
    double t, eps = 1e-4, b = op.dot(r.d), det = b * b - op.dot(op) + rad * rad;
    if (det < 0)
      return 0;
    else
      det = sqrt(det);
    return (t = b - det) > eps ? t : ((t = b + det) > eps ? t : 0);
  }
};

Sphere spheres[] = {
    //Scene: radius, position, emission, color, material
    Sphere(1e5, Vec(1e5 + 1, 40.8, 81.6), Vec(), Vec(.75, .25, .25), DIFF),   //Left
    Sphere(1e5, Vec(-1e5 + 99, 40.8, 81.6), Vec(), Vec(.25, .25, .75), DIFF), //Rght
    Sphere(1e5, Vec(50, 40.8, 1e5), Vec(), Vec(.75, .75, .75), DIFF),         //Back
    Sphere(1e5, Vec(50, 40.8, -1e5 + 170), Vec(), Vec(), DIFF),               //Frnt
    Sphere(1e5, Vec(50, 1e5, 81.6), Vec(), Vec(.75, .75, .75), DIFF),         //Botm
    Sphere(1e5, Vec(50, -1e5 + 81.6, 81.6), Vec(), Vec(.75, .75, .75), DIFF), //Top
    Sphere(16.5, Vec(27, 16.5, 47), Vec(), Vec(1, 1, 1) * .999, SPEC),        //Mirr
    Sphere(16.5, Vec(73, 16.5, 78), Vec(), Vec(1, 1, 1) * .999, REFR),        //Glas
    Sphere(600, Vec(50, 681.6 - .27, 81.6), Vec(12, 12, 12), Vec(), DIFF)     //Lite
};

inline double clamp(double x) { return x < 0 ? 0 : x > 1 ? 1 : x; }

inline int toInt(double x) { return int(pow(clamp(x), 1 / 2.2) * 255 + .5); }

inline bool intersect(const Ray &r, double &t, int &id)
{
  double n = sizeof(spheres) / sizeof(Sphere), d, inf = t = 1e20;
  for (int i = int(n); i--;)
    if ((d = spheres[i].intersect(r)) && d < t)
    {
      t = d;
      id = i;
    }
  return t < inf;
}

Vec radiance(const Ray &r, int depth, unsigned short *Xi)
{
  emca::DataApiSingleton::getInstance()->setDepthIdx(depth);
  double t;   // distance to intersection
  int id = 0; // id of intersected object
  if (!intersect(r, t, id))
    return Vec();                  // if miss, return black
  const Sphere &obj = spheres[id]; // the hit object
  Vec x = r.o + r.d * t, n = (x - obj.p).norm(), nl = n.dot(r.d) < 0 ? n : n * -1, f = obj.c;
  emca::DataApiSingleton::getInstance()->setIntersectionPos(x.x, x.y, x.z);
  double p = f.x > f.y && f.x > f.z ? f.x : f.y > f.z ? f.y : f.z; // max refl
  if (++depth > 5)
  {
    if (erand48(Xi) < p)
    {
      f = f * (1 / p);
    }
    else
    {
      return obj.e; //R.R.
    }
  }
  if (obj.refl == DIFF)
  { // Ideal DIFFUSE reflection
    double r1 = 2 * M_PI * erand48(Xi), r2 = erand48(Xi), r2s = sqrt(r2);
    Vec w = nl, u = ((fabs(w.x) > .1 ? Vec(0, 1) : Vec(1)) % w).norm(), v = w % u;
    Vec d = (u * cos(r1) * r2s + v * sin(r1) * r2s + w * sqrt(1 - r2)).norm();
    return obj.e + f.mult(radiance(Ray(x, d), depth, Xi));
  }
  else if (obj.refl == SPEC) // Ideal SPECULAR reflection
    return obj.e + f.mult(radiance(Ray(x, r.d - n * 2 * n.dot(r.d)), depth, Xi));
  Ray reflRay(x, r.d - n * 2 * n.dot(r.d)); // Ideal dielectric REFRACTION
  bool into = n.dot(nl) > 0;                // Ray from outside going in?
  double nc = 1, nt = 1.5, nnt = into ? nc / nt : nt / nc, ddn = r.d.dot(nl), cos2t;
  if ((cos2t = 1 - nnt * nnt * (1 - ddn * ddn)) < 0) // Total internal reflection
    return obj.e + f.mult(radiance(reflRay, depth, Xi));
  Vec tdir = (r.d * nnt - n * ((into ? 1 : -1) * (ddn * nnt + sqrt(cos2t)))).norm();
  double a = nt - nc, b = nt + nc, R0 = a * a / (b * b), c = 1 - (into ? -ddn : tdir.dot(n));
  double Re = R0 + (1 - R0) * c * c * c * c * c, Tr = 1 - Re, P = .25 + .5 * Re, RP = Re / P, TP = Tr / (1 - P);
  return obj.e + f.mult(depth > 2 ? (erand48(Xi) < P ? // Russian roulette
                                         radiance(reflRay, depth, Xi) * RP
                                                     : radiance(Ray(x, tdir), depth, Xi) * TP)
                                  : radiance(reflRay, depth, Xi) * Re + radiance(Ray(x, tdir), depth, Xi) * Tr);
}

bool saveToEXR(const char *filename, const Vec *vecImageRGB, int &width, int &height)
{
  EXRHeader header;
  InitEXRHeader(&header);

  EXRImage image;
  InitEXRImage(&image);

  image.num_channels = 3;

  std::vector<float> images[3];
  images[0].resize(width * height);
  images[1].resize(width * height);
  images[2].resize(width * height);

  for (int i = 0; i < width * height; i++)
  {
    images[0][i] = vecImageRGB[i].x;
    images[1][i] = vecImageRGB[i].y;
    images[2][i] = vecImageRGB[i].z;
  }

  float *image_ptr[3];
  image_ptr[0] = &(images[2].at(0)); // B
  image_ptr[1] = &(images[1].at(0)); // G
  image_ptr[2] = &(images[0].at(0)); // R

  image.images = (unsigned char **)image_ptr;
  image.width = width;
  image.height = height;

  header.num_channels = 3;
  header.channels = (EXRChannelInfo *)malloc(sizeof(EXRChannelInfo) * header.num_channels);
  // Must be BGR(A) order, since most of EXR viewers expect this channel order.
  strncpy(header.channels[0].name, "B", 255);
  header.channels[0].name[strlen("B")] = '\0';
  strncpy(header.channels[1].name, "G", 255);
  header.channels[1].name[strlen("G")] = '\0';
  strncpy(header.channels[2].name, "R", 255);
  header.channels[2].name[strlen("R")] = '\0';

  header.pixel_types = (int *)malloc(sizeof(int) * header.num_channels);
  header.requested_pixel_types = (int *)malloc(sizeof(int) * header.num_channels);
  for (int i = 0; i < header.num_channels; i++)
  {
    header.pixel_types[i] = TINYEXR_PIXELTYPE_FLOAT;          // pixel type of input image
    header.requested_pixel_types[i] = TINYEXR_PIXELTYPE_HALF; // pixel type of output image to be stored in .EXR
  }

  const char *err;
  int ret = SaveEXRImageToFile(&image, &header, filename, &err);
  if (ret != TINYEXR_SUCCESS)
  {
    fprintf(stderr, "Save EXR err: %s\n", err);
    return false;
  }

  free(header.channels);
  free(header.pixel_types);
  free(header.requested_pixel_types);

  return true;
}

class SmallPt : public emca::RenderInterface
{
public:
  void renderImage()
  {
    std::cout << "Start rendering image ..." << std::endl;
    Ray cam(Vec(50, 52, 295.6), Vec(0, -0.042612, -1).norm()); // cam pos, dir
    Vec cx = Vec(w * .5135 / h), cy = (cx % cam.d).norm() * .5135, r, *c = new Vec[w * h];
#pragma omp parallel for schedule(dynamic, 1) private(r) // OpenMP
    for (int y = 0; y < h; y++)
    { // Loop over image rows
      fprintf(stderr, "\rRendering (%d spp) %5.2f%%", samps * 4, 100. * y / (h - 1));
      for (unsigned short x = 0, Xi[3] = {0, 0, y * y * y}; x < w; x++) // Loop cols
        for (int sy = 0, i = (h - y - 1) * w + x; sy < 2; sy++)         // 2x2 subpixel rows
          for (int sx = 0; sx < 2; sx++, r = Vec())
          { // 2x2 subpixel cols
            for (int s = 0; s < samps; s++)
            {              
              double r1 = 2 * erand48(Xi), dx = r1 < 1 ? sqrt(r1) - 1 : 1 - sqrt(2 - r1);
              double r2 = 2 * erand48(Xi), dy = r2 < 1 ? sqrt(r2) - 1 : 1 - sqrt(2 - r2);
              Vec d = cx * (((sx + .5 + dx) / 2 + x) / w - .5) +
                      cy * (((sy + .5 + dy) / 2 + y) / h - .5) + cam.d;
              r = r + radiance(Ray(cam.o + d * 140, d.norm()), 0, Xi) * (1. / samps);
            } // Camera rays are pushed ^^^^^ forward to start in interior
            c[i] = c[i] + Vec(clamp(r.x), clamp(r.y), clamp(r.z)) * .25;
          }
    }
    // Save smallpt result as EXR file.
    if (saveToEXR(filename, c, w, h))
    {
      printf("\n");
      printf("Successfully saved exr file smallpt with: %d spp", samps);
    }
  }

  void renderPixel(unsigned int x, unsigned int y, int sampleCount)
  {
    std::cout << "Start rendering pixel (" << x << ", " << y << ")" << std::endl;
    Ray cam(Vec(50, 52, 295.6), Vec(0, -0.042612, -1).norm()); // cam pos, dir    
    Vec cx = Vec(w * .5135 / h), cy = (cx % cam.d).norm() * .5135, r, *c = new Vec[w * h];
    unsigned short Xi[3] = {0, 0, y * y * y};
    for (int sy = 0, i = (h - y - 1) * w + x; sy < 2; sy++) { // 2x2 subpixel rows
      for (int sx = 0; sx < 2; sx++, r = Vec())
      { // 2x2 subpixel cols
        for (int s = 0; s < samps; s++)
        {
          emca::DataApiSingleton::getInstance()->setSampleIdx(s);
          emca::DataApiSingleton::getInstance()->setPathOrigin(cam.o.x, cam.o.y, cam.o.z);
          double r1 = 2 * erand48(Xi), dx = r1 < 1 ? sqrt(r1) - 1 : 1 - sqrt(2 - r1);
          double r2 = 2 * erand48(Xi), dy = r2 < 1 ? sqrt(r2) - 1 : 1 - sqrt(2 - r2);
          Vec d = cx * (((sx + .5 + dx) / 2 + x) / w - .5) +
                  cy * (((sy + .5 + dy) / 2 + y) / h - .5) + cam.d;
          r = r + radiance(Ray(cam.o + d * 140, d.norm()), 0, Xi) * (1. / samps);
        } // Camera rays are pushed ^^^^^ forward to start in interior
        c[i] = c[i] + Vec(clamp(r.x), clamp(r.y), clamp(r.z)) * .25;
        emca::DataApiSingleton::getInstance()->setFinalEstimate(c[i].x, c[i].y, c[i].z);
      }      
    }    
  }

  void sendRenderInformation(emca::Stream *stream)
  {
    std::cout << "Send render information ..." << std::endl;
    emca::RenderInfo renderInfo = emca::RenderInfo();
    renderInfo.setSampleCount(samps*4);
    renderInfo.setSceneName("Smallpt");
    renderInfo.setOutputFileExtension(".exr");
    renderInfo.setOutputFilepath("/home/ckreisl/Code/mitsuba/emca/server/build/smallpt.exr");
    renderInfo.serialize(stream);
  }

  void sendCameraData(emca::Stream *stream)
  {
    std::cout << "Send camera information ..." << std::endl;
    Ray cam(Vec(50, 52, 295.6), Vec(0, -0.042612, -1).norm()); // cam pos, dir
    Vec up = cam.o.cross(cam.d).norm();
    emca::Camera camera = emca::Camera();
    camera.setOrigin(emca::Point3f(cam.o.x, cam.o.y, cam.o.z));
    camera.setDirectionVector(emca::Vec3f(cam.d.x, cam.d.y, cam.d.z));
    camera.setUpVector(emca::Vec3f(up.x, up.y, up.z));
    camera.serialize(stream);
  }

  void sendMeshData(emca::Stream *stream)
  {
    std::cout << "Send mesh information ..." << std::endl;
    for(auto &sphere : spheres) {
      emca::Sphere emcaSphere = emca::Sphere(
          emca::Point3f(sphere.p.x, sphere.p.y, sphere.p.z),
          sphere.rad);
      emcaSphere.setDiffuse(emca::Color4f(sphere.c.x, sphere.c.y, sphere.c.z));
      emcaSphere.serialize(stream);
    }
  }

  void updateSampleCount(int sampleCount)
  {
    std::cout << "Update sample value from " << samps << " to " << sampleCount << std::endl;
    std::cout << "Samps is multiplied by 4: " << sampleCount * 4 << std::endl;
    samps = sampleCount;
  }

private:
  const char *filename = "smallpt.exr";
  int w = 1024;
  int h = 768;
  int samps = 1;
};

int main(int argc, char *argv[])
{
  int samps = argc == 2 ? atoi(argv[1]) / 4 : 1; // # samples

  SmallPt *renderer = new SmallPt();
  renderer->updateSampleCount(samps);
  emca::EMCAServer *emcaServer = new emca::EMCAServer();
  emcaServer->setRenderer(renderer);
  emcaServer->start();

  delete emcaServer;
  return 0;
}