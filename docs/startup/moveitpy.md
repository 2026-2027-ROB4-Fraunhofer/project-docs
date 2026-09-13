# MoveItPy

Start simulation or real hardware bringup first. Planning does not execute by
default:

```bash
ros2 run curtmini_piper_motion_examples moveit_goal
```

Plan and execute in simulation:

```bash
ros2 run curtmini_piper_motion_examples moveit_goal --ros-args \
  -p controller_mode:=simulation \
  -p use_sim_time:=true \
  -p plan_only:=false
```

For real hardware, set `controller_mode:=hardware` and use
`use_sim_time:=false`.

With the Docker workspace:

```bash
MOVEIT_PLAN_ONLY=false docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.workspace.yaml \
  run --rm moveitpy-sim
```
