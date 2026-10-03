import os

from ament_index_python.packages import get_package_prefix
from ament_index_pythong.packages import get_package_share_directory, get_package_share_path
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    ros_gz_sim_pkg_path = get_package_share_directory('ros_gz_sim')
    sim_description_pkg_path = FindPackageShare('simulator_description')
    gz_launch_path = PathJoinSubstitution([ros_gz_sim_pkg_path, 'launch', 'gz_sim.launch.py'])
    urdf_path = get_package_share_path('simulator_description') / 'urdf' / 'racecar_control.xacro'

    return LaunchDescription([
        AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            PathJoinSubstitution([sim_description_pkg_path, 'models'])
        ),
        AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            os.path.join(get_package_prefix('simulator_description'), 'share')
        ),
        # SetEnvironmentVariable(
        #     'GZ_SIM_PLUGIN_PATH',
        #     PathJoinSubstitution([example_pkg_path, 'plugins'])
        # ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_launch_path),
            launch_arguments={
                'gz_args': [
                    PathJoinSubstitution([sim_description_pkg_path,
                                         'worlds/acceleration.sdf']),
                    ' -r'],
                'on_exit_shutdown': 'True'
            }.items(),
        ),

        # Bridging Gazebo topics to ROS 2 -> clock
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',],
            output='screen',
            parameters=[{'use_sim_time': True}],
        ),

        # Node for the process
        # xacro -> urdf -> gazebo
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': ParameterValue(
                    Command(['xacro ', str(urdf_path)]), value_type=str
                )},
                {'use_sim_time': True},
            ],

        ),

        # Node for the process
        # topic -> robot spawning
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'racecar',
                '-topic', '/robot_description',
                '-x', '0.0',
                '-y', '0.0',
                '-z', '0.0',
            ],
            output='screen',
            parameters=[{'use_sim_time': True}],
        ),

        # Debug node just for our easyness
        Node(
            package='path_planning',
            executable='path_planning',
            name='custom_minimal_param_node',
            output='screen',
            emulate_tty=True,
        ),

    ])
