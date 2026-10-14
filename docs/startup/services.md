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

```{list-table}
:class: service-reference
:widths: 25 42 42
:header-rows: 1

* - Service
  - What it does
  - When to use it
* - `gz-sim`
  - Runs Gazebo, simulated controllers, two cameras, lidar, and the MoveIt server.
  - Start this as the backend for simulation tasks.
* - `moveit-rviz-sim`
  - Opens RViz with the MoveIt panel, camera views, and robot TF.
  - Use with `gz-sim` when working on arm motion. It does not start Gazebo itself.
* - `moveitpy-sim`
  - Runs a Python example that asks MoveIt to plan an arm motion; execution is optional.
  - Use with `gz-sim` for scripted arm motion. `MOVEIT_PLAN_ONLY=true` is the default.
* - `moveit-action-client-sim`
  - Runs a C++ client that sends an arm goal to Gazebo's MoveIt server.
  - Use with `gz-sim` for joint, absolute TCP, or relative TCP goals. It plans only by default.
* - `keyboard-teleop-sim`
  - Turns keyboard input into mobile-base velocity commands.
  - Use with `gz-sim` to drive manually, including while making a map.
* - `mapping-sim`
  - Runs SLAM Toolbox to build a map from lidar scans and odometry.
  - Use with `gz-sim` in the `curtmini_piper_map` office world and manual driving to create a map, then save it.
* - `nav2-sim`
  - Loads a saved map, localizes with AMCL, and runs Nav2 to drive the base to goals.
  - Use with `gz-sim` after creating a map. Stop mapping and keyboard driving first.
* - `nav2-rviz-sim`
  - Opens RViz with the map, lidar, path, initial-pose and navigation-goal tools.
  - Use during mapping or navigation. It does not start SLAM or Nav2 itself.
* - `tag-pose-sim`
  - Publishes a fresh observed AprilTag pose in `map` using the camera and robot TF chain.
  - Use with `apriltag-base` and either mapping or Nav2 localization.
* - `nav2-goal-client`
  - Provides the Python `nav_to_pose` command in a one-off container.
  - Use with an active Nav2 server after choosing a goal in free space.
```

**MoveIt controls arm motion; Nav2 controls mobile-base navigation.** Choose
the RViz service that matches your task.

The [simulation guide](simulation.md) covers Gazebo and keyboard driving.
The [camera guide](cameras.md) covers simulated images, mounts, and TF.
The [navigation guide](navigation.md) covers saving a map, switching from SLAM
to AMCL, and sending goal poses. Mapping and AMCL must not run together because
both publish the `map → odom` transform. Stop keyboard driving before Nav2
drives because both send commands to the base.
See [Python tools](tools.md) for tag poses and scripted Nav2 goals.

## Real robot

```{list-table}
:class: service-reference
:widths: 28 38 38
:header-rows: 1

* - Service
  - What it does
  - When to use it
* - `base-bringup`
  - Starts the Curt Mini base, joystick, and IMU using `curt_mini_bringup`.
  - Use with `piper-bringup` for the complete real robot.
* - `realsense-base`
  - Starts the base D435i selected by `BASE_CAMERA_SERIAL` and publishes its mount TF.
  - Use when base color, depth, or camera IMU data is needed.
* - `realsense-tool`
  - Starts the tool D435i selected by `TOOL_CAMERA_SERIAL` and publishes its mount TF.
  - Use when end-effector color, depth, or camera IMU data is needed.
* - `piper-bringup`
  - Starts the Piper arm, complete robot model, and MoveIt.
  - Use alone for arm work or with `base-bringup` for the complete robot.
* - `moveit-rviz-hardware`
  - Opens the MoveIt RViz client connected to the real robot.
  - Use with `piper-bringup`.
* - `moveitpy-hardware`
  - Runs the Python arm-motion example against real hardware.
  - Use after hardware bringup; it plans only by default. `MOVEIT_PLAN_ONLY=false` enables execution.
* - `moveit-action-client-hardware`
  - Sends a C++ arm goal to the real robot's MoveIt server.
  - Use with `piper-bringup`; it plans only by default.
* - `keyboard-teleop-hardware`
  - Sends keyboard driving commands through the base's command multiplexer.
  - Use with `base-bringup`.
```

Start `piper-bringup` for the arm, and add `base-bringup` when driving the base. Follow the
[hardware guide](real_hardware.md) for CAN setup and startup commands.
The two RealSense services can run separately; see [Cameras](cameras.md) for
serial numbers and measured mount poses.
For example, after preparing the arm and GUI access:

```sh
docker compose up --build piper-bringup moveit-rviz-hardware
```

The navigation services currently target simulation.

## Build and inspection tools

```{list-table}
:class: service-reference
:widths: 25 42 42
:header-rows: 1

* - Service
  - What it does
  - When to use it
* - `workspace-builder`
  - Builds local simulation, navigation and MoveIt example packages into shared Docker volumes. It excludes hardware bringup and drivers.
  - Optional: use it to test unpublished local source changes. See the local workspace guide.
* - `ros-cli`
  - Opens a shell with ROS command-line tools.
  - Inspect nodes, topics, services or actions using the same middleware and domain as the running robot.
* - `zenoh-router`
  - Routes ROS communication for the Zenoh setup.
  - Available with `compose.zenoh.yaml`; services in that setup depend on it. CycloneDDS does not need this service.
```

For `workspace-builder`, see
[local workspace development](../installation/software/docker.md#local-workspace-development).

You may also see `piper-ros-base`, `piper-description`, and
`piper-moveit-config` when listing services. They build shared robot images,
not running robot components. They have zero replicas (`scale: 0`), so normal
startup creates no containers for them. Compose builds these images when
another robot image needs them; you do not need to start them manually.

The robot repository also has an optional `compose.test.yaml` for
[developer build checks](../installation/software/docker.md#optional-developer-checks).
It is not part of normal startup and does not test physical hardware.

## Why are service names repeated in the CycloneDDS file?

The infrastructure's root `compose.yaml` includes the service definitions from
the robot, simulator, and tools repositories. The robot root file in turn
includes its package Compose files. Those definitions specify what each service runs.
`compose.cyclonedds.yaml` adds the CycloneDDS configuration file and environment
setting to the application services with matching names.

It therefore lists application services, but it is not the complete catalog:
`workspace-builder` is added by `compose.workspace.yaml`, and `zenoh-router`
belongs to the alternative `compose.zenoh.yaml` setup. You choose one middleware
file in `.env`. See [what the Compose files do](../installation/software/docker.md#what-the-compose-files-do).

## Useful commands

```{list-table}
:class: command-reference
:widths: 42 58
:header-rows: 1

* - Command
  - Purpose
* - `docker compose up SERVICE`
  - Starts a service and shows its logs. Add `--build` when its image needs building.
* - `docker compose up -d SERVICE`
  - Starts a service in the background.
* - `docker compose run --rm SERVICE`
  - Runs a separate container for a tool, then removes that container when it exits. Useful for the builder and interactive keyboard driving.
* - `docker compose logs -f SERVICE`
  - Follows service logs. Ctrl+C stops following the logs, not the service.
* - `docker compose stop SERVICE`
  - Stops the named service started with `up`.
* - `docker compose ps`
  - Shows the current project's service containers and their status.
* - `docker compose --profile '*' config --services`
  - Lists all services in the configuration selected by `.env`, including optional profiles.
```

Replace `SERVICE` with a name from the tables. Naming a service explicitly
activates its profile for that command; students do not need to select profiles
for the startup examples. For `run --rm` keyboard sessions, stop driving and
exit that terminal session with Ctrl+C.
