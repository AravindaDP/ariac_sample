from launch import LaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, ExecuteProcess, RegisterEventHandler, TimerAction
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, FindExecutable
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessStart

from launch.actions import (
    DeclareLaunchArgument,
    OpaqueFunction,
)

from ariac_moveit_config.parameters import generate_parameters

def launch_setup(context, *args, **kwargs):
    # Launch arguments
    trial_name = LaunchConfiguration("trial_name")
    
    # Move Group
    moveit = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("ariac_moveit_config"), "/launch", "/ariac_robots_moveit.launch.py"]
        )
    )

    # ARIAC_environment
    ariac_environment = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("ariac_gazebo"), "/launch", "/ariac.launch.py"]
        ),
        launch_arguments={
            'trial_name': trial_name,
            'competitor_pkg': "test_competitor",
            'sensor_config': "sensors"
        }.items()
    )

    # Test Competitor node
    test_competitor = Node(
        package="test_competitor",
        executable="competitor",
        output="screen",
        parameters=generate_parameters(),
    )

    # FlexBE engine
    flexbe_engine = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("flexbe_onboard"), "", "/behavior_onboard.launch.py"]
        )
    )

    # Competitor behavior
    be_launcher = Node(
        package="flexbe_widget",
        executable="be_launcher",
        output="screen"
    )

    start_behavior = ExecuteProcess(
        cmd=[[
            FindExecutable(name='ros2'),
            ' topic pub -1 /flexbe/request_behavior flexbe_msgs/msg/BehaviorRequest "{behavior_name: \'Ariac Behavior\', autonomy_level: 1}"'
        ]],
        shell=True
    )

    delayed_start = RegisterEventHandler(
        OnProcessStart(
            target_action=be_launcher,
            on_start=[
                TimerAction(
                    period=5.0,
                    actions=[start_behavior],
                )
            ]
        )
    )

    nodes_to_start = [
        test_competitor,
        ariac_environment,
        moveit,
        flexbe_engine,
        be_launcher,
        delayed_start
    ]

    return nodes_to_start

def generate_launch_description():
    declared_arguments = []


    declared_arguments.append(
        DeclareLaunchArgument("trial_name", default_value="kitting", description="Name of ariac trial")
    )

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])