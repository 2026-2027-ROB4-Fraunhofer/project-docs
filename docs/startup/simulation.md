# Simulation

Complete [Docker installation](../installation/software/docker.md) first.
In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

## Start Gazebo and RViz

Allow X11 access once per desktop session, then start the robot:

```sh
xhost +si:localuser:root
docker compose up --build gz-sim moveit-rviz-sim
```

Gazebo should show the robot and RViz should show its model and MoveIt panel.
The world comes from `.env`; [mapping](mapping.md) explicitly selects the office world.

## Check the controllers

In a second terminal:

```sh
docker compose exec gz-sim /opt/container/ros_entrypoint.sh \
  ros2 control list_controllers
```

`joint_state_broadcaster`, `base_controller`, and `arm_controller` should all be `active`.
If they are not, use [troubleshooting](troubleshooting.md#simulation-controllers).

## Choose a task

- [Teleoperate the base](teleoperation.md).
- [Move the arm with Python](moveitpy.md) or [C++](moveit_cpp.md).
- [Make a map](mapping.md), then [navigate](navigation.md).
- [View cameras](cameras.md) or [find AprilTags](apriltags.md).

## Stop

Stop any active motion task first, then press Ctrl+C in the startup terminal or run:

```sh
docker compose stop gz-sim moveit-rviz-sim
```

See [simulation configuration](../explanation/simulation.md) for worlds, starting poses and controller behavior, or [development workflows](development.md) to run unpublished local code.
