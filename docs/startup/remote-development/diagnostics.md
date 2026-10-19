# Diagnosing the running system

`ros-cli` is an interactive ROS Jazzy toolbox for hardware and simulation.
It includes controller and TF tools, RViz, PlotJuggler with ROS plugins,
`rqt_graph`, `rqt_console`, rosbag tools, and the Curt Mini/Piper descriptions
and meshes. It uses the deployment's ROS domain and middleware.

Run host commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

## Build and open the shell

Build once, and rebuild after changes to the diagnostic image. While the
changes are only in your local robot checkout, use:

```sh
CURTMINI_PIPER_IMAGE_SOURCE="$(realpath ../rob4_fraunhofer_ws/src/curtmini_piper)" \
  docker compose build ros-cli
```

This also builds its description-image dependency. See
[Development workflows](../development.md) for local versus published sources.

In `.env`, set `ROS_CLI_UID` and `ROS_CLI_GID` to the output of `id -u` and
`id -g`. Keep `ROS_CLI_OUTPUT_DIR=./diagnostics`, or create an alternative
directory owned by your user and set that path. Select the same middleware
overlay as the running system, then open a temporary shell:

```sh
docker compose run --rm ros-cli
```

ROS and the robot description workspace are already sourced. The shell can
start even when the robot backend is unavailable. With Zenoh, Compose starts
the configured router dependency when necessary.

For a persistent container and additional terminals:

```sh
docker compose up -d ros-cli
docker compose exec ros-cli bash
# When finished:
docker compose stop ros-cli
```

You can also run a single query from the host:

```sh
docker compose run --rm ros-cli \
  ros2 control list_controllers -c /piper/controller_manager
```

## Inspect ROS and controllers

Run these commands inside `ros-cli`:

```sh
ros2 node list
ros2 topic list -t
ros2 topic info /joint_states --verbose
ros2 topic echo /joint_states --once
ros2 topic hz /joint_states
```

Stop continuous commands with Ctrl+C. Inspect the arm controller manager:

```sh
ros2 control list_controllers -c /piper/controller_manager
ros2 control list_hardware_interfaces -c /piper/controller_manager
```

For Gazebo, use `-c /controller_manager`. These queries inspect the existing
manager; the diagnostic service does not launch a controller manager.
The Piper integration uses mock-backed controllers and a hardware bridge,
so an active controller is not proof of physical tracking. See
[Hardware command path](../../explanation/moveit.md#hardware-command-path).

For process startup errors, read logs from a separate **host** terminal:

```sh
docker compose logs --tail 150 piper-bringup
```

## Generate a TF tree PDF

Inside the container:

```sh
cd /diagnostics/tf
ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo base_link piper_tcp_link
ros2 run tf2_ros tf2_monitor base_link piper_tcp_link
```

`view_frames` listens briefly and writes its graph/PDF into the current
directory. Open the PDF from `diagnostics/tf/` on the host. The echo and
monitor commands run until interrupted.

## Open RViz and PlotJuggler

For a local Linux desktop, include `compose.gui.yaml` in `COMPOSE_FILE` and
run this on the **host desktop**, using the account selected by `ROS_CLI_UID`:

```sh
xhost +si:localuser:$(id -un)
```

Then enter `ros-cli` and run:

```sh
rviz2 -d /diagnostics/rviz/robot.rviz
```

The initial configuration displays RobotModel, TF and a grid, with `base_link`
as its fixed frame. It reads `/robot_description` from the backend and resolves
the meshes using the image's installed packages. It is copied into persistent
storage only when `robot.rviz` does not already exist.

Use RViz's **Save Config As** to save another configuration under
`/diagnostics/rviz/`, then reopen it with `rviz2 -d /diagnostics/rviz/<name>.rviz`.
The backend must publish the full robot description and the transforms for
the links you want to see. Running only the arm can leave base wheel TF absent.

For Gazebo, start RViz with simulation time:

```sh
rviz2 -d /diagnostics/rviz/robot.rviz --ros-args -p use_sim_time:=true
```

Open PlotJuggler:

```sh
ros2 run plotjuggler plotjuggler
```

Choose the **ROS2 Topic Subscriber** streaming plugin, select topics such as
`/joint_states`, and start streaming. Save the layout as
`/diagnostics/plotjuggler/joints.xml`. Reopen it through the layout controls or:

```sh
ros2 run plotjuggler plotjuggler --layout /diagnostics/plotjuggler/joints.xml
```

A layout stores the plot setup; keep recordings or exported data separately.
For the ROS graph and logs, run:

```sh
ros2 run rqt_graph rqt_graph
ros2 run rqt_console rqt_console
```

The GUI overlay defaults to software rendering for `ros-cli`. Add the existing
`compose.nvidia.yaml` overlay for NVIDIA rendering when the host has the
NVIDIA Container Toolkit. For a software-rendering fallback, omit that overlay
when starting the diagnostic service; other running containers can stay up.

## Save recordings and other files

The container's `/diagnostics` is the host's `diagnostics/` directory by default:

| Container folder | Saved content |
| --- | --- |
| `/diagnostics/tf` | TF PDFs and graph files |
| `/diagnostics/rviz` | RViz configurations |
| `/diagnostics/plotjuggler` | Plot layouts and exports |
| `/diagnostics/bags` | ROS recordings |
| `/diagnostics/home` | Application preferences and shell history |

Record selected topics inside the container, choosing a new output name each time:

```sh
ros2 bag record -o /diagnostics/bags/arm-session \
  /joint_states /tf /tf_static
```

Stop recording with Ctrl+C. For simulation-time recording, add `--use-sim-time`
and ensure Gazebo is publishing `/clock`. Files persist after `--rm` removes
the container and are ignored by Git. Load recordings through PlotJuggler's
ROS bag loader; saving a layout alone does not preserve the recorded samples.

## SSH access and troubleshooting

For terminal diagnostics, SSH to the robot host, change to
`curtmini_piper_containers`, and run the same shell command. GUI tools need a
display connection as well. The supplied GUI overlay uses the robot host's
X11 desktop; SSH alone does not make those windows appear on your laptop.
Use an existing remote desktop session to access that desktop.

- **No ROS nodes/topics:** check the backend is running and both sides use the
  same ROS domain and middleware. For Zenoh, check the router. Host networking
  connects to the host where Docker runs.
- **Controller query waits:** confirm the namespace; Piper uses
  `/piper/controller_manager`, while Gazebo uses `/controller_manager`.
- **RViz cannot load meshes:** check `ros2 pkg prefix agx_arm_urdf` and
  `ros2 pkg prefix curt_mini_description`. Rebuild `ros-cli` if it still uses
  the old teleop image or its assets differ from the backend.
- **Missing links or stale TF:** check `/joint_states`, `/tf`, `/tf_static`, the
  fixed frame, and hardware versus simulation time.
- **Qt/display errors:** check `DISPLAY`, the GUI overlay, and the host's X11
  authorization for the diagnostic user. Root authorization used by other
  project GUI services does not authorize this user.
- **Cannot save files:** check the UID/GID settings and host directory ownership.
  A custom output directory must exist before starting the service.
- **Planning fails:** read the MoveIt backend logs. Controller availability,
  valid joint bounds, and collision checks are separate conditions.
