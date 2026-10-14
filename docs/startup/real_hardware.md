# Real hardware

Source the workspace and activate the Piper CAN interface:

```bash
cd ~/ROB4_Fraunhofer/rob4_fraunhofer_ws
source install/setup.bash
bash src/piper_driver/agx_arm_ros/scripts/can_activate.sh
```

Start the Piper arm and MoveIt:

```bash
ros2 launch curtmini_piper_bringup bringup.launch.py
```

For the complete robot, start the Curt Mini base in a second terminal:

```bash
ros2 launch curt_mini_bringup robot_base.launch.py \
  publish_robot_description:=False
```

The Piper launch publishes the complete robot model. The base launch skips
its base-only model in this combination. For the base alone, use
`ros2 launch curt_mini_bringup robot_base.launch.py` with the default model
publisher. By default, `control_enabled=true` lets the Piper driver
accept commands continuously. With `control_enabled:=false`, bringup starts
the trajectory-status gate, which enables commands during an active trajectory.

For hardware-free MoveIt and RViz testing:

```bash
ros2 launch curtmini_piper_bringup bringup.launch.py \
  start_arm_hardware:=false
```



## Using Docker

Create `curtmini_piper_containers/.env` using the
[Docker setup](../installation/software/docker.md#configure-once-with-env).
For hardware with CycloneDDS and RViz, put these settings in the file:

```ini
CONTAINER_ROS_DISTRO=jazzy
RMW=cyclonedds
ROS_DOMAIN_ID=42
COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml
```

Compose reads `.env` automatically. In each terminal, run commands from
`curtmini_piper_containers/`; no repeated `-f` options or exports are needed.
If earlier shell exports override your file, follow the
[precedence instructions](../installation/software/docker.md#temporary-overrides-and-precedence).
See the [service guide](services.md) for the difference between bringup and RViz.

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
xhost +si:localuser:root
```

Allow X11 access once per desktop session; the GUI containers run as root.
Activate the CAN interface on the host before starting hardware:

```sh
sudo ip link set can0 up type can bitrate 1000000
```

Verify:

```sh
ip -details -statistics link show can0
```

### Arm only

Start only the arm (use `piper-bringup`):

```sh
docker compose up --build piper-bringup moveit-rviz-hardware
```

Stop these services from another terminal:

```sh
docker compose stop piper-bringup moveit-rviz-hardware
```

### Arm + Base

Start both arm and base as separate services:

```sh
docker compose up --build base-bringup piper-bringup moveit-rviz-hardware
```

`piper-bringup` publishes the complete robot model. Compose therefore sets
`PUBLISH_BASE_DESCRIPTION=False` for `base-bringup`. To run the base without
the Piper service, set `PUBLISH_BASE_DESCRIPTION=True` in `.env` or for that
command so the base publishes its own model.

### Two D435i cameras

The `realsense-base` and `realsense-tool` services start the two cameras by
serial number and publish their mount TFs. Measure the real mounts in
`curtmini_piper_sensors/config/camera_mounts.yaml`, then set
`BASE_CAMERA_SERIAL` and `TOOL_CAMERA_SERIAL` in `.env`. To start them with the
complete robot and RViz:

```sh
docker compose up --build base-bringup piper-bringup realsense-base realsense-tool moveit-rviz-hardware
```

See [Cameras](cameras.md) for the expected topics, native launch commands,
and the difference between simulated and physical mount configuration.



## Updating hardware images

Hardware images build from upstream `curtmini_piper/main`. After reviewed
changes reach that branch, refresh the
dedicated hardware and RViz images:

```sh
docker compose build --no-cache piper-bringup moveit-rviz-hardware
```

Then use the hardware startup commands above. For the complete robot, also
build and start `base-bringup`. For local hardware code changes,
use a [native source workspace](../installation/software/source.md).


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
