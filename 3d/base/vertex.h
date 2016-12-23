#ifndef __vertex_h__base_
#define __vertex_h__base_

namespace base
{
  template <typename T>
  class vertex_t
  {
  public:
    T x;
    T y;
    T z;
  };

  using vertex = vertex_t<double>;
}


#endif //__vertex_h__base_
