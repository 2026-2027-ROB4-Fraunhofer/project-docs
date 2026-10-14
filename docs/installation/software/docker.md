# Docker installation

## Install Docker

Follow Docker's [Ubuntu installation guide](https://docs.docker.com/engine/install/ubuntu/)
and [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/).
Install the Compose plugin too; use **Docker Compose 2.24.4 or newer** for all
workflows in this guide. The workspace and test overlays use
[`!override`](https://docs.docker.com/reference/compose-file/merge/#replace-value),
which requires that version. Use `docker compose` (with a space), not the legacy
`docker-compose` command.

```sh
docker compose version
```

Docker provides the project's ROS 2 environment without a host ROS installation.
See [Docker cleanup](../../student_helpers/Tools/docker.md) for managing disk usage.

## Configure this project

After [cloning the workspace](index.md#create-the-workspace), run Compose commands
from the infrastructure repository:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
[ -f .env ] || cp .env.example .env
```

### Configure once with `.env`

Edit `curtmini_piper_containers/.env` in your text editor. Docker Compose reads
it automatically whenever you run a command from this directory. You do not
need to run `source .env` or repeat shell exports in every terminal.
`.env.example` is a template; copy it to `.env` to use its settings.

The example selects regular application images with GUI support:

```sh
CONTAINER_ROS_DISTRO=jazzy
RMW=cyclonedds
ROS_DOMAIN_ID=42
SIM_WORLD=curtmini_piper_map
SIM_USE_HOKUYO=true
SIM_USE_CAMERAS=true
COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml
```

The office world above is useful for navigation; the template initially selects
the simpler `curtmini_piper` world. To make a useful map, change the **actual**
`.env` file to `SIM_WORLD=curtmini_piper_map`, or use the explicit world override
in the [navigation guide](../../startup/navigation.md#2-make-a-map).
`COMPOSE_FILE` lists the files to combine,
in order, separated by colons on Linux. Choose one active `COMPOSE_FILE` line:

| Workflow | Value of `COMPOSE_FILE` in `.env` |
| --- | --- |
| Regular simulation, Nav2, or hardware, with GUI | `compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml` |
| Optional local simulation workspace, with GUI | `compose.yaml:compose.cyclonedds.yaml:compose.workspace.yaml:compose.gui.yaml` |

For regular images, use `--build` with the services you want to start. If an
existing `.env` still selects `compose.workspace.yaml`, remove it for this
workflow. For unpublished changes, see [which source workflow to use](#choose-a-source-workflow).
Changing `.env` changes future Compose commands; it does not restart already
running services.

With the regular-image setting, for example, hardware startup becomes:

```sh
xhost +si:localuser:root
docker compose up --build piper-bringup moveit-rviz-hardware
```

In each new terminal, just change to `curtmini_piper_containers/` and run the
short commands. The `xhost` command is needed once per desktop session for GUI
access. `compose.gui.yaml` passes the display and graphics devices to the
containers; omitting it can cause RViz to exit with a Qt `xcb` error.

### Container ROS distribution

`CONTAINER_ROS_DISTRO=jazzy` selects the container ROS version independently of
the host's `ROS_DISTRO`. `RMW=cyclonedds` selects the ROS communication middleware,
and `ROS_DOMAIN_ID=42` selects the ROS domain. Keep the same values for services
that must communicate. Dockerfiles still use `ROS_DISTRO` internally.

For Zenoh, set `RMW=zenoh` and replace `compose.cyclonedds.yaml` with
`compose.zenoh.yaml` in the `.env` file's `COMPOSE_FILE` value.

### Temporary overrides and precedence

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

## What the Compose files do

These files are in `curtmini_piper_containers/`:

| File | Purpose |
| --- | --- |
| `compose.yaml` | Includes the robot, simulator and tools service definitions: their images, commands and default settings. |
| `compose.cyclonedds.yaml` | Adds CycloneDDS communication settings to the named application services. |
| `compose.zenoh.yaml` | Alternative communication setup using Zenoh; also defines `zenoh-router`. |
| `compose.workspace.yaml` | Adds `workspace-builder` and makes simulation clients use its shared installation. |
| `compose.gui.yaml` | Includes display and graphics settings for Gazebo and RViz. |

An overlay is simply a Compose file that adds to or changes the selected
configuration. `compose.cyclonedds.yaml` is not the complete service definition
or a list of everything to start. Its service names identify which services
receive CycloneDDS settings. `workspace-builder`, for example, is defined in
the workspace file and does not need those runtime communication settings.

The project GUI file includes `curtmini_piper/compose.gui.yaml`, which collects
the MoveIt and navigation packages' GUI settings, plus the simulator's GUI file.
Keep the project GUI overlay selected when opening Gazebo or RViz. These files
provide display access; they do not start additional services on their own.

Choose services by name, such as `docker compose up gz-sim moveit-rviz-sim`.
Including a file does not start every service listed in it. See
[Which service should I use?](../../startup/services.md) for their roles.

## Where the Docker files live

There are three layers:

1. **Package:** its Dockerfile describes how to build an image; its Compose file
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
robot images; that is controlled by `CURTMINI_PIPER_IMAGE_SOURCE` below.

## Upstream code and local settings

By default, regular application image builds fetch their owning repository from
upstream `main` (the published branch on GitHub). The four tools images use the
published `curtmini_piper_tools/main` source. Robot image builds can instead use
a local checkout; see [local robot images](#build-local-robot-images). Use the
workspace overlay for unpublished tools changes. Robot and simulator `vcs import`
steps still clone dependencies from GitHub using their manifests. Hardware's
Python SDK revision is in the robot repository's
`curtmini_piper_bringup/docker/dependencies/jazzy-hardware-python.env`.

The tools repository is private. Give the Docker builder an SSH key with access
to it before building regular `moveitpy-sim`, `moveit-action-client-sim`,
`nav2-goal-client`, or `tag-pose-sim` images. Compose uses
the SSH agent by default. If your SSH configuration selects a specific key for
a GitHub host alias, set
`CURTMINI_PIPER_TOOLS_SSH_AUTH=default=/absolute/path/to/private_key` in
`curtmini_piper_containers/.env`. The repository needs a published `main` branch
before these regular images can build.

Compose still loads service definitions from the local robot, simulator and tools
checkouts. Local edits to root or package Compose files can therefore change
commands, mounts, and build settings even for regular images. The local
`geometry.yaml`, `camera_mounts.yaml`, `initial_state.yaml`, and navigation maps
also remain runtime inputs. Review those files when checking a student's setup.

For example, the Gazebo image builds upstream `curtmini_piper_gz_sim` code and
imports `curtmini_piper`, `curt_mini`, `agx_arm_urdf`, and `neo_gz_worlds` from
its manifest. `neo_gz_worlds` uses the `gz-harmonic` branch for the office
assets. The project-level
`project-docs/dependencies.repos` creates the host workspace layout.

### Robot geometry in the simulator image

The Gazebo build gets the robot description and MoveIt configuration from
upstream `curtmini_piper/main`. The description reads
`curtmini_piper_description/config/geometry.yaml`, whose local directory is
bind-mounted into the containers. Restart the simulation and its clients after
changing mount values in that YAML; no image rebuild is needed for those values.
The simulator also publishes the camera mount TFs from the same geometry file.
Physical camera mount TFs use the separate, measured
`curtmini_piper_sensors/config/camera_mounts.yaml`.
See [Cameras](../../startup/cameras.md) for the two setups.

Changes to URDF, launch, bridge, or controller code require updating upstream
`main` and rebuilding the regular image. The local workspace workflow can test
those changes before they are published.

The simulation's starting base pose and six arm joint positions are configured
in `curtmini_piper_gz_sim/config/initial_state.yaml`. The `gz-sim` service
bind-mounts that file, so a service restart applies pose edits without
rebuilding the image. Bridge and controller YAML files use the upstream image
copies. See the [simulation guide](../../startup/simulation.md#starting-pose-and-joint-positions).

Rebuild an application image after upstream code changes. `--build` may reuse
cached Git imports even when a remote branch advances. To fetch the latest
simulator commit after pushing it to `main`, run:

```sh
docker compose build --no-cache gz-sim
```

For published navigation package changes, use `mapping-sim` in place of
`gz-sim`; the navigation services share its image. Then recreate the affected
services with the commands in the [simulation guide](../../startup/simulation.md)
or [navigation guide](../../startup/navigation.md).

## Choose a source workflow

Start with the first row unless you are changing source code:

| Your task | Workflow | Source used |
| --- | --- | --- |
| Run the published project | Regular images, without `compose.workspace.yaml` | GitHub `main` by default |
| Test changes in robot packages, including hardware bringup | [Build local robot images](#build-local-robot-images), without `compose.workspace.yaml` | Local `curtmini_piper` checkout; dependencies still come from their manifests |
| Develop simulation or tools alongside robot packages | [Local workspace](#local-workspace-development), with `compose.workspace.yaml` | Mounted local sources compiled into a shared install volume; hardware services keep their own images |

### Build local robot images

Use this when you have edited a robot package but have not pushed the changes
to GitHub. Keep the regular-image `COMPOSE_FILE` selection in `.env` (without
`compose.workspace.yaml`). From the infrastructure directory:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
CURTMINI_PIPER_IMAGE_SOURCE="$(realpath ../rob4_fraunhofer_ws/src/curtmini_piper)" \
  docker compose build piper-bringup moveit-rviz-hardware
```

This example builds the arm and RViz images; it does **not** start the robot.
Replace the service names with the ones you need, such as `mapping-sim` for
navigation. The override uses an absolute path so package Compose files all
find the same source directory. Compose builds the required shared robot
images automatically.

The override affects robot image builds only. It does not switch the Gazebo or
tools images to local source. In particular, use the workspace workflow to test
local robot description changes inside Gazebo.

The variable above applies to that one command. After following the relevant
startup guide, start the built services with `docker compose up SERVICE`
without `--build`; another build without the override uses published source
again. Local builds use the same image tags as regular builds. To return to
published robot images, rebuild the affected services without the override.

For repeated local builds, you can instead set `CURTMINI_PIPER_IMAGE_SOURCE`
to the absolute checkout path in `curtmini_piper_containers/.env`. Remove that
setting and any shell export (`unset CURTMINI_PIPER_IMAGE_SOURCE`) when returning
to published source.

Keep the robot and infrastructure checkouts compatible. If the package Docker
layout has not yet been published on upstream `main`, use this local override
until it is published; the default remote build cannot find unpublished files.

## Local workspace development

Use `compose.workspace.yaml` to test unpublished edits in local simulator,
navigation, or tools sources. The builder compiles these packages into
a shared Docker install volume; hardware services keep using their own images.

In `curtmini_piper_containers/.env`, use the local-workspace file selection:

```sh
COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.workspace.yaml:compose.gui.yaml
```

Build the development image and mounted sources before starting the affected
simulation services:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
docker compose build workspace-builder
docker compose run --rm workspace-builder
```

Then start the services from the relevant startup guide. After further source
edits, stop those services, rerun `workspace-builder`, and restart them. To
return to regular images, remove `compose.workspace.yaml` from `COMPOSE_FILE`
and start the services with `--build`. The container repository's
[workspace guide](https://github.com/ipa-may/curtmini_piper_containers/blob/main/README.md#local-simulation-workspace)
has the details about mounts and cached dependencies.

## Optional developer checks

Normal startup does not need `curtmini_piper/compose.test.yaml`. This optional
overlay selects Dockerfile stages that run checks while building separate test
images. It checks Xacro expansion, MoveIt launch-argument parsing, teleop package
availability, and any registered package tests. Coverage depends on the tests
each package provides; a successful build is not proof of correct robot behavior.

These build checks do not start hardware services or verify CAN communication,
firmware, or physical motion. Do not add the test overlay to the normal project
`COMPOSE_FILE`. Test build commands and infrastructure configuration checks are
in the robot repository's
[container checks guide](https://github.com/ipa-may/curtmini_piper/blob/main/doc/containers.md#checks).
