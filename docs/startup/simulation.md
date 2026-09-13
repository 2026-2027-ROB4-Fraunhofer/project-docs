# Simulation

Simulation is maintained in the
[curtmini_piper_gz_sim repository](https://github.com/ipa-may/curtmini_piper_gz_sim).

With the local workspace built, start Gazebo:

```bash
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
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
