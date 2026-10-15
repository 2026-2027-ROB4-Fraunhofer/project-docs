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

## Proposed real robot architecture

This diagram shows the intended roles of a development PC and the robot NUC.
The real robot navigation and localization components shown here are planned.


```mermaid
flowchart TB
    pc["Development PC: RViz, goal and task clients"]

    subgraph nuc["Robot NUC"]
        base["Base controller"] -->|/odometry/wheel| ekf["EKF"]
        imu["OpenZen IMU"] -->|IMU messages| ekf
        ekf --> filtered["/odometry/filtered"]
        ekf --> odom_tf["odom → base_link"]

        lidar["Lidar driver"] -->|/scan| localization["SLAM or AMCL"]
        localization --> map_tf["map → odom"]
        lidar -->|/scan| costmaps["Nav2 costmaps"]

        nav2["Nav2"] -->|/cmd_vel| mux["twist_mux"]
        mux --> base
        base --> wheels["Wheels"]

        moveit["MoveIt"] -->|trajectory requests| piper["Piper driver/controllers"]
        cameras["Two RealSense drivers"] --> data["Images, depth, camera IMUs"]
    end

    pc -.->|ROS 2| nav2
    pc -.->|ROS 2| moveit
```


## Deployment by host

```mermaid
flowchart LR
    subgraph pc["Development PC"]
        rviz["moveit-rviz-hardware"]
        action["moveit-action-client-hardware"]
        python["moveitpy-hardware"]
        teleop["keyboard-teleop-hardware"]
        goal["nav2-goal-client"]
    end

    subgraph nuc["Robot NUC"]
        base["base-bringup<br/>base, joystick, IMU"]
        piper["piper-bringup<br/>Piper driver and MoveIt server"]
        base_camera["realsense-base<br/>base D435i"]
        tool_camera["realsense-tool<br/>tool D435i"]
        tags["apriltag-base<br/>optional"]
        lidar["lidar-bringup<br/>planned"]
        ekf["state-estimation-real<br/>planned"]
        mapping["mapping-real<br/>planned"]
        nav["nav2-real<br/>planned"]
    end

    rviz -->|MoveIt UI| piper
    action -->|/move_action| piper
    python -->|MoveIt requests| piper
    teleop -->|/cmd_vel| base
    goal -.->|navigation goal| nav

    base_camera -->|images| tags
    base -->|wheel odometry and IMU| ekf
    lidar -.->|/scan| mapping
    lidar -.->|/scan| nav
    ekf -.->|filtered odometry| mapping
    ekf -.->|filtered odometry| nav
    nav -.->|/cmd_vel| base
```

`mapping-real` and `nav2-real` are planned alternatives for different phases; run one at a time.

**`mapping-real`** would run SLAM Toolbox on the NUC. It would use lidar scans
and the EKF's odometry to build a map, publish `map → odom`, and save the map
for later use. The robot would be driven manually during mapping.

**`nav2-real`** would load that saved map and run AMCL plus Nav2's planning and
driving components. AMCL would use the map and lidar scans to localize the
robot. After an initial pose is set, Nav2 could accept goals and send
`/cmd_vel` through the base's `twist_mux`. The lidar driver and EKF would keep
running in both phases.
