# Teleoperating the base

## Prerequisites

- Complete [Docker installation](../../../installation/software/docker.md).
- [Start Gazebo](../bringup.md).

In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

## Drive

Cancel active navigation goals and stop Nav2 before driving manually:

```sh
docker compose stop nav2-sim
```

```sh
docker compose run --rm --build keyboard-teleop-sim
```

## Controls and stopping

Keep the terminal focused:

| Key | Action |
| --- | --- |
| `i` | Forward |
| `,` | Backward |
| `j` / `l` | Turn |
| `k` | Stop |

The base should respond to the keys. Press `k` before Ctrl+C to stop and exit the one-off container. This leaves the simulation backend running.

See [deployment architecture](../../../explanation/compose_project/system_deployment_architecture.md) for the simulation and hardware command paths.
