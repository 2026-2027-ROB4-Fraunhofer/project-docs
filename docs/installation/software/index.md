# Software

## Create the workspace

Install Git and vcstool before importing the repositories. Use your own GitHub
account; see the [Git guide](../../student_helpers/Tools/git.md) for SSH setup.

```sh
sudo apt-get install git python3-vcstool
mkdir -p ~/ROB4_Fraunhofer
cd ~/ROB4_Fraunhofer
git clone git@github.com:2026-2027-ROB4-Fraunhofer/project-docs.git
vcs import . < project-docs/dependencies.repos
```

The imported layout is:

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

`curtmini_piper_containers` assembles the application Compose files and provides
shared middleware configuration and workspace tooling. The application
Dockerfiles, package lists, and Compose services live in the `docker/` folders
of `curtmini_piper` and `curtmini_piper_gz_sim`.

## Choose an installation workflow

Start with [Docker](docker.md) to run simulation, visualization, and hardware
bringup without installing ROS 2 on your host. Local source development is also
possible through the [workspace overlay](docker.md#local-workspace-development).

On Ubuntu 24.04, [native source installation](source.md) is an alternative for
building and debugging ROS 2 Jazzy packages directly on the host.

```{toctree}
:maxdepth: 1

docker
source
```
