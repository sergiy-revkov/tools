#ifndef __vertex_h__base_
#define __vertex_h__base_
#include <limits>

namespace base
{
  template <typename T>
  class vertex_t
  {
  public:
    vertex_t(): x(0), y(0), z(0) {}
    vertex_t(const T x_, const T y_, const T z_): x(x_), y(y_), z(z_) {}
    vertex_t(const T& c): x(c.x), y(c.y), z(c.z) {}
    T x;
    T y;
    T z;
  };

  using vertex = vertex_t<double>;

  vertex get_vertex_min()
  {
    return vertex(
		  std::numeric_limits<double>::min(),
		  std::numeric_limits<double>::min(),
		  std::numeric_limits<double>::min()
		  );
  }

  vertex get_vertex_max()
  {
    return vertex(
		  std::numeric_limits<double>::max(),
		  std::numeric_limits<double>::max(),
		  std::numeric_limits<double>::max()
		  );
  }

  
}


#endif //__vertex_h__base_
