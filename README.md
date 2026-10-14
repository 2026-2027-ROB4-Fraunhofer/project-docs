# Set up the workspace

## 1. Clone the repositories

Install Git, vcstool, and [Docker with Compose](docs/installation/software/docker.md).
Use your own GitHub account; see the [Git guide](docs/student_helpers/Tools/git.md)
for SSH setup.
Your GitHub account also needs access to the private `curtmini_piper_tools`
repository before importing the workspace manifest.

```sh
sudo apt-get install git python3-vcstool
mkdir -p ~/ROB4_Fraunhofer
cd ~/ROB4_Fraunhofer
git clone git@github.com:2026-2027-ROB4-Fraunhofer/project-docs.git
vcs import . < project-docs/dependencies.repos
```

The workspace layout is:

```text
ROB4_Fraunhofer/
├── project-docs/
├── curtmini_piper_containers/
└── rob4_fraunhofer_ws/src/
    ├── curt_mini/
    ├── curtmini_piper/
    ├── curtmini_piper_tools/
    ├── curtmini_piper_simulation/
    │   ├── curtmini_piper_gz_sim/
    │   └── neo_gz_worlds/
    └── piper_driver/
        ├── agx_arm_ros/
        └── agx_arm_urdf/
```

## 2. Configure Docker

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
[ -f .env ] || cp .env.example .env
```

Docker Compose automatically reads `.env` when you run commands from this
directory. Edit it once; no `source .env`, repeated exports or `-f` options are
needed. The template selects regular application images with GUI support:

```ini
CONTAINER_ROS_DISTRO=jazzy
RMW=cyclonedds
ROS_DOMAIN_ID=42
COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml
```

If an existing `.env` still includes `compose.workspace.yaml`, remove it for
the regular-image workflow. The workspace overlay is optional for testing
unpublished local code.

The host's `ROS_DISTRO` does not select the container distro. Previously exported
shell variables take precedence over `.env`. See the
[Docker configuration guide](docs/installation/software/docker.md#configure-once-with-env)
for workflow selection, precedence and alternate checkout paths.

Each robot package owns its Dockerfile and service definitions in a `docker/`
folder. `curtmini_piper/compose.yaml` collects those services, and
`curtmini_piper_containers` combines them with simulation and tools, adding
project-wide communication and GUI settings.

By default, image builds use published code from upstream `main`. To build
unpublished robot changes, use the [local robot image workflow](docs/installation/software/docker.md#build-local-robot-images).
The workspace overlay is a separate option for local simulation and tools
development. Mount settings such as `geometry.yaml` remain local. See
[Docker architecture and source inputs](docs/installation/software/docker.md#where-the-docker-files-live).

## 3. Run or develop

- [Which service should I use?](docs/startup/services.md)
- [Mapping and Nav2 goal navigation](docs/startup/navigation.md)
- [Gazebo office world, RViz, and keyboard teleop](docs/startup/simulation.md)
- [Two cameras in Gazebo and on hardware](docs/startup/cameras.md)
- [AprilTag navigation exercise](docs/startup/apriltags.md)
- [Python tools and examples](docs/startup/tools.md)
- [Real hardware](docs/startup/real_hardware.md)
- [Standalone RViz](docs/startup/rviz.md) and [MoveItPy](docs/startup/moveitpy.md)
- [Optional local workspace development](docs/installation/software/docker.md#local-workspace-development):
  build unpublished local sources into a shared install volume.
- [Native ROS 2 source installation](docs/installation/software/source.md)

## Build the documentation

From `project-docs`, install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```sh
uv venv
source .venv/bin/activate
uv pip install -r docs/requirements.txt
sphinx-build -W --keep-going -b html docs docs/_build/html
```

Open `docs/_build/html/index.html`, or preview it with:

```sh
uv run python -m http.server 8000 --directory docs/_build/html
```

GitHub Actions builds the same guide on pull requests and pushes to `main`.
