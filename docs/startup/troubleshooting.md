# Troubleshooting

## Missing Curt Mini dependencies

Confirm that the hardware dependencies were imported:

```bash
colcon list | grep -E '^(candle_ros2|openzen_driver)[[:space:]]'
```

If either package is missing, repeat the nested `vcs import` commands from the
[source installation page](../installation/software/source.md).

## Piper Python SDK

Before starting the real arm, verify that its SDK is available:

```bash
python3 -c "import pyAgxArm; print(pyAgxArm.__file__)"
```

## Mount and TCP offsets

Check the mount values in `curtmini_piper_description/config/geometry.yaml`, then restart the affected robot, simulator and clients. Physical camera mounts use `curtmini_piper_sensors/config/camera_mounts.yaml`.
See [geometry and rebuild behavior](../explanation/cameras.md#robot-mount-and-tcp-offsets) before changing offsets.

## Simulation controllers

```sh
docker compose exec gz-sim /opt/container/ros_entrypoint.sh ros2 control list_controllers
docker compose logs --tail 120 gz-sim
```

All three controllers should be active. If `joint_state_broadcaster` is inactive, inspect the spawner output; MoveIt needs current `/joint_states`. See [controller behavior](../explanation/simulation.md#controller-and-moveit-checks).

## Mapping and navigation

- **Gazebo shows only a ground plane:** `curtmini_piper` is the simple world.
  Set `SIM_WORLD=curtmini_piper_map` in the actual `.env` file, then rerun the
  [mapping startup command](mapping.md#start-mapping). The one-command prefix also selects it.
- **Map does not exist:** save a map first and check `maps/map.yaml`, or set
  `NAV2_MAP` to the saved YAML filename.
- **RViz has no `map` frame during localization:** provide a 2D Pose Estimate.
- **Scan does not line up:** check the initial pose, lidar geometry and TF.
- **Robot does not move:** inspect `docker compose logs nav2-sim`, check Nav2
  is active, and select a goal in mapped free space with room for the footprint.
- **Transform or time errors:** keep the same ROS domain and middleware in
  all terminals; all navigation nodes must use the simulator clock.

## GUI or environment settings

If RViz reports a Qt `xcb` error, check that `compose.gui.yaml` is selected and run `xhost +si:localuser:root` in the desktop session.
If `.env` changes appear ignored, check [shell precedence](../explanation/compose_project/environment.md#temporary-overrides-and-precedence), then recreate affected services. Editing `.env` alone does not restart them.

For service inspection and logs, see [Docker usage](../helpers/Tools/docker_usage.md).
