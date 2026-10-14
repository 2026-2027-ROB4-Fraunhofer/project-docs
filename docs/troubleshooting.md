# Troubleshooting

## Missing Curt Mini dependencies

Confirm that the hardware dependencies were imported:

```bash
colcon list | grep -E '^(candle_ros2|openzen_driver)[[:space:]]'
```

If either package is missing, repeat the nested `vcs import` commands from the
source installation page.

## Piper Python SDK

Before starting the real arm, verify that its SDK is available:

```bash
python3 -c "import pyAgxArm; print(pyAgxArm.__file__)"
```

## Mount and TCP offsets

Edit `curtmini_piper_description/config/geometry.yaml` to set the arm, TCP,
lidar, and simulated camera mounts. Containers bind-mount this config; restart
bringup, Gazebo, RViz, and motion clients that use it after an edit. A native
install without `--symlink-install` also needs the description package rebuilt
to update its installed copy. Regular Gazebo builds fetch robot code from
upstream `main`. For unpublished local URDF changes, use
[local workspace development](installation/software/docker.md#local-workspace-development).
Physical camera TF offsets are separate, in
`curtmini_piper_sensors/config/camera_mounts.yaml`, and must be measured on the
robot. See [Cameras](startup/cameras.md).

If only the lidar's position or orientation changes, update
`lidar_mount_on_base` in `geometry.yaml` and verify that `/scan` aligns with
walls in RViz. The current Nav2 and SLAM configurations use `/scan` and TF to
locate `hokuyo_link`; their parameters normally need no change while those
names stay the same. Revisit the navigation footprint if the new mount changes
the robot's outline, and check an existing map if the new scan plane sees a
different set of obstacles.
