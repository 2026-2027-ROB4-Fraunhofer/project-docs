# Standalone RViz

## Prerequisites

- Complete [Docker installation](../../installation/software/docker.md).
- Start [the arm backend](bringup.md#start-the-arm).
- Skip this page if the required RViz window is already running.

For the GUI introduction, use [MoveIt in RViz: first arm motion](manipulation/moveit_gui.md).

In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

## Docker

Keep `compose.gui.yaml` in `.env`'s `COMPOSE_FILE` and use the backend's ROS domain and middleware:

```sh
xhost +si:localuser:root
docker compose run --rm --build moveit-rviz-hardware
```

The MoveIt view should display the robot and planning panel. Start [cameras](perception/cameras.md) to populate its image displays.

## Native source alternative

After sourcing the installed workspace, match `arm_model` to the backend (the example uses `piper_x`):

```sh
ros2 launch curtmini_piper_moveit_config moveit_rviz.launch.py arm_model:=piper_x use_sim_time:=false
```

## Stop

Close RViz or press Ctrl+C in its terminal. The backend remains running.
See [Compose services](../../explanation/compose_project/compose_services.md) for the roles of RViz and the backend.
