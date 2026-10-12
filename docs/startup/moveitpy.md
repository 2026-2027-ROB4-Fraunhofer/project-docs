# MoveItPy

Start [simulation](simulation.md) or [hardware bringup](real_hardware.md) first.
The example plans without executing by default.

## Docker

Use the same `curtmini_piper_containers/.env` as the backend; see
[configure once with `.env`](../installation/software/docker.md#configure-once-with-env).
Keep `compose.workspace.yaml` selected when using a previously built local
simulation workspace. Compose reads `.env` automatically in every terminal.

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
MOVEIT_PLAN_ONLY=true docker compose run --rm --build moveitpy-sim
```

To plan and execute in simulation:

```sh
MOVEIT_PLAN_ONLY=false docker compose run --rm --build moveitpy-sim
```

The value before the command overrides `.env` for that invocation only. To
keep a preference, set `MOVEIT_PLAN_ONLY` in `.env` instead.
Use `moveitpy-hardware` for an active real robot. `MOVEIT_PLAN_ONLY=false` enables
execution there too. See the [service guide](services.md) for related tools.

## Native source workspace

Install `ros-jazzy-moveit-py` and source the built workspace. Plan in simulation:

```sh
ros2 run curtmini_piper_motion_examples moveit_goal --ros-args \
  -p controller_mode:=simulation -p use_sim_time:=true -p plan_only:=true
```

Set `plan_only:=false` to execute. For hardware, use `controller_mode:=hardware`
and `use_sim_time:=false`.

Simulation containers pass `SIM_USE_HOKUYO` to the client robot model. For a
native launch, set `use_hokuyo:=false` (RViz launch argument) or
`-p use_hokuyo:=false` (MoveItPy parameter) when the simulator lidar is disabled.
The native defaults include the lidar for simulation and omit it for hardware.
