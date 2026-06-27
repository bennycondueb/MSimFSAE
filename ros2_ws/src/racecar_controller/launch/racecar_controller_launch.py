from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='racecar_controller',
            executable='racecar_controller',
            name='racecar_controller',
            output='screen',
            emulate_tty=True,
        )
    ])
