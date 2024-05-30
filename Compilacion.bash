cd ~/ros2_ws
rosdep install -i --from-path src --rosdistro humble -y
cd src
colcon build --packages-select mi_odometria
source install/setup.bash
