# Simulation

##
Simulation is maintained in the
[curtmini_piper_gz_sim repository](https://github.com/ipa-may/curtmini_piper_gz_sim).

With the local workspace built:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

Set some environment variables:
```sh
export CONTAINER_ROS_DISTRO=jazzy
export RMW=cyclonedds
export COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.gui.yaml
export SIM_WORLD=curtmini_piper_map
```

See [container ROS distribution](../installation/software/docker.md#container-ros-distribution).
Jazzy is the default, including when the host shell uses ROS 2 Humble or another distro.

Then run on Terminal #1:
```sh
docker compose up --build gz-sim moveit-rviz-sim
```

and on Terminal #2:
```sh
docker compose -f compose.yaml -f compose.cyclonedds.yaml \
  run --rm --build keyboard-teleop-sim
```


## Give the gz sim world:

Start gazebo + rviz
Empty map:
```sh
SIM_WORLD=curtmini_piper docker compose up --build gz-sim moveit-rviz-sim
```

With furnitures:
```sh
SIM_WORLD=curtmini_piper_map docker compose up --build gz-sim moveit-rviz-sim
```

## Some explanations

The COMPOSE_FILE environment allows
Gazebo:
```sh
xhost +local:docker
  docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.gui.yaml \
  up gz-sim
```

Moveit:
```sh
    docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.gui.yaml \
  up moveit-rviz-sim
```


Teleop:
```sh
   docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  up keyboard-teleop-sim
```


## Do not read that
Start Gazebo

```sh
xhost +local:docker
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.workspace.yaml \
  -f compose.gui.yaml \
  up gz-sim
```

Start RViz or MoveItPy in separate terminals using the instructions on their
respective pages.
