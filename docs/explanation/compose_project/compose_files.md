# Compose files and repository organization

## What the Compose files do

These files are in `curtmini_piper_containers/`:

| File | Purpose |
| --- | --- |
| `compose.yaml` | Includes the robot, simulator and tools service definitions: their images, commands and default settings. |
| `compose.cyclonedds.yaml` | Adds CycloneDDS communication settings to the named application services. |
| `compose.zenoh.yaml` | Alternative communication setup using Zenoh; also defines `zenoh-router`. |
| `compose.workspace.yaml` | Adds `workspace-builder` and makes simulation clients use its shared installation. |
| `compose.gui.yaml` | Includes display and graphics settings for Gazebo and RViz. |

An overlay is simply a Compose file that adds to or changes the selected configuration.

The project GUI file includes `curtmini_piper/compose.gui.yaml`, which collects
the MoveIt and navigation packages' GUI settings, plus the simulator's GUI file.
Keep the project GUI overlay selected when opening Gazebo or RViz. These files
provide display access; they do not start additional services on their own.

Choose services by name, such as `docker compose up gz-sim moveit-rviz-sim`.

Including a file does not start every service listed in it. See
[Which service should I use?](compose_services.md) for their roles.

## Where the Docker files live

There are three layers:

1. **ROS Packages:** its Dockerfile describes how to build an image; its Compose file
   defines services that use it.
2. **Robot repository:** `curtmini_piper/compose.yaml` includes the package service
   definitions. Its `compose.gui.yaml` collects their optional display settings.
3. **Project infrastructure:** `curtmini_piper_containers` combines robot,
   simulator, and tools services with the chosen communication and GUI settings.

| Location | Maintains |
| --- | --- |
| `curtmini_piper/` | Root `compose.yaml` and `compose.gui.yaml` include the package definitions; `compose.test.yaml` selects optional build checks |
| `curtmini_piper/<package>/docker/` | Each robot package's Dockerfile, dependency lists, and Compose services |
| `curtmini_piper/docker/common/` | Shared ROS base image and its build-only service |
| `curtmini_piper/docker/dependencies/` | Shared arm and mobile-base source manifests |
| `curtmini_piper_tools/` | Root Compose include; each tools package has its own `docker/Dockerfile`, `docker/compose.yaml`, and ROS package list |
| `curtmini_piper_gz_sim/docker/` | Gazebo Dockerfile, package lists, simulation service, and GUI settings |
| `curtmini_piper_containers/` | Compose includes, middleware configuration, shared startup helpers, workspace builder, and Zenoh router |

The robot images share a ROS base. Compose builds shared layers through the
`piper-ros-base`, `piper-description`, and `piper-moveit-config` services. They
have `scale: 0`: they supply images but do not run containers during normal
startup. You do not need to start them manually.

The MoveItPy and C++ MoveIt client
images build on the robot's MoveIt RViz image; the Nav2 client and tag pose
images use a ROS base.
Compose selects the services; the existing
`moveitpy-sim` and `moveitpy-hardware` service names and `moveit_goal` command
remain the same.
Build `moveit-rviz-sim` before the MoveIt client images; `scripts/build-all.sh` does this
automatically.

For package ownership and build details, see the robot repository's
[container guide](https://github.com/ipa-may/curtmini_piper/blob/main/doc/containers.md)
(also available locally at `curtmini_piper/doc/containers.md`).

## Why are service names repeated in the CycloneDDS file?

The infrastructure's root `compose.yaml` includes the service definitions from
the robot, simulator, and tools repositories. The robot root file in turn
includes its package Compose files. Those definitions specify what each service runs.
`compose.cyclonedds.yaml` adds the CycloneDDS configuration file and environment
setting to the application services with matching names.

It therefore lists application services, but it is not the complete catalog:
`workspace-builder` is added by `compose.workspace.yaml`, and `zenoh-router`
belongs to the alternative `compose.zenoh.yaml` setup. You choose one middleware
file in `.env`. See [what the Compose files do](compose_files.md#what-the-compose-files-do).
