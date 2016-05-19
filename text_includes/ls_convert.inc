// vim: set filetype=cpp:

//TODO(Wesley) Don't do this every tick
namespace ConvertArgs {
int ls_convert_int(std::string arg) {
  return std::stoi(arg);
}
bool ls_convert_bool(std::string arg) {
  return arg == "true" ? true : false;
}
float ls_convert_float(std::string arg) {
  return std::stof(arg)
}
Time ls_convert_time(std::string arg) {
  return std::stof(arg) * s;
}
Distance ls_convert_distance(std::string arg) {
  return std::stof(arg) * m;
}
Angle ls_convert_angle(std::string arg) {
  return std::stof(arg) * rad;
}
Velocity ls_convert_velocity(std::string arg) {
  return std::stof(arg) * (m / s);
}
Acceleration ls_convert_acceleration(std::string arg) {
  return std::stof(arg) * (m / (s * s));
}
AngularVelocity ls_convert_angularvelocity(std::string arg) {
  return std::stof(arg) * (rad / s);
}
Voltage ls_convert_voltage(std::string arg) {
  return std::stof(arg) * V;
}
}
