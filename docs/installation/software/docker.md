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

### Container ROS distribution

Select the distro and middleware in `.env`:

```sh
CONTAINER_ROS_DISTRO=jazzy
RMW=cyclonedds
ROS_DOMAIN_ID=42
```

`CONTAINER_ROS_DISTRO` defaults to Jazzy, independently of the host's
`ROS_DISTRO`. Dockerfiles still use `ROS_DISTRO` internally.

Shell exports take precedence over `.env`; `.env` is read on each Compose invocation.

Keep the same distro, middleware, and domain in every terminal.

You can save the Compose file selection in `curtmini_piper_containers/.env`,
instead of exporting it in every terminal.

For CycloneDDS with GUI support, set:

```ini
RMW=cyclonedds
COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml
```

Allow the root-run GUI containers to access the X11 display, then run commands
from `curtmini_piper_containers/`. You can name the Compose files explicitly:

```sh
xhost +si:localuser:root
docker compose -f compose.yaml -f compose.cyclonedds.yaml -f compose.gui.yaml \
  up --build gz-sim moveit-rviz-sim
```

With the `COMPOSE_FILE` value above, you can omit the `-f` options and run
`docker compose up --build gz-sim moveit-rviz-sim`. Without `compose.gui.yaml`,
the RViz container has no X11 display and exits with a Qt `xcb` error.

Compose reads `.env` each time you run a command. Previously exported variables
override the values in `.env`; run `unset RMW COMPOSE_FILE` to use the file's settings.

For Zenoh, set `RMW=zenoh` and replace `compose.cyclonedds.yaml` with
`compose.zenoh.yaml`. Zenoh image builds remain supported.

If you provide `-f` options explicitly, Compose uses those files instead of the
`COMPOSE_FILE` selection.

## Where the Docker files live

| Location | Maintains |
| --- | --- |
| `curtmini_piper/docker/` | One Dockerfile with `hardware`, `moveit-rviz`, `moveitpy`, and `teleop` targets; package lists and Compose services |
| `curtmini_piper_gz_sim/docker/` | Gazebo Dockerfile, package lists, simulation service, and GUI settings |
| `curtmini_piper_containers/` | Compose includes, middleware configuration, shared startup helpers, workspace builder, and Zenoh router |

The four robot targets share a ROS base. Hardware, RViz, and MoveItPy also share
MoveIt dependencies and a common robot build stage. Compose selects the targets;
the usual service names and launch commands remain the same.

The default checkout paths are in `.env.example`. In particular:

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
`dependencies.repos`, or `docker/dependencies/<distro>.repos` when present.
Hardware's Python SDK revision is in the robot repository's
`docker/dependencies/<distro>-hardware-python.env`.

For example, the Gazebo image uses local `curtmini_piper_gz_sim` code but downloads
`curtmini_piper`, `curt_mini`, `agx_arm_urdf`, and `neo_gz_worlds` from its manifest.
It does not automatically use those neighbouring checkouts. `neo_gz_worlds` uses
the `gz-harmonic` branch for the office assets. The project-level
`project-docs/dependencies.repos` creates the host workspace layout.

### Robot geometry in the simulator image

The simulator's current dependency manifest pins `curtmini_piper` to revision
`fa5bfdce328d3a69bdc171eec0e19d9f27367bcc`, before the robot description
began reading `curtmini_piper_description/config/geometry.yaml`. The standard
`gz-sim` image therefore uses the arm, TCP, and lidar mount defaults in that
revision's Xacros, even though the source `config` directory is bind-mounted.
Changing the local geometry YAML alone does not change the simulated model in
that image. The [local workspace workflow](#local-workspace-development) builds
the neighbouring robot checkout and uses its YAML-aware description.

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
install volume. No host ROS build is required.

Check all source paths in `.env.example`, including `CURT_MINI_SOURCE`,
`AGX_ARM_URDF_SOURCE`, and the nested simulation paths above. In each terminal
used for this workflow:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
export CONTAINER_ROS_DISTRO=jazzy
export RMW=cyclonedds
export ROS_DOMAIN_ID=42
export COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.workspace.yaml:compose.gui.yaml
```

Before starting simulation, build the development image and the mounted sources:

```sh
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
package lists change. The helper imports missing upstream dependencies and
retains existing cached checkouts; changing a manifest revision alone does not
update those cached repositories.

Keep `compose.workspace.yaml` in the launch commands that should use this
installation. To return to normal application images, remove it from
`COMPOSE_FILE` and launch with `--build` again.

The container repository has further details in its
[Compose file guide](https://github.com/ipa-may/curtmini_piper_containers/blob/main/README_compose_files.md)
and [service reference](https://github.com/ipa-may/curtmini_piper_containers/blob/main/README_compose_service.md).
