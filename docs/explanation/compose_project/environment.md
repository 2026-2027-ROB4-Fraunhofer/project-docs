# Environment settings

The project settings are stored in `curtmini_piper_containers/.env`.

Docker Compose reads it automatically whenever you run a command from this directory. You do not
need to run `source .env` or repeat shell exports in every terminal.
`.env.example` is a template; copy it to `.env` to use its settings.

See official docker documentation on [variable interpolation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/).

In this project, the environment variables are:

```sh
# .env.example

## ROS settings
CONTAINER_ROS_DISTRO=jazzy
RMW=cyclonedds
ROS_DOMAIN_ID=42

## Robot settings
ARM_MODEL=piper_x

# Navigation settings
NAV2_MAP=map.yaml

## Simulation settings
# Use curtmini_piper_map for the office environment.
SIM_WORLD=curtmini_piper
SIM_USE_HOKUYO=true
SIM_USE_CAMERAS=true
SIM_USE_APRILTAGS=false

# Compose overlays
COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml
```

| Variable | What it does | Values |
| --- | --- | --- |
| `CONTAINER_ROS_DISTRO` | Selects the container [ROS 2 distribution](https://docs.ros.org/en/jazzy/Releases/Release-Jazzy-Jalisco.html). | `jazzy` (the only supported value) |
| `RMW` | Selects the [ROS middleware](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Different-Middleware-Vendors.html). | `cyclonedds` or `zenoh` (CycloneDDS is the documented default; Zenoh is an alternative) |
| `ROS_DOMAIN_ID` | Groups ROS nodes that can discover each other; see [ROS domains](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Domain-ID.html). | `42` here; 0–101 is recommended on Linux |
| `ARM_MODEL`| Selects the arm type | default=`piper_x`, `piper_l`, `piper_h` |
| `NAV2_MAP` | Selects the saved map on which AMCL localizes (used by `nav2-sim`; real navigation is planned) | default=`map.yaml` |
| `SIM_WORLD` | Selects the Gazebo world. | `curtmini_piper`, `curtmini_piper_map`, another packaged world, or an SDF path inside the container |
| `SIM_USE_HOKUYO` | Enables the simulated lidar. | `true` or `false` |
| `SIM_USE_CAMERAS` | Enables the simulated cameras and their IMUs. | `true` or `false` |
| `COMPOSE_FILE` | Lists [Compose files](https://docs.docker.com/compose/how-tos/environment-variables/envvars/#compose_file) to combine. | Colon-separated files; see the workflows below |

## About gz worlds and SIM_WORLD env variable
For `SIM_WORLD`, browse the [simulator worlds](https://github.com/ipa-may/curtmini_piper_gz_sim/tree/main/worlds)
and [Neo worlds](https://github.com/ipa-may/neo_gz_worlds/tree/gz-harmonic/worlds).

To add an environment, create an [SDF world](https://gazebosim.org/docs/harmonic/sdf_worlds/)
in the simulator's `worlds/` directory, publish it for regular image builds,
rebuild the image, and set `SIM_WORLD` to its filename without `.sdf`.

The office world above is useful for navigation; the template initially selects
the simpler `curtmini_piper` world. To make a useful map, change the **actual**
`.env` file to `SIM_WORLD=curtmini_piper_map`, or use the explicit world override
in the [mapping walkthrough](../../startup/mapping.md#start-mapping).

## About COMPOSE_FILE env variable
`COMPOSE_FILE` lists the files to combine, in order, separated by colons on Linux. Choose one active `COMPOSE_FILE` line:

| Workflow | Value of `COMPOSE_FILE` in `.env` |
| --- | --- |
| Regular simulation, Nav2, or hardware, with GUI | `compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml` |
| Optional local simulation workspace, with GUI | `compose.yaml:compose.cyclonedds.yaml:compose.workspace.yaml:compose.gui.yaml` |

For regular images, use `--build` with the services you want to start.

For unpublished changes, see [which source workflow to use](image_builds.md#choose-a-source-workflow).

:::{attention}
Changing `.env` changes future Compose commands; it does not restart already running services.
:::

With the regular-image setting, for example, hardware startup becomes:

```sh
xhost +si:localuser:root
docker compose up --build piper-bringup moveit-rviz-hardware
```

The selected overlays apply to each command run from this directory.

## On GUI access

The `xhost` command is needed once per desktop session for GUI access:
```sh
xhost +si:localuser:root
```

`compose.gui.yaml` passes the display and graphics devices to the containers; omitting it can cause RViz to exit with a Qt `xcb` error.

## Temporary overrides and precedence

Shell variables override matching `.env` values. If an earlier terminal setup
exported these settings, clear those exports to use `.env` again:

```sh
unset CONTAINER_ROS_DISTRO RMW ROS_DOMAIN_ID SIM_WORLD SIM_USE_HOKUYO SIM_USE_CAMERAS COMPOSE_FILE
```

To change a setting for one command, put it before the command:

```sh
SIM_WORLD=curtmini_piper docker compose up gz-sim
```

Explicit `-f` options override the file list in `COMPOSE_FILE`; they do not add
to it. For example, this command explicitly selects the regular GUI setup:

```sh
docker compose -f compose.yaml -f compose.cyclonedds.yaml -f compose.gui.yaml \
  up --build gz-sim moveit-rviz-sim
```

See Docker's [`.env` explanation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/)
and [COMPOSE_FILE reference](https://docs.docker.com/compose/how-tos/environment-variables/envvars/#compose_file).

## Checkout paths

Compose supplies the default checkout paths. Override them in `.env` only for
a different layout:

```sh
CURTMINI_PIPER_SOURCE=../rob4_fraunhofer_ws/src/curtmini_piper
CURTMINI_PIPER_TOOLS_SOURCE=../rob4_fraunhofer_ws/src/curtmini_piper_tools
CURTMINI_PIPER_GZ_SIM_SOURCE=../rob4_fraunhofer_ws/src/curtmini_piper_simulation/curtmini_piper_gz_sim
NEO_GZ_WORLDS_SOURCE=../rob4_fraunhofer_ws/src/curtmini_piper_simulation/neo_gz_worlds
```

The robot, simulator and tools checkouts are required to load their included Compose
files. If the infrastructure checkout is elsewhere, set `CONTAINER_INFRA_SOURCE`
to its absolute path so application builds can find the shared scripts.

`CURTMINI_PIPER_SOURCE` selects the local robot checkout for Compose definitions
and runtime mounts. It does **not** select the source compiled into regular
robot images; that is controlled by `CURTMINI_PIPER_IMAGE_SOURCE`; see [image source workflows](image_builds.md#choose-a-source-workflow).

## Hardware settings

| Variable | Purpose |
| --- | --- |
| `CAN_PORT` | Piper CAN interface; default `can0` |
| `CONTROL_ENABLED` | Piper driver command gate; default `true` |
| `FAST_MODE` | Piper streamed-setpoint mode; default `true` |
| `PUBLISH_BASE_DESCRIPTION` | Default `False` with Piper; set `True` for the base alone |
| `LPMS_DEVICE` | Base IMU device; default `/dev/ttyLPMSCA3D00510053` |
| `JOYSTICK_DEVICE` | Base joystick device; default `/dev/input/js0` |
| `BASE_CAMERA_SERIAL`, `TOOL_CAMERA_SERIAL` | Distinct physical camera serial numbers |

Set device paths to match the hardware host. See [hardware startup](../../startup/real_hardware.md) and [arm command behavior](../moveit.md#hardware-command-path).

## Task settings

| Variable | Purpose |
| --- | --- |
| `SIM_USE_APRILTAGS` | Spawn the packaged panels in the office simulation; default `false` |
| `APRILTAG_SIZE` | Detector black-square edge size in metres; default `0.20`, must match the panels |
| `TAG_FRAME` | Observed tag frame for `tag-pose-sim`; default `tag36h11:0` |
| `MOVEIT_PLAN_ONLY` | Plan without execution by default; `false` enables motion |

See [AprilTag configuration](../apriltags.md) and [MoveIt goal parameters](../moveit.md#goal-parameters).
