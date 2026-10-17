# Docker installation

## Install Docker

Follow Docker's [Ubuntu installation guide](https://docs.docker.com/engine/install/ubuntu/) and [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/), including the Compose plugin.
The project images target AMD64 (x86-64). Docker supplies ROS 2; a host ROS installation is not required.

Check that Compose is version 2.24.4 or newer, or **2.30.0 or newer for the NVIDIA overlay** ([Docker requirement](https://docs.docker.com/reference/compose-file/services/#gpus)):

```sh
docker compose version
```

Use `docker compose` with a space. See [Compose files](../../explanation/compose_project/compose_files.md) for the project layout and [Docker cleanup](../../helpers/Tools/docker.md) for disk usage.

## Configure once with `.env`

First [clone the workspace](index.md#create-the-workspace). Then:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
[ -f .env ] || cp .env.example .env
```

Edit the actual `.env` file to use these regular-image settings:

```ini
CONTAINER_ROS_DISTRO=jazzy
RMW=cyclonedds
ROS_DOMAIN_ID=42
ARM_MODEL=piper_x
SIM_WORLD=curtmini_piper_map
SIM_USE_HOKUYO=true
SIM_USE_CAMERAS=true
```

The office world is used for the mapping walkthrough. The supplied template selects `curtmini_piper`, the simpler ground-plane world.
Run Compose commands from this directory; it reads `.env` automatically. You do not need `source .env` or repeated exports.

For other settings and conflicting shell exports, see [environment settings](../../explanation/compose_project/environment.md).

## Select Gazebo graphics

The template enables NVIDIA by default. It needs a working host driver (`nvidia-smi`) and the [NVIDIA Container Toolkit configured for Docker](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).
Choose one active line in `.env`:

```ini
# NVIDIA
COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml:compose.nvidia.yaml
# Without NVIDIA selection (e.g. Intel or AMD): use this line instead
# COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml
```

See [GPU scope and switching](../../explanation/compose_project/environment.md#gazebo-gpu-selection).

## Access for tools image builds

The tools repository is private. Your SSH agent must have a key with access to it when building the MoveIt, Nav2-client and tag-pose tool images.
Alternatively, set this in `.env`, using your key's absolute path:

```ini
CURTMINI_PIPER_TOOLS_SSH_AUTH=default=/absolute/path/to/private_key
```

See [Git SSH setup](../../helpers/Tools/git.md#connect-to-github-with-ssh) and [image source details](../../explanation/compose_project/image_builds.md#upstream-code-and-local-settings).

## Start a task

Continue to [Startup and walkthrough](../../startup/index.md). Each task supplies its build/start commands and any GUI preparation.
For unpublished local code, use [development workflows](../../startup/development.md).
