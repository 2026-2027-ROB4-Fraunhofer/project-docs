# Simulation startup

Complete [Docker installation](../../installation/software/docker.md) first.
Select [Gazebo graphics](../../installation/software/docker.md#select-gazebo-graphics) once in `.env`; the startup commands below work with either selection.
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
The world comes from `.env`; [mapping](navigation/mapping.md) explicitly selects the office world.

Optionally check the renderer in a second terminal; with NVIDIA selected, it should name your NVIDIA GPU:

```sh
docker compose exec gz-sim sh -c \
  'grep -E "GL_VENDOR|GL_RENDERER" /root/.gz/rendering/ogre2.log'
```

## Check the controllers

In a second terminal:

```sh
docker compose exec gz-sim /opt/container/ros_entrypoint.sh \
  ros2 control list_controllers
```

`joint_state_broadcaster`, `base_controller`, and `arm_controller` should all be `active`.
If they are not, use [troubleshooting](../troubleshooting.md#simulation-controllers).

## Choose a task

- [Teleoperate the base](navigation/teleoperation.md).
- [MoveIt in RViz: first arm motion](manipulation/moveit_gui.md).
- [Move the arm with Python](manipulation/moveitpy.md) or [C++](manipulation/moveit_cpp.md).
- [Make a map](navigation/mapping.md), then [navigate](navigation/navigation.md).
- [View cameras](perception/cameras.md) or [find AprilTags](perception/apriltags.md).

## Stop

Stop any active motion task first, then press Ctrl+C in the startup terminal or run:

```sh
docker compose stop gz-sim moveit-rviz-sim
```

See [simulation configuration](../../explanation/simulation.md) for worlds, starting poses and controller behavior, or [development workflows](../development.md) to run unpublished local code.
