#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_description = get_package_share_directory('so_arm100_teleop_description')
    pkg_gazebo = get_package_share_directory('so_arm100_teleop_gazebo')
    pkg_bringup = get_package_share_directory('so_arm100_teleop_bringup')
    bridge_config_path = os.path.join(pkg_bringup, 'config', 'so_arm100_bridge.yaml')
    pkg_ros_gz = get_package_share_directory('ros_gz_sim')

    # 1. URDF 
    urdf_path = os.path.join(pkg_description, 'models', 'so_arm100', 'so100.urdf')
    with open(urdf_path, 'r') as f:
        robot_description = f.read()

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': True, 'robot_description': robot_description}],
    )

    # 2. Gazebo World
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_ros_gz, 'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': [
                PathJoinSubstitution([pkg_gazebo, 'worlds', 'workspace.sdf']),
                ' -r',
            ]
        }.items(),
    )

    # 3. Spawn Robot
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'so_arm100', '-topic', 'robot_description', '-x', '-0.25', '-z', '1.0'],
        output='screen',
    )

    # 4. The Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': bridge_config_path,
        }],
        output='screen'
    )

    # 5. Rviz2
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(pkg_bringup, 'config', 'so_arm100.rviz')],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    # 6. Web Video Server
    web_video_server = Node(
        package='web_video_server',
        executable='web_video_server',
        name='web_video_server',
        parameters=[{
            'port': 8080,
            'address': '0.0.0.0',
        }],
        output='screen'
    )

    # 7. Record Data (Optional)
    record_arg = DeclareLaunchArgument(
        'record', default_value='false',
        description='Set to true to enable data recording'
    )

    record_data_node = Node(
        package='so_arm100_teleop_application',
        executable='record_data',
        name='record_data',
        condition=IfCondition(LaunchConfiguration('record')),
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        bridge, 
        rviz2,
        web_video_server,
        record_arg,
        record_data_node,
    ])