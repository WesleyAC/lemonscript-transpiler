#ifndef BASE_CLASS_H_
#define BASE_CLASS_H_

class BaseAutoFunction {
  public:
    bool Init(CitrusRobot *robot, std::vector<void *>);
    bool Periodic(CitrusRobot *robot, std::vector<void *>);
  private:
    //none
};

#endif
