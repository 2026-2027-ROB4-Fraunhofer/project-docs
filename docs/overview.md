# Overview

This project integrates a Curt Mini mobile base, an AgileX Piper arm, MoveIt 2,
and Gazebo Harmonic. It supports source-based development and Docker Compose
workflows.

The main repositories are:

- [Curt Mini](https://github.com/ipa-may/curt_mini): base description,
  teleoperation, hardware bringup, and ROS 2 control integration.
- [Curt Mini Piper](https://github.com/ipa-may/curtmini_piper): combined robot
  description, MoveIt configuration, hardware bringup, camera launches,
  motion examples, and their Docker builds.
- [Gazebo simulation](https://github.com/ipa-may/curtmini_piper_gz_sim):
  simulation launch, controllers, sensors, worlds, and the Gazebo Docker build.
- [Containers](https://github.com/ipa-may/curtmini_piper_containers): Compose
  includes, shared middleware configuration, and workspace tooling.

The combined model prefixes Piper links and joints with `piper_`. Set the arm,
TCP, lidar, and simulated camera mounts in
`curtmini_piper_description/config/geometry.yaml`. Set measured physical camera
mounts in `curtmini_piper_sensors/config/camera_mounts.yaml`; see the
[camera guide](startup/cameras.md).
The simulation's starting base pose and six arm joint positions are separate
settings in `curtmini_piper_gz_sim/config/initial_state.yaml`.
