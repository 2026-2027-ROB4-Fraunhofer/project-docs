# Simulation

Complete the [Docker setup](../installation/software/docker.md) first. This
guide uses regular application images.

## Configure once

Create `curtmini_piper_containers/.env` as described in the
[Docker setup](../installation/software/docker.md#configure-once-with-env).
For this regular-image workflow, edit these values in that file:

```ini
CONTAINER_ROS_DISTRO=jazzy
RMW=cyclonedds
ROS_DOMAIN_ID=42
SIM_WORLD=curtmini_piper_map
SIM_USE_HOKUYO=true
SIM_USE_CAMERAS=true
COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml
```

In **each terminal**, change to the directory containing `.env`:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

Compose reads the file automatically. No `source .env`, repeated exports, or
`-f` options are needed. If you previously exported settings, see
[temporary overrides and precedence](../installation/software/docker.md#temporary-overrides-and-precedence).

## Terminal 1: Gazebo and RViz

Allow X11 access once per desktop session, before launching the windows:

```sh
xhost +si:localuser:root
docker compose up --build gz-sim moveit-rviz-sim
```

The current containers run as root, so the X11 rule names `root`. GUI Compose
settings pass `DISPLAY`, the X11 socket, and `/dev/dri` to the containers. Without
`compose.gui.yaml`, RViz cannot connect to the display and exits with a Qt `xcb`
error. The `.env` configuration above already includes the GUI file.

`curtmini_piper_map` is the office world. Use `SIM_WORLD=curtmini_piper` for the
simple ground-plane world, either in `.env` or before a command. The simulation
starts Gazebo, the robot controllers, and MoveIt; the separate RViz service displays them.
The two simulated cameras are enabled by default. RViz includes their color
and depth views when the simulator image contains the camera implementation;
see [Cameras](cameras.md) for topics and mount transforms.

To load a world from `neo_gz_worlds`, use its name without a path, for example
`SIM_WORLD=neo_workshop` in the same command. Other choices include
`neo_office_empty`, `neo_workshop_2`, and `office_harmonic_02`. The Neo world
files do not load the sensor systems used by the simulator's own worlds, so
lidar, camera, and IMU data may be unavailable in them.

## Starting pose and joint positions

Edit `curtmini_piper_gz_sim/config/initial_state.yaml` to set the starting
`base.x`, `base.y`, and `base.z` in metres, `base.orientation` as a rotation
around Z in radians, and all six `arm.piper_joint*` positions in radians. The
launch checks those joint positions against the Piper limits. The `gz-sim`
service bind-mounts this YAML file, so restart the service after editing it;
an image rebuild is not needed for this setting. Bridge and controller YAML
files come from the upstream simulator in regular images.

For a native ROS workspace launch, point to the source YAML to apply edits
without rebuilding the package. Run this from the simulator repository root:

```sh
ros2 launch curtmini_piper_gz_sim simulation.launch.py \
  initial_state_file:=$(pwd)/config/initial_state.yaml
```

The launch uses its installed copy of `initial_state.yaml` when no path is
provided. Arm, TCP, lidar, and simulated camera mounts are configured
separately in `curtmini_piper_description/config/geometry.yaml`; see
[robot geometry in the simulator image](../installation/software/docker.md#robot-geometry-in-the-simulator-image)
for when to restart or rebuild.

## Controller and MoveIt checks

One spawner activates `joint_state_broadcaster`, `base_controller`, and
`arm_controller` in that order. After startup, check their states from the
infrastructure repository:

```sh
docker compose exec gz-sim /opt/container/ros_entrypoint.sh \
  ros2 control list_controllers
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
