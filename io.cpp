#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <wat_array/wat_array.hpp>
using namespace std;

namespace cpp_watarray {

  template <class A>
  void dump(A *a, const char *filename) {
    ofstream outfile(filename, ios::out);
    outfile.exceptions(ios::failbit | ios::badbit);
    a->Save(outfile);
    outfile.close();
  }
  template void dump(wat_array::WatArray *wa, const char* filename); 
  template void dump(wat_array::BitArray *ba, const char* filename); 

  template <class A>
  void load(A *a, const char *filename) {
    ifstream infile(filename, ios::in);
    infile.exceptions(ios::failbit | ios::badbit);
    a->Load(infile);
    infile.close();
  }
  template void load(wat_array::WatArray *wa, const char *filename);
  template void load(wat_array::BitArray *ba, const char *filename);
  
  template <class A>
  void dumps(A *a, string& str) {
    ostringstream oss;
    oss.exceptions(ios::failbit | ios::badbit);
    a->Save(oss);
    str = oss.str();
  }
  template void dumps(wat_array::WatArray *wa, string& str);
  template void dumps(wat_array::BitArray *ba, string& str);

  template <class A>
  void loads(A *a, string& str) {
    istringstream iss(str, ios::in);
    iss.exceptions(ios::failbit | ios::badbit);
    a->Load(iss);
  }
  template void loads(wat_array::WatArray *wa, string& str);
  template void loads(wat_array::BitArray *ba, string& str);

}
