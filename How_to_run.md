# How to run

1. Running the gz simulation
2. Running the real hardware
3. Removing the container

## 1. Running the Gz Simulation

### Terminal 1: Start Gazebo

```sh
xhost +local:docker
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.workspace.yaml \
  -f compose.gui.yaml \
  up gz-sim moveit-rviz-sim
```

### Terminal #2: Start the keyboard_teleop

```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  run --rm keyboard-teleop-sim
```

### Terminal #3: Start RViZ + Moveit
Start Rviz + Moveit:
```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.workspace.yaml \
  -f compose.gui.yaml \
  run --rm -e LIBGL_ALWAYS_SOFTWARE=1 moveit-rviz-sim
```

### Terminal #4: Start MoveitPy

Run MoveItPy in another terminal:

```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.workspace.yaml \
  run --rm moveitpy-sim
```



## 2. Running the real robot


## 3. 