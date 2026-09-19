# Software

## Step 1 : Create the workspace

```bash
mkdir -p ~/ROB4_Fraunhofer
cd ~/ROB4_Fraunhofer
git clone git@github.com:2026-2027-ROB4-Fraunhofer/project-docs.git
vcs import . < project-docs/dependencies.repos
```

Vous devez avoir installe vcs tools:
```sh
sudo apt-get install python3-vcstool
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

## Step 2 : Install the software

Docker is required to run the Gazebo simulation, RViz, MoveItPy,
teleoperation, and hardware bringup.


If you have Ubuntu 24.04: you could install ROS 2 and the source dependencies on your host if you want to:

- Develop or modify ROS 2 packages
- Build packages locally
- Debug source code directly

I would not recommand doing that in the beginning. First get familiar with ROS 2 and use the provided containers. If you find limitation to the containers, don't hesitate to tell me.


For your development setup:

- If you’re using Ubuntu 24.04:
You can install ROS 2 directly on your host and develop your ROS 2 components there. This should be easier than containerizing the application from the start.

I’d still be very happy if you Dockerize the application at a later stage, but I completely understand if that feels like too much effort. You already have plenty on your plate for this project.

- If you don't have Ubuntu 24.04: 
Then Dockerizing the application is the only option. It’s good practice to do so anyway.


```{toctree}
:maxdepth: 1

docker
source
```
