// vim: set filetype=cpp:

//TODO(Wesley) Don't do this every tick
namespace ConvertArgs {
template<typename T>
T ls_convert(void* arg) {
  return *static_cast<T*>(arg);
}

template<>
Time ls_convert<Time>(void* arg) {
  return ls_convert<NT>(arg) * s;
}

template<>
Length ls_convert<Length>(void* arg) {
  return ls_convert<NT>(arg) * m;
}

template<>
Velocity ls_convert<Velocity>(void* arg) {
  return ls_convert<NT>(arg) * (m / s);
}

template<>
Acceleration ls_convert<Acceleration>(void* arg) {
  return ls_convert<NT>(arg) * (m / (s * s));
}

template<>
Angle ls_convert<Angle>(void* arg) {
  return ls_convert<NT>(arg) * rad;
}

template<>
AngularVelocity ls_convert<AngularVelocity>(void* arg) {
  return ls_convert<NT>(arg) * (rad / s);
}

template<>
AngularAcceleration ls_convert<AngularAcceleration>(void* arg) {
  return ls_convert<NT>(arg) * (rad / (s * s));
}

template<>
CitrusRobot* ls_convert<CitrusRobot*>(void* arg) {
  return static_cast<CitrusRobot*>(arg);
}
}
