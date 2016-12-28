#ifndef __bounding_box_
#define __bounding_box_

#include "vertex.h"

namespace base
{
  class bounding_box
  {
  public:
    bounding_box(): min_(base::vertex_max), max_(base::vertex_min) {}
    void add_vertex(const vertex& v);
  private:
    base::vertex min_;
    base::vertex max_;
  };
}

#endif //__bounding_box_
