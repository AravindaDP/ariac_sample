cmake_minimum_required(VERSION 3.8)
project(ariac_competitor)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(ariac_msgs REQUIRED)
find_package(orocos_kdl REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(test_competitor REQUIRED)

# Install Python modules
# ament_python_install_package(${PROJECT_NAME} SCRIPTS_DESTINATION lib/${PROJECT_NAME})

# Install Python executables
# install(PROGRAMS
#   scripts/tutorial_1.py
#   scripts/tutorial_2.py
#   scripts/tutorial_3.py
#   scripts/tutorial_4.py
#   scripts/tutorial_5.py
#   scripts/tutorial_6.py
#   scripts/tutorial_7.py
#   DESTINATION lib/${PROJECT_NAME}
# )


# Install the config directory to the package share directory
install(DIRECTORY 
  config
  launch
  DESTINATION share/${PROJECT_NAME}
)

# Install C++ executables
# add_executable(competitor_node 
#  src/competitor_node.cpp)

# ament_target_dependencies(competitor_node 
#   rclcpp
#   moveit_ros_planning_interface 
#   ariac_msgs
#   test_competitor)

# install(TARGETS
#   competitor_node
#   DESTINATION lib/${PROJECT_NAME})


ament_package()
