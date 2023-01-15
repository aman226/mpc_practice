#include <gz/transport.hh>
#include <ignition/math/Quaternion.hh>
#include <iostream>

int main(int argc, char **argv)
{
  // check for 7 arguments (model name, x, y, z, roll, pitch, yaw)
  if (argc != 8)
  {
    std::cerr << "Usage: " << argv[0] << " model_name x y z roll pitch yaw" << std::endl;
    return -1;
  }

  gz::Node node;
  gz::Transport transport(node);
  if (!transport.Connect())
  {
    std::cerr << "Failed to connect to gazebo" << std::endl;
    return -1;
  }

  std::string model_name = argv[1];
  double x = atof(argv[2]);
  double y = atof(argv[3]);
  double z = atof(argv[4]);
  double roll = atof(argv[5]);
  double pitch = atof(argv[6]);
  double yaw = atof(argv[7]);

  ignition::msgs::Pose msg;
  msg.mutable_position()->set_x(x);
  msg.mutable_position()->set_y(y);
  msg.mutable_position()->set_z(z);
  ignition::math::Quaterniond orientation(roll, pitch, yaw);
  msg.mutable_orientation()->set_w(orientation.W());
  msg.mutable_orientation()->set_x(orientation.X());
  msg.mutable_orientation()->set_y(orientation.Y());
  msg.mutable_orientation()->set_z(orientation.Z());

  ignition::msgs::Model model_msg;
  model_msg.set_name(model_name);
  model_msg.mutable_pose()->CopyFrom(msg);

  if (!transport.Publish("/gazebo/set_model_state", model_msg)) {
    std::cerr << "Failed to publish model state message" << std::endl;
    return -1;
  }

  std::cout << "Successfully updated pose for model: " << model_name << std::endl;
  return 0;
}