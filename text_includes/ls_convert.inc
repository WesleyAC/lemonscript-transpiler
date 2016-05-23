// vim: set filetype=cpp:

//TODO(Wesley) Don't do this every tick
namespace ConvertArgs {
int ls_convert_int(void *arg) {
  return *((int *)arg);
}
bool ls_convert_bool(void *arg) {
  return *((bool *)arg);
}
float ls_convert_float(void *arg) {
  return *((float *)arg);
}
std::string ls_convert_string(void *arg) {
  return *((std::string *)arg);
}
Time ls_convert_time(void *arg) {
  return ls_convert_float(arg) * s;
}
Distance ls_convert_distance(void *arg) {
  return ls_convert_float(arg) * m;
}
Angle ls_convert_angle(void *arg) {
  return ls_convert_float(arg) * rad;
}
Velocity ls_convert_velocity(void *arg) {
  return ls_convert_float(arg) * (m / s);
}
Acceleration ls_convert_acceleration(void *arg) {
  return ls_convert_float(arg) * (m / (s * s));
}
AngularVelocity ls_convert_angularvelocity(void *arg) {
  return ls_convert_float(arg) * (rad / s);
}
Voltage ls_convert_voltage(void *arg) {
  return ls_convert_float(arg) * V;
}
}
