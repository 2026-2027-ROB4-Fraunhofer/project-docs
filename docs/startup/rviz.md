# Standalone RViz

RViz is a client. Start simulation or hardware bringup first; the backend provides
MoveIt, joint states, transforms, and the planning scene. The
[simulation quick start](simulation.md) already starts RViz.

## Docker

Use the same `curtmini_piper_containers/.env` as the backend; see
[configure once with `.env`](../installation/software/docker.md#configure-once-with-env).
Keep `compose.gui.yaml` in `COMPOSE_FILE` so RViz can open on the desktop.
Compose reads the file for every command, so no per-terminal exports are needed.

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
xhost +si:localuser:root
docker compose run --rm --build moveit-rviz-sim
```

Use `moveit-rviz-hardware` for an active real robot. Match the backend's distro,
middleware, ROS domain, and mount/TCP settings. This service displays MoveIt;
use `nav2-rviz-sim` for the [navigation view](navigation.md).
The MoveIt RViz configuration includes both camera bodies, TF, and color and
depth image displays. Follow the [camera guide](cameras.md) to start the
simulated or physical image publishers before opening those displays.
See the [service guide](services.md) for the available clients.

## Native source workspace

After sourcing the installed workspace, run:

```sh
ros2 launch curtmini_piper_moveit_config moveit_rviz.launch.py use_sim_time:=true
```

Use `use_sim_time:=false` for real hardware.

Simulation containers pass `SIM_USE_HOKUYO` to the client robot model. For a
native launch, set `use_hokuyo:=false` (RViz launch argument) or
`-p use_hokuyo:=false` (MoveItPy parameter) when the simulator lidar is disabled.
The native defaults include the lidar for simulation and omit it for hardware.
