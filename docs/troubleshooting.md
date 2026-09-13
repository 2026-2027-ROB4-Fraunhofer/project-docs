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

Adjust the arm mount without editing the Xacro:

```bash
ros2 launch curtmini_piper_bringup bringup.launch.py \
  arm_mount_xyz:="0 0 0.20" arm_mount_rpy:="0 0 0"
```

Pass matching mount and TCP offsets to bringup, RViz, and motion clients.
