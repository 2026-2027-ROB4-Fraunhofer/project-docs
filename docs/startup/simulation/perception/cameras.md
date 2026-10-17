# Cameras

## Prerequisites

- Complete [Docker installation](../../../installation/software/docker.md).
- Keep `SIM_USE_CAMERAS=true` in `.env`.

In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

## Start the cameras

Keep `SIM_USE_CAMERAS=true` in `.env`:

```sh
xhost +si:localuser:root
docker compose up --build gz-sim moveit-rviz-sim
```

In RViz, check the color and depth displays for both cameras. They should update as the robot moves.

## Stop

Stop the camera publishers by stopping [simulation](../bringup.md#stop).

See [camera topics and geometry](../../../explanation/cameras.md) for the stream reference and mount configuration.
