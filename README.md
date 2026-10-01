# Set up the workspace

## 1. Clone the repositories

Install Git, vcstool, and [Docker with Compose](docs/installation/software/docker.md).
Use your own GitHub account; see the [Git guide](docs/student_helpers/Tools/git.md)
for SSH setup.

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

Set `CONTAINER_ROS_DISTRO=jazzy` and `RMW=cyclonedds` in `.env`. The host's
`ROS_DISTRO` does not select the container distro. For an existing configuration,
check its source paths against `.env.example`, especially:

```dotenv
CURTMINI_PIPER_GZ_SIM_SOURCE=../rob4_fraunhofer_ws/src/curtmini_piper_simulation/curtmini_piper_gz_sim
NEO_GZ_WORLDS_SOURCE=../rob4_fraunhofer_ws/src/curtmini_piper_simulation/neo_gz_worlds
```

The infrastructure includes the Compose files in `curtmini_piper/docker/` and
`curtmini_piper_gz_sim/docker/`. Each application repository owns its Dockerfile,
package lists, and source dependency manifest. Image builds copy that repository's
local code and clone its upstream dependencies from GitHub. See
[Docker architecture and source inputs](docs/installation/software/docker.md#where-the-docker-files-live).

## 3. Run or develop

- [Gazebo office world, RViz, and keyboard teleop](docs/startup/simulation.md)
- [Real hardware](docs/startup/real_hardware.md)
- [Standalone RViz](docs/startup/rviz.md) and [MoveItPy](docs/startup/moveitpy.md)
- [Local workspace development](docs/installation/software/docker.md#local-workspace-development):
  build mounted sources into a shared install volume instead of rebuilding application images.
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
