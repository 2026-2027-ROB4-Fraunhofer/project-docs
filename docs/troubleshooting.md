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
and lidar mounts. Containers bind-mount this config; restart bringup, RViz,
and motion clients after an edit. A native install without `--symlink-install`
also needs the description package rebuilt to update its installed copy.
The standard `gz-sim` image pins an older robot description that does not
read this YAML; see the
[simulator image caveat](installation/software/docker.md#robot-geometry-in-the-simulator-image).
