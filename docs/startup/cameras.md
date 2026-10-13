# Cameras

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

## Run in Gazebo

Follow the [Docker setup](../installation/software/docker.md). For the regular
application images, which build robot and simulator code from upstream `main`,
set this in `curtmini_piper_containers/.env` and leave
`SIM_USE_CAMERAS=true` (the default):

```ini
COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml
SIM_USE_CAMERAS=true
```

From `curtmini_piper_containers/`, run:

```sh
xhost +si:localuser:root
docker compose up --build gz-sim moveit-rviz-sim
```

The MoveIt RViz view includes both camera bodies, TF, and color and depth image
displays. `SIM_USE_CAMERAS=false` disables the Gazebo camera sensors and their
camera TF publishers. The simulator's own worlds include the sensor systems
needed for images and IMU; other Gazebo worlds may need those systems added.
The regular image includes simulated cameras once their simulator code is on
upstream `main`; use the local workspace workflow to test simulator changes
before then. After upstream changes land, run
`docker compose build --no-cache gz-sim` once to refresh cached Git imports.
If you select `compose.workspace.yaml` instead, build `workspace-builder` first
as described in [local workspace development](../installation/software/docker.md#local-workspace-development).

## Run physical cameras

First configure the measured poses in `camera_mounts.yaml`. Add the **two
different device serial numbers** to `curtmini_piper_containers/.env`:

```ini
BASE_CAMERA_SERIAL=123456789
TOOL_CAMERA_SERIAL=987654321
```

Replace these examples with the serials of your cameras. With the hardware
`COMPOSE_FILE` selection from the [real hardware guide](real_hardware.md), run:

```sh
docker compose up --build real-bringup realsense-base realsense-tool moveit-rviz-hardware
```

The two RealSense services are independent; you can start either one on its
own. `real-bringup` supplies the robot's TF tree for RViz. Each camera launch
requires a serial number so both services cannot accidentally select the same
USB device. For a native Jazzy workspace, run one command in each of two
sourced terminals:

```sh
ros2 launch curtmini_piper_sensors realsense_camera.launch.py \
  camera:=base_camera serial_no:=_123456789
ros2 launch curtmini_piper_sensors realsense_camera.launch.py \
  camera:=tool_camera serial_no:=_987654321
```

Hardware image streams and physical mount calibration still require checking
on the installed robot. In RViz, verify that each image is live and that the
camera TF remains attached to the correct link while the arm moves.
