# MoveItPy

Start [simulation](simulation.md) or [hardware bringup](real_hardware.md) first.
The example plans without executing by default.

## Docker

Run from the infrastructure repository, matching the backend's settings:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
export CONTAINER_ROS_DISTRO=jazzy
export RMW=cyclonedds
export ROS_DOMAIN_ID=42
export COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml
MOVEIT_PLAN_ONLY=true docker compose run --rm --build moveitpy-sim
```

To plan and execute in simulation:

```sh
MOVEIT_PLAN_ONLY=false docker compose run --rm --build moveitpy-sim
```

Use `moveitpy-hardware` for an active real robot. `MOVEIT_PLAN_ONLY=false` enables
execution there too.

For a previously built [local workspace](../installation/software/docker.md#local-workspace-development),
select its overlay before running the command:

```sh
export COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.workspace.yaml
```

## Native source workspace

Install `ros-jazzy-moveit-py` and source the built workspace. Plan in simulation:

```sh
ros2 run curtmini_piper_motion_examples moveit_goal --ros-args \
  -p controller_mode:=simulation -p use_sim_time:=true -p plan_only:=true
```

Set `plan_only:=false` to execute. For hardware, use `controller_mode:=hardware`
and `use_sim_time:=false`.
