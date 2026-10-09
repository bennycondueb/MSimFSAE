from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='path_planning',
            executable='path_planning',
            name='custom_minimal_param_node',
            output='screen',
            emulate_tty=True,
        )
    ])
