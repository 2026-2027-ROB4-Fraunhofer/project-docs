# Which service should I use?

A **Compose service** is a named program setup, such as `gz-sim`. Compose uses
it to create a container with the right image, startup command and settings.
One service can start several ROS nodes.

Configure `curtmini_piper_containers/.env` first using the
[Docker setup](../installation/software/docker.md#configure-once-with-env).
Run the commands below from that directory. Compose reads `.env` automatically,
including the `COMPOSE_FILE` list, so you can choose services by name:

```sh
docker compose up gz-sim moveit-rviz-sim
```

This starts the simulation backend and its MoveIt RViz window. Listing a service
in a Compose file does not mean you must start it for every task.

## Simulation and navigation

| Service | What it does | When to use it |
| --- | --- | --- |
| `gz-sim` | Runs Gazebo, the simulated robot controllers and the MoveIt server. | Start this as the backend for simulation tasks. |
| `moveit-rviz-sim` | Opens RViz with the MoveIt panel to display the robot and plan arm motions. | Use with `gz-sim` when working on arm motion. It does not start Gazebo itself. |
| `moveitpy-sim` | Runs a Python example that asks MoveIt to plan an arm motion; execution is optional. | Use with `gz-sim` for scripted arm motion. `MOVEIT_PLAN_ONLY=true` is the default. |
| `keyboard-teleop-sim` | Turns keyboard input into mobile-base velocity commands. | Use with `gz-sim` to drive manually, including while making a map. |
| `mapping-sim` | Runs SLAM Toolbox to build a map from lidar scans and odometry. | Use with `gz-sim` and manual driving to create a map, then save it. |
| `nav2-sim` | Loads a saved map, localizes with AMCL, and runs Nav2 to drive the base to goals. | Use with `gz-sim` after creating a map. Stop mapping and keyboard driving first. |
| `nav2-rviz-sim` | Opens RViz with the map, lidar, path, initial-pose and navigation-goal tools. | Use during mapping or navigation. It does not start SLAM or Nav2 itself. |

**MoveIt controls arm motion; Nav2 controls mobile-base navigation.** Choose
the RViz service that matches your task.

The [simulation guide](simulation.md) covers Gazebo and keyboard driving.
The [navigation guide](navigation.md) covers saving a map, switching from SLAM
to AMCL, and sending goal poses. Mapping and AMCL must not run together because
both publish the `map → odom` transform. Stop keyboard driving before Nav2
drives because both send commands to the base.

## Real robot

| Service | What it does | When to use it |
| --- | --- | --- |
| `real-bringup` | Starts the Curt Mini base and Piper arm hardware, plus MoveIt. Joystick and IMU are enabled by default. | Use as the backend for the complete real robot. |
| `piper-bringup` | Starts only the real Piper arm and MoveIt, without the base, joystick or IMU. | Use as the backend when working with the arm alone. |
| `moveit-rviz-hardware` | Opens the MoveIt RViz client connected to the real robot. | Use with either `real-bringup` or `piper-bringup`. |
| `moveitpy-hardware` | Runs the Python arm-motion example against real hardware. | Use after hardware bringup; it plans only by default. `MOVEIT_PLAN_ONLY=false` enables execution. |
| `keyboard-teleop-hardware` | Sends keyboard driving commands through the base's command multiplexer. | Use with the mobile base running under `real-bringup`. |

Choose one hardware backend: `real-bringup` or `piper-bringup`. Follow the
[hardware guide](real_hardware.md) for CAN setup and startup commands.
For example, after preparing the arm and GUI access:

```sh
docker compose up --build piper-bringup moveit-rviz-hardware
```

The navigation services currently target simulation.

## Build and inspection tools

| Service | What it does | When to use it |
| --- | --- | --- |
| `workspace-builder` | Builds local simulation, navigation and MoveIt example packages into shared Docker volumes. It excludes hardware bringup and drivers. | Select `compose.workspace.yaml` in `.env`, then run it before local simulation and after source edits. It exits when the build finishes. |
| `ros-cli` | Opens a shell with ROS command-line tools. | Inspect nodes, topics, services or actions using the same middleware and domain as the running robot. |
| `zenoh-router` | Routes ROS communication for the Zenoh setup. | Available with `compose.zenoh.yaml`; services in that setup depend on it. CycloneDDS does not need this service. |

For local development, these commands do different jobs:

```sh
docker compose build workspace-builder
docker compose run --rm workspace-builder
```

`build` creates the development image with ROS dependencies and build tools.
`run` starts a container from that image and builds your mounted ROS packages.
See [local workspace development](../installation/software/docker.md#local-workspace-development).

## Why are service names repeated in the CycloneDDS file?

The root `compose.yaml` includes the service definitions from the robot and
simulator repositories. Those definitions specify what each service runs.
`compose.cyclonedds.yaml` adds the CycloneDDS configuration file and environment
setting to the application services with matching names.

It therefore lists application services, but it is not the complete catalog:
`workspace-builder` is added by `compose.workspace.yaml`, and `zenoh-router`
belongs to the alternative `compose.zenoh.yaml` setup. You choose one middleware
file in `.env`. See [what the Compose files do](../installation/software/docker.md#what-the-compose-files-do).

## Useful commands

| Command | Purpose |
| --- | --- |
| `docker compose up SERVICE` | Starts a service and shows its logs. Add `--build` when its image needs building. |
| `docker compose up -d SERVICE` | Starts a service in the background. |
| `docker compose run --rm SERVICE` | Runs a separate container for a tool, then removes that container when it exits. Useful for the builder and interactive keyboard driving. |
| `docker compose logs -f SERVICE` | Follows service logs. Ctrl+C stops following the logs, not the service. |
| `docker compose stop SERVICE` | Stops the named service started with `up`. |
| `docker compose ps` | Shows the current project's service containers and their status. |
| `docker compose --profile '*' config --services` | Lists all services in the configuration selected by `.env`, including optional profiles. |

Replace `SERVICE` with a name from the tables. Naming a service explicitly
activates its profile for that command; students do not need to select profiles
for the startup examples. For `run --rm` keyboard sessions, stop driving and
exit that terminal session with Ctrl+C.
