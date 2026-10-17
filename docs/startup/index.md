# Startup and walkthrough

Complete [Installation](../installation/index.md) first. Start a simulation or the available hardware components, then choose a task below.
The full real-robot deployment is still being assembled; [deployment architecture](../explanation/compose_project/system_deployment_architecture.md) distinguishes current components from planned ones.

Compose commands run from `~/ROB4_Fraunhofer/curtmini_piper_containers` and use its `.env` file. Use the same ROS domain and middleware for all components.
For background, see [Explanation](../explanation/index.md); for general commands, see [Docker usage](../helpers/Tools/docker_usage.md).

```{toctree}
:maxdepth: 1
:caption: Startup

simulation
real_hardware
```

```{toctree}
:maxdepth: 1
:caption: Walkthroughs

mapping
navigation
teleoperation
moveitpy
moveit_cpp
cameras
apriltags
tag_pose
nav2_python
rviz
```

```{toctree}
:maxdepth: 1
:caption: Development and troubleshooting

development
troubleshooting
```
