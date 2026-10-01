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
export COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml
```

`COMPOSE_FILE` replaces the repeated `-f` arguments. These shell exports apply
only to that terminal; see the [environment settings](../installation/software/docker.md#container-ros-distribution).

## Terminal 1: Gazebo and RViz

Allow X11 access once per desktop session, before launching the windows:

```sh
xhost +si:localuser:root
SIM_WORLD=curtmini_piper_map docker compose up --build gz-sim moveit-rviz-sim
```

The current containers run as root, so the X11 rule names `root`. GUI Compose
settings already pass `/dev/dri` for GPU access; X11 permission controls access
to the display.

`curtmini_piper_map` is the office world. Use `SIM_WORLD=curtmini_piper` for the
simple ground-plane world. The simulation starts Gazebo, the robot controllers,
and MoveIt; the separate RViz service displays them.

## Terminal 2: Keyboard teleop

After the robot has spawned, using the same terminal setup:

```sh
docker compose run --rm --build keyboard-teleop-sim
```

Keep this terminal focused: `i` drives forward, `,` backward, `j`/`l` turn, and
`k` stops. See the [MoveItPy guide](moveitpy.md) for motion examples. RViz is
already running from terminal 1, so you do not need to start another instance.

## Stop

Press `k` to stop driving, then `Ctrl+C` in the teleop terminal. Press `Ctrl+C`
in terminal 1 to stop Gazebo and RViz. Alternatively, from a configured terminal:

```sh
docker compose stop gz-sim moveit-rviz-sim
```

## Develop with local workspace packages

Follow [local workspace development](../installation/software/docker.md#local-workspace-development)
to build the mounted source repositories and launch with `compose.workspace.yaml`.
Keep that overlay in every launch command that should use the shared installation.
