# Software

## Create the workspace

Install Git and vcstool before importing the repositories. Use your own GitHub
account; see the [Git guide](../../helpers/Tools/git.md) for SSH setup.
Your account needs access to the private `curtmini_piper_tools` repository.

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
    ├── curtmini_piper_tools/
    ├── curtmini_piper_simulation/
    │   ├── curtmini_piper_gz_sim/
    │   └── neo_gz_worlds/
    └── piper_driver/
        ├── agx_arm_ros/
        └── agx_arm_urdf/
```

For repository responsibilities and container organization, see [Compose files](../../explanation/compose_project/compose_files.md).

## Choose an installation workflow

Start with [Docker](docker.md) to run simulation, visualization, and hardware
bringup without installing ROS 2 on your host. Default image builds use published
source. For unpublished changes, choose between
[building local robot images](../../startup/development.md#build-local-robot-images) and the
[workspace overlay](../../startup/development.md#local-workspace-development) for simulation and tools.

On Ubuntu 24.04, [native source installation](source.md) is an alternative for
building and debugging ROS 2 Jazzy packages directly on the host.

```{toctree}
:maxdepth: 1

docker
source
```
