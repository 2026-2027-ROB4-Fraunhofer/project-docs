# Standalone RViz

Start [simulation](simulation.md) or [hardware bringup](real_hardware.md) first. Skip this page if the required RViz window is already running.

Complete [Docker installation](../installation/software/docker.md) first.
In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

## Docker

Keep `compose.gui.yaml` in `.env`'s `COMPOSE_FILE` and use the backend's ROS domain and middleware:

```sh
xhost +si:localuser:root
docker compose run --rm --build moveit-rviz-sim
```

For the real robot, use `moveit-rviz-hardware`. For mapping or navigation, use `nav2-rviz-sim`.
The MoveIt view should display the robot and planning panel. Start [cameras](cameras.md) to populate its image displays.

## Native source alternative

After sourcing the installed workspace:

```sh
ros2 launch curtmini_piper_moveit_config moveit_rviz.launch.py use_sim_time:=true
```

Use `use_sim_time:=false` for real hardware. If the simulated lidar is disabled, also pass `use_hokuyo:=false` to match its model.

## Stop

Close RViz or press Ctrl+C in its terminal. The backend remains running.
See [Compose services](../explanation/compose_project/compose_services.md) for the roles of RViz and the backend.
