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



## Using docker

Run the Compose commands from `curtmini_piper_containers/` with
`CONTAINER_ROS_DISTRO=jazzy` and `RMW=cyclonedds` in its `.env`; see
[container ROS distribution](../installation/software/docker.md#container-ros-distribution).
Jazzy is the default, independently of the host's ROS distro.

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

### Base only

### Arm + Base
Start both arm + base (use `real-bringup`)
```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.gui.yaml \
  up real-bringup moveit-rviz-hardware
```



## Using workspace packages (advanced)


Modify the joint limits.

Build the workspace
```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.workspace.yaml \
  run --rm workspace-builder
```


Run the container using local workspace packages:
```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.workspace.yaml \
  -f compose.gui.yaml \
  up --force-recreate piper-bringup moveit-rviz-hardware
```


```sh
CONTROL_ENABLED=true FAST_MODE=true docker compose   -f compose.yaml   -f compose.cyclonedds.yaml   -f compose.workspace.yaml   -f compose.gui.yaml down piper-bringup moveit-rviz-hardware

```


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

if control_enabled = false:
then the real Piper driver ignores commands.

If control_enabled = true: 
then the real Piper driver accepts commands.



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