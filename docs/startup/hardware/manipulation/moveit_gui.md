# MoveIt in RViz: first arm motion

Start the Piper MoveIt backend, preview an arm trajectory, and execute it on the real robot.

## Prerequisites

- Complete [Docker installation](../../../installation/software/docker.md).
- Complete [CAN and GUI preparation](../bringup.md#prepare-can-and-gui-access). Set `ARM_MODEL` in `.env` to match the installed Piper.
- Keep the base stationary and the arm workspace clear. The example below starts only the arm backend and RViz.

## Start MoveIt and RViz

Run this if the backend and RViz are not already running:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
xhost +si:localuser:root
docker compose up --build piper-bringup moveit-rviz-hardware
```

`piper-bringup` supplies MoveIt and the arm controller; `moveit-rviz-hardware` opens the GUI. If only RViz needs reopening, use [standalone RViz](../rviz.md).

Check startup logs for CAN/driver errors and confirm the displayed arm pose agrees with the physical arm before proceeding. Camera displays may stay empty unless [physical cameras](../perception/cameras.md) are running.

## Find the controls

The project loads `curtmini_piper_moveit_config/config/moveit.rviz`. It already enables **MotionPlanning**, robot/camera TF, and color/depth displays. Its fixed frame is `base_link`.

| GUI area | Use |
| --- | --- |
| Displays → MotionPlanning | Robot model, planning scene and trajectory display settings |
| MotionPlanning → Planning | Select planning group `arm` and use the planning/execution buttons |
| 3D view | Inspect the current robot, target pose and trajectory preview |

The model can also expose a gripper group; select `arm` for this walkthrough. See [MoveIt configuration](../../../explanation/moveit.md) for the backend and controller roles.

## Choose an arm target

Use the current robot state as the start. Enable **Query Goal State**, select **Interact**, and move the goal marker a small distance; the **Joints** tab is another way to adjust the target. These controls edit the requested goal.

## Plan and inspect

Click **Plan**. Inspect the preview before execution; a looping preview is animation, not commanded motion. If planning fails, check the reported error and choose a nearer reachable target. Keep the current start state and replan after any target or robot-state change.

## Execute

**Execute** runs a successful plan; **Plan & Execute** combines both steps. Use separate planning and execution for this first attempt.

**Clicking Execute commands the physical arm.** Check the actual workspace before clicking: only obstacles represented in the planning scene can be considered by the planner.

The current hardware controller is fake-backed. Inspect the physical outcome; a successful GUI result alone does not confirm the arm reached its target. See [hardware command path](../../../explanation/moveit.md#hardware-command-path).

`MOVEIT_PLAN_ONLY` configures the Python/C++ examples; it does not disable RViz execution buttons. No Python or C++ client is needed for this GUI exercise.

## Finish or continue

After the trajectory finishes, continue with [MoveItPy](moveitpy.md) or [C++](moveit_cpp.md), keeping the backend running. To end this session, press Ctrl+C in the startup terminal or run:

```sh
docker compose stop piper-bringup moveit-rviz-hardware
```

Closing RViz alone does not stop the backend or cancel an accepted motion.

For more GUI examples, see the [official MoveIt RViz tutorial](https://moveit.picknik.ai/main/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html). It uses a different robot; use this project's services and `arm` group here.
