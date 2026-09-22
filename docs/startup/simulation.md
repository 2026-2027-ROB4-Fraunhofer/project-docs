# Simulation

Simulation is maintained in the
[curtmini_piper_gz_sim repository](https://github.com/ipa-may/curtmini_piper_gz_sim).

With the local workspace built:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```


Set `CONTAINER_ROS_DISTRO=jazzy` and `RMW=cyclonedds` in the container
repository's `.env`; see [container ROS distribution](../installation/software/docker.md#container-ros-distribution).
Jazzy is the default, including when the host shell uses ROS 2 Humble.

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
  -f compose.gui.yaml \
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
