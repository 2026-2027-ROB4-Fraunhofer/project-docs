# Nav2 configuration and interfaces

`curtmini_piper_navigation` configures **Nav2 for Gazebo simulation**. Nav2 plans a path and
drives the mobile base to a goal position and orientation. SLAM Toolbox builds
the map; AMCL estimates the robot's position on a saved map.

The package belongs in `curtmini_piper` because its frames, controller topics,
lidar and footprint are specific to this robot. Nav2 and SLAM Toolbox are
installed from ROS packages. They do not need separate source repositories.

## Files

| File | Purpose |
| --- | --- |
| `config/slam.yaml` | Lidar, frames and map-building settings |
| `config/nav2.yaml` | Localization, path planning, obstacle avoidance and speed limits |
| `launch/mapping.launch.py` | Starts SLAM Toolbox |
| `launch/navigation.launch.py` | Starts the map server, AMCL and Nav2 servers |
| `launch/rviz.launch.py` | Opens the navigation view |
| `rviz/navigation.rviz` | Map, scan, footprint, path and goal tools |
| `maps/` | Maps saved on the host; generated files are ignored by Git |

## How the pieces connect

| Interface | Used for |
| --- | --- |
| `/scan` (`sensor_msgs/msg/LaserScan`) | Mapping, localization and obstacle detection |
| `/base_controller/odom` | Wheel odometry for navigation |
| `/base_controller/cmd_vel` (`geometry_msgs/msg/TwistStamped`) | Base velocity commands |
| `/clock` | Simulation time for every navigation node |
| `/navigate_to_pose` | Goal action, including feedback and cancellation |
| `map → odom` | Published by SLAM while mapping, or AMCL while navigating |
| `odom → base_link` | Published by the simulated base controller |
| `base_link → … → hokuyo_link` | Published from the robot description |

NavFn plans the global path. DWB chooses local velocities while checking the
robot footprint against obstacles. The controller and recovery behaviors send
stamped commands directly to the base controller. Speed limits are configured in `config/nav2.yaml`. The current local file sets
`FollowPath.max_vel_x` to 2.25 m/s and `max_vel_theta` to 2.5 rad/s; other
velocity and acceleration settings also constrain motion. These are configuration
values, not measured robot speeds. Check the mounted file when tuning navigation.

The footprint is a fixed 1.0 × 0.7 m rectangle, plus 3 cm padding. It assumes
the stationary initial arm pose. Moving the arm does not automatically update
the footprint; an extended arm or changed attachments require a new footprint.
This is a 2D lidar setup and does not provide full 3D arm clearance checking.

## Saved maps

The [mapping walkthrough](../startup/mapping.md#save-the-map) creates `map.yaml` and `map.pgm` in `rob4_fraunhofer_ws/src/curtmini_piper/curtmini_piper_navigation/maps/` on
your host. `/maps` inside the container is a bind mount of that directory.
The files may be owned by root because the containers run as root.
The YAML records the image filename, map resolution and map origin. Keep both
files together.

The `nav2_map_server` map saver takes a filename prefix through `-f`. For example, `/maps/office` produces `office.yaml` and `office.pgm`.

## Lidar mounting

In RViz, the laser points should follow walls and furniture. If most points
land on the robot itself, correct the lidar mounting before mapping. Its
position is in `curtmini_piper_description/config/geometry.yaml`.

Changing only the lidar mount pose normally requires a TF/geometry update, not
new Nav2 parameters, while `/scan` and `hokuyo_link` keep their names. Check
an existing map again if the new height or tilt changes what the scan sees.

## Runtime configuration

The navigation services bind-mount the local `config/` directory. Restart affected services after changing `slam.yaml` or `nav2.yaml`; configuration edits do not require an image rebuild. The mapping and navigation services share the same image. Launch code changes require rebuilding that image.

Mapping and AMCL both publish `map → odom`; run one at a time. Keyboard teleoperation and Nav2 both command the simulated base; stop teleoperation before navigation.

See [mapping](../startup/mapping.md), [navigation](../startup/navigation.md), and [Python goals](../startup/nav2_python.md) for commands.

References: [Nav2 setup guide](https://docs.nav2.org/setup_guides/index.html) and [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox).
