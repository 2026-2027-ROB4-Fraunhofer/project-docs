# Moving the arm with MoveItPy

Start [simulation](simulation.md) or [hardware bringup](real_hardware.md) first.

Complete [Docker installation](../installation/software/docker.md) first.
In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

## Build the base image

Before the first MoveItPy image build:

```sh
docker compose build moveit-rviz-sim
```

The simulation and hardware RViz services share this image. Building it does not start RViz.

## Plan in simulation

Optionally edit `curtmini_piper_tools/curtmini_piper_moveitpy_example/config/goal.yaml` for your goal. See [goal parameters](../explanation/moveit.md#goal-parameters).

```sh
MOVEIT_PLAN_ONLY=true docker compose run --rm --build moveitpy-sim
```

Look for `Planning succeeded`. The arm should stay still in plan-only mode.

## Execute in simulation

```sh
MOVEIT_PLAN_ONLY=false docker compose run --rm --build moveitpy-sim
```

The simulated arm should follow the trajectory. The example exits after its request finishes.

## Hardware

Use `moveitpy-hardware` in place of `moveitpy-sim` with the hardware backend running. Start with `MOVEIT_PLAN_ONLY=true`; setting it to `false` commands the real arm.

## Native source alternative

Install `ros-jazzy-moveit-py` and source the built workspace:

```sh
ros2 run curtmini_piper_moveitpy_example moveit_goal --ros-args \
  -p controller_mode:=simulation -p use_sim_time:=true -p plan_only:=true
```

Set `plan_only:=false` to execute. For hardware use `controller_mode:=hardware` and `use_sim_time:=false`.

## Finish

Let the one-shot request complete before stopping the backend through its startup page. Closing the client is not a documented motion-cancellation mechanism.

See [MoveIt APIs and arm control](../explanation/moveit.md) for planning, execution and controller details.
