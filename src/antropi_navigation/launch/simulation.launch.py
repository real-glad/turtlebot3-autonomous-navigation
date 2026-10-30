from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    turtlebot3_gazebo_launch = PathJoinSubstitution([
        FindPackageShare('turtlebot3_gazebo'),
        'launch',
        'turtlebot3_world.launch.py'
    ])

    return LaunchDescription([

        # Set TurtleBot3 model
        SetEnvironmentVariable(
            name='TURTLEBOT3_MODEL',
            value='burger'
        ),

        # Launch TurtleBot3 Gazebo world
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                turtlebot3_gazebo_launch
            )
        )
    ])


