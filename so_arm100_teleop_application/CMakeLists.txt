cmake_minimum_required(VERSION 3.5)

project(so_arm100_teleop_application)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  src/webxr_ros_bridge.py
  DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS
  src/gazebo_teleop_bridge.py
  DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/run_wireless.sh
  DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS
  web/https_server.py
  DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS
  web/webxr_streamer.html
  DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS
  src/record_data.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME record_data
)

ament_package()
