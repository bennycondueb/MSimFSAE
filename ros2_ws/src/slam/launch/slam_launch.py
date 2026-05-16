from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='slam',
            executable='slam',
            name='slam_node',
            output='screen',
            emulate_tty=True,
        )
    ])