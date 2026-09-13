# Software

## Create the workspace

```bash
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
└── rob4_fraunhofer_ws/
    └── src/
        ├── curt_mini/
        ├── curtmini_piper/
        ├── curtmini_piper_gz_sim/
        └── piper_driver/
            ├── agx_arm_ros/
            └── agx_arm_urdf/
```

- [`project-docs`](https://github.com/2026-2027-ROB4-Fraunhofer/project-docs)
  contains the project-level setup and operating documentation.
- [`curtmini_piper_containers`](https://github.com/ipa-may/curtmini_piper_containers)
  contains the container images and Docker Compose services.
- `rob4_fraunhofer_ws` is the local ROS 2 colcon workspace. Its `src` directory
  contains:
  - [`curt_mini`](https://github.com/ipa-may/curt_mini), which provides the
    mobile-base description, hardware bringup, and teleoperation packages.
  - [`curtmini_piper`](https://github.com/ipa-may/curtmini_piper), which
    integrates the Curt Mini base with the Piper arm.
  - [`curtmini_piper_gz_sim`](https://github.com/ipa-may/curtmini_piper_gz_sim),
    which provides the Gazebo simulation.
  - `piper_driver`, which groups the Piper driver repositories:
    - [`agx_arm_ros`](https://github.com/ipa-may/agx_arm_ros) provides the ROS 2
      driver for the arm.
    - [`agx_arm_urdf`](https://github.com/ipa-may/agx_arm_urdf) provides the
      Piper robot description.

Choose either the source or Docker installation workflow:

```{toctree}
:maxdepth: 1

source
docker
```
