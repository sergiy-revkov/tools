#ifndef __vertex_h__base_
#define __vertex_h__base_

namespace base
{
  template <typename T>
  class vertex_t
  {
  public:
    vertex_t(): x(0), y(0), z(0) {}
    vertex_t(const T x_, const T y_, const T z_): x(x_), y(y_), z(z_) {}

    T x;
    T y;
    T z;
  };

  using vertex = vertex_t<double>;
}


#endif //__vertex_h__base_
