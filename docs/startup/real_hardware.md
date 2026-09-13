# Real hardware

Source the workspace and activate the Piper CAN interface:

```bash
cd ~/ROB4_Fraunhofer/rob4_fraunhofer_ws
source install/setup.bash
bash src/piper_driver/agx_arm_ros/scripts/can_activate.sh
```

Start the Piper arm and Curt Mini base:

```bash
ros2 launch curtmini_piper_bringup bringup.launch.py
```

Start only the Piper arm:

```bash
ros2 launch curtmini_piper_bringup bringup.launch.py start_base:=false
```

By default, bringup starts the base hardware, joystick, IMU, Piper arm,
MoveIt, and RViz. The command interface is enabled only while the trajectory
action is active.

For hardware-free MoveIt and RViz testing:

```bash
ros2 launch curtmini_piper_bringup bringup.launch.py \
  start_base:=false start_arm_hardware:=false
```
