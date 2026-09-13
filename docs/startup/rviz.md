# Standalone RViz

Start simulation or hardware bringup with RViz disabled, then run RViz as a
separate client.

For a source workspace:

```bash
# Simulation
ros2 launch curtmini_piper_moveit_config moveit_rviz.launch.py \
  use_sim_time:=true

# Real hardware
ros2 launch curtmini_piper_moveit_config moveit_rviz.launch.py \
  use_sim_time:=false
```

For the Docker workspace against an active simulation:

```bash
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.workspace.yaml \
  -f compose.gui.yaml \
  run --rm moveit-rviz-sim
```

The active backend must provide `move_group`, `/joint_states`, transforms, and
the planning scene.
