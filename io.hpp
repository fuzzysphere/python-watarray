#ifndef _WATARRAY_IO_H
#define _WATARRAY_IO_H 

#include <string>
#include <wat_array/wat_array.hpp>
using namespace std;

namespace cpp_watarray {
  template <class A> void dump(A *a, const char *filename);
  template <class A> void load(A *a, const char *filename);
  template <class A> void dumps(A *a, string& str);
  template <class A> void loads(A *a, string& str);
}

#endif
