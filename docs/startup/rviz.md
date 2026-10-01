# Standalone RViz

RViz is a client. Start simulation or hardware bringup first; the backend provides
MoveIt, joint states, transforms, and the planning scene. The
[simulation quick start](simulation.md) already starts RViz.

## Docker

To start RViz separately, run from the infrastructure repository:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
export CONTAINER_ROS_DISTRO=jazzy
export RMW=cyclonedds
export ROS_DOMAIN_ID=42
export COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml
xhost +si:localuser:root
docker compose run --rm --build moveit-rviz-sim
```

Use `moveit-rviz-hardware` for an active real robot. Match the backend's distro,
middleware, ROS domain, and mount/TCP settings.

For a previously built [local workspace](../installation/software/docker.md#local-workspace-development),
select its overlay before running the RViz command:

```sh
export COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.workspace.yaml:compose.gui.yaml
```

## Native source workspace

After sourcing the installed workspace, run:

```sh
ros2 launch curtmini_piper_moveit_config moveit_rviz.launch.py use_sim_time:=true
```

Use `use_sim_time:=false` for real hardware.
