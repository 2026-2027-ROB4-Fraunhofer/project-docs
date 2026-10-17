# Cameras

## Prerequisites

- Complete [Docker installation](../../../installation/software/docker.md).
- Connect the two D435i cameras and note their serial numbers.
- Complete [hardware preparation](../bringup.md#prepare-can-and-gui-access) before starting the arm backend.

In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

## Configure the cameras

First measure the camera mounts and update `curtmini_piper_sensors/config/camera_mounts.yaml`; the supplied mount values are provisional. See [mounts and TF](../../../explanation/cameras.md#camera-mounts-and-tf).
Add two different device serial numbers to `.env`:

```ini
BASE_CAMERA_SERIAL=123456789
TOOL_CAMERA_SERIAL=987654321
```

Replace the examples with your device serials. After [hardware preparation](../bringup.md#prepare-can-and-gui-access):

```sh
docker compose up --build base-bringup piper-bringup \
  realsense-base realsense-tool moveit-rviz-hardware
```

Check that both images are live and the tool camera frame follows the arm. Physical image streams and calibration still need verification on the installed robot.
Either RealSense service can run independently; the robot backend supplies the robot TF tree.

## Native source alternative

Run one command in each of two sourced Jazzy terminals, replacing the serials:

```sh
ros2 launch curtmini_piper_sensors realsense_camera.launch.py \
  camera:=base_camera serial_no:=_123456789
```

```sh
ros2 launch curtmini_piper_sensors realsense_camera.launch.py \
  camera:=tool_camera serial_no:=_987654321
```

## Stop

Stop physical camera services with:

```sh
docker compose stop realsense-base realsense-tool
```

Stop any additionally started hardware services through [hardware startup](../bringup.md#stop). Native camera launches stop with Ctrl+C.

See [camera topics and geometry](../../../explanation/cameras.md) for the stream reference and calibration details.
