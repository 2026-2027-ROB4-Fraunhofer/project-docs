# System deployment architecture

The diagrams below describe the existing simulation services. Hardware deployment is still incomplete; its proposed layout is marked separately below. See [Compose services](compose_services.md) for the service catalog and [Startup and walkthrough](../../startup/index.md) for commands.

## Simulation: mapping

```mermaid
flowchart LR
    gz["gz-sim: Gazebo and controllers"] -->|"/scan, /base_controller/odom, /clock, TF"| slam["mapping-sim: SLAM Toolbox"]
    teleop["keyboard-teleop-sim"] -->|"/base_controller/cmd_vel"| gz
    slam -->|"map and map → odom"| rviz["nav2-rviz-sim"]
    gz -->|"scan and robot TF"| rviz
    slam --> saver["map_saver_cli"]
    saver --> maps["Host maps/: YAML and image"]
```

SLAM supplies `map → odom`; the simulated controller supplies `odom → base_link`. Manual driving provides the views needed to build the map. See [mapping](../../startup/mapping.md).

## Simulation: navigation

```mermaid
flowchart LR
    maps["Saved map"] --> nav["nav2-sim: map server, AMCL, Nav2"]
    gz["gz-sim"] -->|"scan, odometry, clock, TF"| nav
    rviz["nav2-rviz-sim"] -->|"initial pose and goal"| nav
    python["nav2-goal-client"] -->|"/navigate_to_pose"| nav
    nav -->|"/base_controller/cmd_vel"| gz
    nav -->|"map, localization, path"| rviz
```

AMCL replaces SLAM as the `map → odom` publisher. Stop mapping and keyboard driving before Nav2 drives. See [navigation](../../startup/navigation.md).

## Simulation: arm control

```mermaid
flowchart LR
    rviz["moveit-rviz-sim"] --> movegroup["move_group in gz-sim"]
    cpp["moveit-action-client-sim"] -->|"/move_action"| movegroup
    movegroup --> controller["arm_controller in gz-sim"]
    python["moveitpy-sim: local planning"] -->|"trajectory execution"| controller
    controller --> arm["Simulated arm"]
    state["Joint states and robot model"] --> python
    state --> movegroup
```

The C++ client delegates planning to `move_group`; MoveItPy plans in its own process. See [MoveIt APIs](../moveit.md).

## Simulation: arm control and navigation

One `gz-sim` backend supplies the arm and base controllers. Add the navigation services for base goals and the MoveIt clients for arm goals. The stacks do not provide coordinated mobile-manipulator planning: the Nav2 footprint is fixed and assumes the initial arm pose. An extended arm needs a reviewed footprint and clearance checks. See [Nav2 configuration](../navigation.md).

```mermaid
flowchart LR
    nav["nav2-sim"] --> base["Base controller in gz-sim"]
    clients["MoveIt clients"] --> arm["Arm controller in gz-sim"]
    gz["Gazebo state, sensors, clock"] --> nav
    gz --> clients
```

## Optional AprilTag detection

```mermaid
flowchart LR
    camera["Base camera in gz-sim"] -->|"image and camera_info"| detector["apriltag-base"]
    detector -->|"detections and tag TF"| pose["tag-pose-sim"]
    localization["SLAM or AMCL + robot TF"] --> pose
    pose -->|"/tag_pose_in_map"| exercise["User-written approach behavior"]
    exercise -.->|"chosen base goal"| nav["Nav2"]
```

The detector and pose tool exist. Selecting a reachable approach pose and implementing the approach behavior is the exercise; the project does not automatically drive to a detected tag. See [AprilTags](../apriltags.md).

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

## Hardware command routing

`keyboard-teleop-hardware` publishes `/cmd_vel` through the base command multiplexer. Simulation teleoperation instead publishes stamped commands directly to `/base_controller/cmd_vel`. Hardware arm control uses the [Piper driver path](../moveit.md#hardware-command-path).
