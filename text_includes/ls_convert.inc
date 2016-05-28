// vim: set filetype=cpp:

//TODO(Wesley) Don't do this every tick
namespace ConvertArgs {

// These operators are in structs because C++ doesn't support
// partial function overloading, which is needed to specialize
// on Units<U1, U2, U3, U4>
template<typename T>
struct Convert {
  T operator()(void* arg) {
    return *static_cast<T*>(arg);
  }
};

template<int U1, int U2, int U3, int U4>
struct Convert<Units<U1, U2, U3, U4>> {
  Units<U1, U2, U3, U4> operator()(void *arg) {
    return Convert<NT>()(arg) * Units<U1, U2, U3, U4>(1);
  }
};

template<typename T>
struct Convert<T*>{
  T* operator()(void* arg) {
    return static_cast<T*>(arg);
  }
};
}
