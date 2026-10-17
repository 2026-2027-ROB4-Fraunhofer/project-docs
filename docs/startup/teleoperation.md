# Teleoperating the base

Complete [Docker installation](../installation/software/docker.md) first.
In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

Start [simulation](simulation.md) or [the hardware base](real_hardware.md) first.
Cancel navigation goals and stop `nav2-sim` before driving manually.

## Simulation

```sh
docker compose run --rm --build keyboard-teleop-sim
```

## Hardware

With `base-bringup` running:

```sh
docker compose run --rm --build keyboard-teleop-hardware
```

## Drive and stop

Keep the terminal focused:

| Key | Action |
| --- | --- |
| `i` | Forward |
| `,` | Backward |
| `j` / `l` | Turn |
| `k` | Stop |

The base should respond to the keys. Press `k` before Ctrl+C to stop and exit the one-off container. This leaves the simulation or hardware backend running.

See [deployment architecture](../explanation/compose_project/system_deployment_architecture.md) for the simulation and hardware command paths.
