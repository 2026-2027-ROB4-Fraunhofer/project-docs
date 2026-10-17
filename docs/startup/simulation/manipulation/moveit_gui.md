# MoveIt in RViz: first arm motion

Start the simulated robot and MoveIt, preview an arm trajectory, and execute it in Gazebo.

## Prerequisites

- Complete [Docker installation](../../../installation/software/docker.md).
- Use the regular-image `.env` settings from installation. Keep the base stationary and finish any navigation or teleoperation task before moving the arm.

## Start MoveIt and RViz

Run this if the backend and RViz are not already running:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
xhost +si:localuser:root
docker compose up --build gz-sim moveit-rviz-sim
```

`gz-sim` supplies MoveIt and the arm controller; `moveit-rviz-sim` opens the GUI. If only RViz needs reopening, use [standalone RViz](../rviz.md).

Gazebo should show the robot. If the arm state is missing, run the [controller check](../bringup.md#check-the-controllers) before planning.

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

Click **Execute** and watch the arm move in Gazebo. The scene robot in RViz should update as joint states arrive. If only the preview moves, inspect the controller status and execution result.

`MOVEIT_PLAN_ONLY` configures the Python/C++ examples; it does not disable RViz execution buttons. No Python or C++ client is needed for this GUI exercise.

## Finish or continue

After the trajectory finishes, continue with [MoveItPy](moveitpy.md) or [C++](moveit_cpp.md), keeping the backend running. To end this session, press Ctrl+C in the startup terminal or run:

```sh
docker compose stop gz-sim moveit-rviz-sim
```

Closing RViz alone does not stop the backend or cancel an accepted motion.

For more GUI examples, see the [official MoveIt RViz tutorial](https://moveit.picknik.ai/main/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html). It uses a different robot; use this project's services and `arm` group here.
