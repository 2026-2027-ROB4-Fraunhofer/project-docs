# Docker installation

## Install Docker

Follow Docker's [Ubuntu installation guide](https://docs.docker.com/engine/install/ubuntu/)
and [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/).
Install the Compose plugin too. The refactored configuration uses Compose
`include`; configuration checks have passed with Docker Compose 5.1.4.

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

The example selects local simulation development with GUI support:

```sh
CONTAINER_ROS_DISTRO=jazzy
RMW=cyclonedds
ROS_DOMAIN_ID=42
SIM_WORLD=curtmini_piper_map
SIM_USE_HOKUYO=true
COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.workspace.yaml:compose.gui.yaml
```

The office world above is useful for navigation; the template initially selects
the simpler `curtmini_piper` world. `COMPOSE_FILE` lists the files to combine,
in order, separated by colons on Linux. Choose one active `COMPOSE_FILE` line:

| Workflow | Value of `COMPOSE_FILE` in `.env` |
| --- | --- |
| Local simulation and Nav2, with GUI | `compose.yaml:compose.cyclonedds.yaml:compose.workspace.yaml:compose.gui.yaml` |
| Regular application images or hardware, with GUI | `compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml` |

For local simulation, [build the workspace first](#local-workspace-development).
For regular images, use `--build` with the services you want to start.
Hardware services use their dedicated images even if the workspace file remains
selected. Changing `.env` changes future Compose commands; it does not restart
already running services.

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
unset CONTAINER_ROS_DISTRO RMW ROS_DOMAIN_ID SIM_WORLD SIM_USE_HOKUYO COMPOSE_FILE
```

To change a setting for one command, put it before the command:

```sh
SIM_WORLD=curtmini_piper docker compose up gz-sim
```

Explicit `-f` options override the file list in `COMPOSE_FILE`; they do not add
to it. For example, the following selects regular images for this command even
when `.env` selects the workspace:

```sh
docker compose -f compose.yaml -f compose.cyclonedds.yaml -f compose.gui.yaml \
  up --build gz-sim moveit-rviz-sim
```

See Docker's [`.env` explanation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/)
and [COMPOSE_FILE reference](https://docs.docker.com/compose/how-tos/environment-variables/envvars/#compose_file).

## What the Compose files do

| File | Purpose |
| --- | --- |
| `compose.yaml` | Includes the robot and simulator service definitions: their images, commands and default settings. |
| `compose.cyclonedds.yaml` | Adds CycloneDDS communication settings to the named application services. |
| `compose.zenoh.yaml` | Alternative communication setup using Zenoh; also defines `zenoh-router`. |
| `compose.workspace.yaml` | Adds `workspace-builder` and makes simulation clients use its shared installation. |
| `compose.gui.yaml` | Includes display and graphics settings for Gazebo and RViz. |

An overlay is simply a Compose file that adds to or changes the selected
configuration. `compose.cyclonedds.yaml` is not the complete service definition
or a list of everything to start. Its service names identify which services
receive CycloneDDS settings. `workspace-builder`, for example, is defined in
the workspace file and does not need those runtime communication settings.

Choose services by name, such as `docker compose up gz-sim moveit-rviz-sim`.
Including a file does not start every service listed in it. See
[Which service should I use?](../../startup/services.md) for their roles.

## Where the Docker files live

| Location | Maintains |
| --- | --- |
| `curtmini_piper/docker/` | One Dockerfile with `hardware`, `moveit-rviz`, `moveitpy`, `teleop`, and `navigation` targets; package lists and Compose services |
| `curtmini_piper_gz_sim/docker/` | Gazebo Dockerfile, package lists, simulation service, and GUI settings |
| `curtmini_piper_containers/` | Compose includes, middleware configuration, shared startup helpers, workspace builder, and Zenoh router |

The five robot targets share a ROS base. Hardware, RViz, and MoveItPy also share
MoveIt dependencies and a common robot build stage. Compose selects the targets;
the usual service names and launch commands remain the same.

Compose supplies the default checkout paths. Override them in `.env` only for
a different layout:

```sh
CURTMINI_PIPER_SOURCE=../rob4_fraunhofer_ws/src/curtmini_piper
CURTMINI_PIPER_GZ_SIM_SOURCE=../rob4_fraunhofer_ws/src/curtmini_piper_simulation/curtmini_piper_gz_sim
NEO_GZ_WORLDS_SOURCE=../rob4_fraunhofer_ws/src/curtmini_piper_simulation/neo_gz_worlds
```

The robot and simulator checkouts are required to load their included Compose
files. If the infrastructure checkout is elsewhere, set `CONTAINER_INFRA_SOURCE`
to its absolute path so application builds can find the shared scripts.

## Local code and GitHub dependencies

An application image build copies its owning repository from the local checkout.
Its `vcs import` step clones upstream dependencies from GitHub, using that owner's
`dependencies.repos`. Hardware's Python SDK revision is in the robot repository's
`docker/dependencies/jazzy-hardware-python.env`.

For example, the Gazebo image uses local `curtmini_piper_gz_sim` code but downloads
`curtmini_piper`, `curt_mini`, `agx_arm_urdf`, and `neo_gz_worlds` from its manifest.
It does not automatically use those neighbouring checkouts. `neo_gz_worlds` uses
the `gz-harmonic` branch for the office assets. The project-level
`project-docs/dependencies.repos` creates the host workspace layout.

### Robot geometry in the simulator image

The simulator manifest now tracks `curtmini_piper` on `main`. The robot
description reads `curtmini_piper_description/config/geometry.yaml`, whose
directory is bind-mounted into the containers. Restart the simulation and its
clients after changing it. Older cached images may still contain a description
that ignores this YAML: rebuild with refreshed dependencies, or use the
[local workspace workflow](#local-workspace-development) to build the neighbouring
robot checkout. A manifest change alone does not update an existing image.

The simulation's starting base pose and six arm joint positions are configured
in `curtmini_piper_gz_sim/config/initial_state.yaml`. The `gz-sim` service
bind-mounts that file's directory, so a service restart applies YAML edits
without rebuilding the image. See the [simulation guide](../../startup/simulation.md#starting-pose-and-joint-positions).

Rebuild an application image after changing its local code. `--build` may reuse
cached Git downloads even when a remote branch advances. To refresh simulation
dependencies without changing the manifest:

```sh
docker compose -f compose.yaml -f compose.cyclonedds.yaml build --no-cache gz-sim
```

Then recreate the service with the launch command. See the
[simulation guide](../../startup/simulation.md) for the normal image workflow.

## Local workspace development

Use `compose.workspace.yaml` when you want the simulator and tools to use the
mounted local repositories together. The builder compiles them into a shared
install volume. It builds `curtmini_piper_gz_sim`,
`curtmini_piper_motion_examples`, `curtmini_piper_navigation`, and their dependencies. Hardware bringup and
drivers are excluded; hardware services use their dedicated images without
mounting the shared installation. No host ROS build is required.

In `curtmini_piper_containers/.env`, use the local-workspace file selection:

```sh
COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.workspace.yaml:compose.gui.yaml
```

Before starting simulation, build the development image and the mounted sources:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
docker compose build workspace-builder
docker compose run --rm workspace-builder
```

Allow X11 access once per desktop session, then launch the workspace installation:

```sh
xhost +si:localuser:root
SIM_WORLD=curtmini_piper_map docker compose up gz-sim moveit-rviz-sim
```

The current containers run as root; this X11 rule authorizes their GUI clients.
It is separate from GPU access. In another terminal with the same setup, use
`docker compose run --rm --build keyboard-teleop-sim` or follow the
[MoveItPy guide](../../startup/moveitpy.md).

After source edits, stop the affected services, rerun `workspace-builder`, and
start them again with this overlay. Rebuild the development image when its
package lists or workspace helper scripts change. The helper reads only the
simulator's dependency manifest and retains existing cached checkouts; changing
a manifest revision alone does not update those cached repositories. Older
cached hardware dependencies are left in place but are not built.

Keep `compose.workspace.yaml` in the `.env` file's `COMPOSE_FILE` value while
using this installation. To return to regular application images, stop the
affected services, remove it from `COMPOSE_FILE`, and launch with `--build` again.

The container repository has further details in its
[Compose file guide](https://github.com/ipa-may/curtmini_piper_containers/blob/main/README_compose_files.md)
and [service reference](https://github.com/ipa-may/curtmini_piper_containers/blob/main/README_compose_service.md).

For mapping and goal navigation, follow [Navigation in simulation](../../startup/navigation.md).
