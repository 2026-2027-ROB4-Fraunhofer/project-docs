# Hardware startup

The full robot deployment is not complete. These commands start the available arm, base and camera components; real-robot mapping and navigation remain planned. See [deployment architecture](../../explanation/compose_project/system_deployment_architecture.md#proposed-real-robot-architecture).

Complete [Docker installation](../../installation/software/docker.md) first.
In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

## Prepare CAN and GUI access

On the hardware host, activate the arm's CAN interface (replace `can0` if your configuration uses another interface):

```sh
sudo ip link set can0 up type can bitrate 1000000
ip -details -statistics link show can0
xhost +si:localuser:root
```

Confirm the interface is up. Check that the base's configured IMU and joystick devices exist before starting `base-bringup`; see [hardware settings](../../explanation/compose_project/environment.md#hardware-settings).

## Start the arm

```sh
docker compose up --build piper-bringup moveit-rviz-hardware
```

RViz should show the combined robot and MoveIt panel. Check startup logs for CAN or driver errors before sending a motion request.

## Start arm and base together

Use this command instead of the arm-only command:

```sh
docker compose up --build base-bringup piper-bringup moveit-rviz-hardware
```

## Start the base

Check the configured IMU and joystick devices from [hardware settings](../../explanation/compose_project/environment.md#hardware-settings). Arm CAN preparation is only needed when also starting the Piper. For the base alone:

```sh
PUBLISH_BASE_DESCRIPTION=True docker compose up --build base-bringup
```

To add the cameras, follow [Cameras](perception/cameras.md#configure-the-cameras). Use [teleoperation](navigation/teleoperation.md#drive) for manual base driving, or start with [MoveIt in RViz](manipulation/moveit_gui.md) before [MoveItPy](manipulation/moveitpy.md) and [C++](manipulation/moveit_cpp.md) for arm goals.

## Stop

Stop teleoperation and finish or cancel active motion tasks before stopping the backend. Press Ctrl+C in the startup terminal, or run:

```sh
docker compose stop base-bringup piper-bringup moveit-rviz-hardware
```

If cameras are running, stop them using the [camera walkthrough](perception/cameras.md#stop).

## Native source alternative

After [source installation](../../installation/software/source.md), run:

```sh
cd ~/ROB4_Fraunhofer/rob4_fraunhofer_ws
source install/setup.bash
bash src/piper_driver/agx_arm_ros/scripts/can_activate.sh
ros2 launch curtmini_piper_bringup bringup.launch.py
```

In another sourced terminal, add the base:

```sh
ros2 launch curt_mini_bringup robot_base.launch.py publish_robot_description:=False
```

For the base alone, omit `publish_robot_description:=False`. For hardware-free arm testing, replace the Piper launch with:

```sh
ros2 launch curtmini_piper_bringup bringup.launch.py start_arm_hardware:=false
```

Stop native launches with Ctrl+C. See [MoveIt and driver behavior](../../explanation/moveit.md#hardware-command-path) for `control_enabled` and `fast_mode`, and [development workflows](../development.md) to refresh hardware images.
