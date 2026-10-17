# Moving the arm with MoveItPy

## Prerequisites

- Complete [Docker installation](../../../installation/software/docker.md).
- Start MoveIt through the [first arm motion walkthrough](moveit_gui.md#start-moveit-and-rviz).
- Keep the backend running and finish any previous arm motion before sending a new goal.

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

## Plan

Optionally edit `curtmini_piper_tools/curtmini_piper_moveitpy_example/config/goal.yaml` for your goal. See [goal parameters](../../../explanation/moveit.md#goal-parameters).

```sh
MOVEIT_PLAN_ONLY=true docker compose run --rm --build moveitpy-sim
```

Look for `Planning succeeded`. The arm should stay still in plan-only mode.

## Execute

```sh
MOVEIT_PLAN_ONLY=false docker compose run --rm --build moveitpy-sim
```

The simulated arm should follow the trajectory. The example exits after its request finishes.

## Native source alternative

Install `ros-jazzy-moveit-py` and source the built workspace:

```sh
ros2 run curtmini_piper_moveitpy_example moveit_goal --ros-args \
  -p controller_mode:=simulation -p use_sim_time:=true -p plan_only:=true
```

Set `plan_only:=false` to execute.

## Finish

Let the one-shot request complete before stopping the backend through its startup page. Closing the client is not a documented motion-cancellation mechanism.

See [MoveIt APIs and arm control](../../../explanation/moveit.md) for planning, execution and controller details.
