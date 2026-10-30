from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    nav2_launch = PathJoinSubstitution([
        FindPackageShare('turtlebot3_navigation2'),
        'launch',
        'navigation2.launch.py'
    ])

    package_share = FindPackageShare('antropi_navigation')

    map_file = PathJoinSubstitution([
        package_share,
        'maps',
        'turtlebot3_world.yaml'
    ])

    params_file = PathJoinSubstitution([
        package_share,
        'config',
        'nav2_params.yaml'
    ])

    return LaunchDescription([

        SetEnvironmentVariable(
            name='TURTLEBOT3_MODEL',
            value='burger'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav2_launch),
            launch_arguments={
                'map': map_file,
                'params_file': params_file,
                'use_sim_time': 'True',
                'autostart': 'True'
            }.items()
        )
    ])

