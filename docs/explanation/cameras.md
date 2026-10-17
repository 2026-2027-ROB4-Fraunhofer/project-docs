# Cameras and robot geometry

The robot has two camera positions: `base_camera` on `chassis`, below the lidar,
and `tool_camera` on `piper_tcp_link`, at the end effector. Gazebo models them as
D435i-like RGBD cameras with IMUs. On hardware, `curtmini_piper_sensors` starts
two physical D435i devices, selected by serial number.

Both setups publish color and depth images, camera information, and IMU data
under `/base_camera` and `/tool_camera`. For example:

| Stream | Base topic | Tool topic |
| --- | --- | --- |
| Color | `/base_camera/color/image_raw` | `/tool_camera/color/image_raw` |
| Depth | `/base_camera/depth/image_rect_raw` | `/tool_camera/depth/image_rect_raw` |
| Color calibration | `/base_camera/color/camera_info` | `/tool_camera/color/camera_info` |
| Depth calibration | `/base_camera/depth/camera_info` | `/tool_camera/depth/camera_info` |
| IMU | `/base_camera/imu` | `/tool_camera/imu` |

The Gazebo cameras provide simulated streams; their images and calibration do
not reproduce every property of a physical D435i.

## Camera mounts and TF

Gazebo reads both mount poses from
`curtmini_piper_description/config/geometry.yaml`. Its launch publishes static
mount transforms from `chassis` to `base_camera_link` and from
`piper_tcp_link` to `tool_camera_link`, plus optical-frame transforms. The
camera bodies in the robot model use the same geometry values. Restart Gazebo
and RViz after editing the YAML.

Physical camera mounts are configured separately in
`curtmini_piper_sensors/config/camera_mounts.yaml`. Its supplied poses are
**provisional**: measure both mounts on the real robot before using their TFs.
Each camera service publishes its robot-to-camera static transform; the
RealSense driver publishes the camera's internal frames. The tool camera's
mount is static relative to `piper_tcp_link`, so it follows the moving arm.
Keep the robot model's camera body placement in `geometry.yaml` aligned with
the measured hardware mount if you want RViz's camera body to match the device.
Restart the camera services after changing `camera_mounts.yaml`; the config is
bind-mounted, so the sensor image does not need rebuilding for pose changes.

## Simulation sensor availability

`SIM_USE_CAMERAS=false` disables the Gazebo camera sensors and their camera TF publishers. The simulator worlds include the sensor systems needed for images and IMU; other worlds may need these systems added.

See [camera startup](../startup/cameras.md) for commands and stream checks, and [image builds](compose_project/image_builds.md#robot-geometry-in-the-simulator-image) for restart versus rebuild behavior.

## Robot mount and TCP offsets

Edit `curtmini_piper_description/config/geometry.yaml` to set the arm, TCP,
lidar, and simulated camera mounts. Containers bind-mount this config; restart
bringup, Gazebo, RViz, and motion clients that use it after an edit. A native
install without `--symlink-install` also needs the description package rebuilt
to update its installed copy. Regular Gazebo builds fetch robot code from
upstream `main`. For unpublished local URDF changes, use
[local workspace development](../startup/development.md#local-workspace-development).
Physical camera TF offsets are separate, in
`curtmini_piper_sensors/config/camera_mounts.yaml`, and must be measured on the
robot. See [Cameras](../startup/cameras.md).

If only the lidar's position or orientation changes, update
`lidar_mount_on_base` in `geometry.yaml` and verify that `/scan` aligns with
walls in RViz. The current Nav2 and SLAM configurations use `/scan` and TF to
locate `hokuyo_link`; their parameters normally need no change while those
names stay the same. Revisit the navigation footprint if the new mount changes
the robot's outline, and check an existing map if the new scan plane sees a
different set of obstacles.
