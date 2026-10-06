# Simulation

Complete the [Docker setup](../installation/software/docker.md) first. This
workflow builds application images; it does not require a native ROS workspace
build or the workspace overlay.

## Terminal setup

Run this in **each terminal** used below:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
export CONTAINER_ROS_DISTRO=jazzy
export RMW=cyclonedds
export ROS_DOMAIN_ID=42
```

These shell exports apply only to that terminal; see the [environment
settings](../installation/software/docker.md#container-ros-distribution).

## Terminal 1: Gazebo and RViz

Allow X11 access once per desktop session, before launching the windows:

```sh
xhost +si:localuser:root
SIM_WORLD=curtmini_piper_map docker compose \
  -f compose.yaml -f compose.cyclonedds.yaml -f compose.gui.yaml \
  up --build gz-sim moveit-rviz-sim
```

The current containers run as root, so the X11 rule names `root`. GUI Compose
settings pass `DISPLAY`, the X11 socket, and `/dev/dri` to the containers. Without
`compose.gui.yaml`, RViz cannot connect to the display and exits with a Qt `xcb`
error. The shorter `docker compose up --build gz-sim moveit-rviz-sim` command
works only when `COMPOSE_FILE` includes `compose.gui.yaml`.

`curtmini_piper_map` is the office world. Use `SIM_WORLD=curtmini_piper` for the
simple ground-plane world. The simulation starts Gazebo, the robot controllers,
and MoveIt; the separate RViz service displays them.

To load a world from `neo_gz_worlds`, use its name without a path, for example
`SIM_WORLD=neo_workshop` in the same command. Other choices include
`neo_office_empty`, `neo_workshop_2`, and `office_harmonic_02`. The Neo world
files do not load the sensor systems used by the simulator's own worlds, so
lidar and IMU data may be unavailable in them.

## Starting pose and joint positions

Edit `curtmini_piper_gz_sim/config/initial_state.yaml` to set the starting
`base.x`, `base.y`, and `base.z` in metres, `base.orientation` as a rotation
around Z in radians, and all six `arm.piper_joint*` positions in radians. The
launch checks those joint positions against the Piper limits. The `gz-sim`
service bind-mounts the source `config` directory, so restart the service after
editing the YAML; an image rebuild is not needed for this setting.

For a native ROS workspace launch, point to the source YAML to apply edits
without rebuilding the package. Run this from the simulator repository root:

```sh
ros2 launch curtmini_piper_gz_sim simulation.launch.py \
  initial_state_file:=$(pwd)/config/initial_state.yaml
```

The launch uses its installed copy of `initial_state.yaml` when no path is
provided. Arm, TCP, and lidar mounts are configured separately in
`curtmini_piper_description/config/geometry.yaml`; see the
[Docker source caveat](../installation/software/docker.md#robot-geometry-in-the-simulator-image)
before changing them in the standard simulator image.

## Controller and MoveIt checks

One spawner activates `joint_state_broadcaster`, `base_controller`, and
`arm_controller` in that order. After startup, check their states from the
infrastructure repository:

```sh
docker compose -f compose.yaml -f compose.cyclonedds.yaml -f compose.gui.yaml \
  exec gz-sim ros2 control list_controllers
```

All three should be `active`. If the broadcaster is loaded but `inactive`,
`/joint_states` will be missing; inspect the spawner output before planning or
executing a motion. The simulator's `config/moveit_controllers.yaml` sets
`trajectory_execution.allowed_start_tolerance` to `0.0`, which disables
MoveIt's trajectory start-position check. MoveIt still needs current joint
states from the broadcaster.

## Terminal 2: Keyboard teleop

After the robot has spawned, using the same terminal setup:

```sh
docker compose -f compose.yaml -f compose.cyclonedds.yaml \
  run --rm --build keyboard-teleop-sim
```

Keep this terminal focused: `i` drives forward, `,` backward, `j`/`l` turn, and
`k` stops. See the [MoveItPy guide](moveitpy.md) for motion examples. RViz is
already running from terminal 1, so you do not need to start another instance.

## Stop

Press `k` to stop driving, then `Ctrl+C` in the teleop terminal. Press `Ctrl+C`
in terminal 1 to stop Gazebo and RViz. Alternatively, from a configured terminal:

```sh
docker compose -f compose.yaml -f compose.cyclonedds.yaml -f compose.gui.yaml \
  stop gz-sim moveit-rviz-sim
```

## Develop with local workspace packages

Follow [local workspace development](../installation/software/docker.md#local-workspace-development)
to build the mounted source repositories and launch with `compose.workspace.yaml`.
Keep that overlay in every launch command that should use the shared installation.
