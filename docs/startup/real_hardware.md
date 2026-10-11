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
MoveIt, and RViz. By default, `control_enabled=true` lets the Piper driver
accept commands continuously. With `control_enabled:=false`, bringup starts
the trajectory-status gate, which enables commands during an active trajectory.

For hardware-free MoveIt and RViz testing:

```bash
ros2 launch curtmini_piper_bringup bringup.launch.py \
  start_base:=false start_arm_hardware:=false
```



## Using docker

Run the Compose commands from `curtmini_piper_containers/` with
`CONTAINER_ROS_DISTRO=jazzy` and `RMW=cyclonedds` in its `.env`; see
[container ROS distribution](../installation/software/docker.md#container-ros-distribution).
Jazzy is the default, independently of the host's ROS distro. For RViz, allow
X11 access once per desktop session with `xhost +si:localuser:root`; the current
containers run as root.

```sh
sudo ip link set can0 up type can bitrate 1000000
```

Verify:
```sh
ip -details -statistics link show can0
```

### Arm only

Start only the arm (use `piper-bringup`)
```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.gui.yaml \
  up piper-bringup moveit-rviz-hardware
```

Stop it (or down)
```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.gui.yaml \
  down piper-bringup moveit-rviz-hardware
```

### Arm + Base
Start both arm + base (use `real-bringup`)
```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.gui.yaml \
  up real-bringup moveit-rviz-hardware
```



## Building local hardware changes

The workspace builder is for simulation, navigation and MoveIt examples. It does not build
hardware bringup or drivers, and `compose.workspace.yaml` does not override
hardware services. After editing the robot repository, rebuild its dedicated
hardware and RViz images:

```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.gui.yaml \
  build piper-bringup moveit-rviz-hardware
```

Then use the hardware startup commands above. For full arm and base bringup,
use `real-bringup` in place of `piper-bringup`.


## Infos


Moveit COntroller:

```text
/piper/arm_controller
```

Real Piper driver:
This is the thing that talks to the robot over CAN.

```text
/piper/agx_arm_ctrl_single_node
```

### About `control_enabled`

The driver accepts commands while its control gate is enabled. The default
launch setting `control_enabled=true` leaves it enabled continuously.

With `control_enabled:=false`, the driver starts disabled and bringup launches
`piper_control_gate`. That node enables the driver during an active trajectory
and disables it afterward; the launch setting is not a permanent command lock.



### About `fast_mode`

Parameter from the real Piper driver.


When the real driver receives commands, it can send them to the robot in two ways:
1. fast_mode = false
Uses:  `move_j` (go to this joint pose as a normal move)

2. fast_mode = true
Uses: `move_js` (stream joint setpoints continuously. )Since MoveIt sends many small trajectory points quickly, `fast_mode=true` may fit better.


So command path:
```text
RViz says:
  "Move to this target."

MoveIt sends the path to:
  /piper/arm_controller

/piper/arm_controller is fake-backed:
  it says "done" when the fake robot reaches the target.

Meanwhile, a bridge publishes those fake joint positions to:
  /piper/control/joint_states

The real Piper driver listens there:
  /piper/agx_arm_ctrl_single_node

But the real driver only acts if:
  control_enabled = true
```
