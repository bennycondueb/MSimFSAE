from ament_index_python.packages import get_package_share_directory, get_package_share_path
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    ros_gz_sim_pkg_path = get_package_share_directory('ros_gz_sim')
    sim_description_pkg_path = FindPackageShare('simulator_description')
    gz_launch_path = PathJoinSubstitution([ros_gz_sim_pkg_path, 'launch', 'gz_sim.launch.py'])
    path_to_urdf = get_package_share_path('simulator_description') / 'urdf' / 'racecar.xacro'

    return LaunchDescription([
        # SetEnvironmentVariable(
        #     'GZ_SIM_RESOURCE_PATH',
        #     PathJoinSubstitution([example_pkg_path, 'models'])
        # ),
        # SetEnvironmentVariable(
        #     'GZ_SIM_PLUGIN_PATH',
        #     PathJoinSubstitution([example_pkg_path, 'plugins'])
        # ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_launch_path),
            launch_arguments={
                'gz_args': PathJoinSubstitution([sim_description_pkg_path,
                                                'worlds/empty_asphalt.sdf']),
                'on_exit_shutdown': 'True'
            }.items(),
        ),

        # Bridging and remapping Gazebo topics to ROS 2 (replace with your own topics)
        # Node(
        #     package='ros_gz_bridge',
        #     executable='parameter_bridge',
        #     arguments=['/example_imu_topic@sensor_msgs/msg/Imu@gz.msgs.IMU',],
        #     remappings=[('/example_imu_topic',
        #                  '/remapped_imu_topic'),],
        #     output='screen'
        # ),

        # Node for the process
        # xacro -> urdf -> gazebo
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': ParameterValue(
                    Command(['xacro ', str(path_to_urdf)]), value_type=str
                )
            }]
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
            output='screen'
        ),

        # Debug node just for our easyness
        Node(
            package='path_planning',
            executable='path_planning',
            name='custom_minimal_param_node',
            output='screen',
            emulate_tty=True,
        )

    ])
