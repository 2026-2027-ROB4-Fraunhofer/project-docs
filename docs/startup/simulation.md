# Simulation

Simulation is maintained in the
[curtmini_piper_gz_sim repository](https://github.com/ipa-may/curtmini_piper_gz_sim).

With the local workspace built:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```


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
