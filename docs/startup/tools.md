# Tools and examples

The separate `curtmini_piper_tools` repository holds student-facing ROS
applications. The robot repository supplies bringup and server configuration;
the tools call those running services.

| ROS package | Command | Uses |
| --- | --- | --- |
| `curtmini_piper_moveitpy_example` | `moveit_goal` | MoveIt for Piper arm goals |
| `curtmini_piper_moveit_action_client_example` | `moveit_action_client_example` | C++ client for a running Piper MoveIt server |
| `curtmini_piper_tag_tools` | `tag_pose_in_map` | tf2 for an observed tag pose in `map` |
| `curtmini_piper_nav_examples` | `nav_to_pose` | Nav2 for a mobile-base goal |

Each package has its own dependencies. The MoveItPy example is documented in
the [MoveItPy guide](moveitpy.md).

## Send an arm goal through MoveIt

Start `gz-sim`, then edit
`curtmini_piper_tools/curtmini_piper_moveit_action_client_example/config/goal.yaml`.
From `curtmini_piper_containers/`, request a plan:

```sh
docker compose run --rm --build moveit-action-client-sim
```

The C++ client sends the goal to the running `move_group`. Its default is
planning only; set `MOVEIT_PLAN_ONLY=false` to execute. For the real Piper,
start `piper-bringup` and use `moveit-action-client-hardware`.

## Observe a tag in the map

First start Gazebo and the AprilTag detector as described in the
[AprilTag exercise](apriltags.md). Run `mapping-sim` while making a map, or
`nav2-sim` with a saved map, so `map → odom` exists. Then start the tool:

```sh
docker compose up tag-pose-sim
```

It looks up the detector's `tag36h11:0` frame through the robot's camera TF
chain and publishes `/tag_pose_in_map` as a `PoseStamped`. Set `TAG_FRAME` to
another observed frame before starting the service to inspect a different tag.
The output stops when the tag observation is too old. The tool uses camera
observations; it does not read the panels' Gazebo world coordinates.

The result is the **tag pose**. The student task is to select a safe base pose
near it, with enough space for the robot footprint and a heading facing the
panel.

## Request a Nav2 goal from Python

Start `nav2-sim` and initialize AMCL in RViz first. From
`curtmini_piper_containers/`, request an example map-frame goal:

```sh
docker compose run --rm nav2-goal-client \
  ros2 run curtmini_piper_nav_examples nav_to_pose 1.0 0.0 0.0 \
  --ros-args -p use_sim_time:=true
```

The three numbers are `x` and `y` in metres and yaw in radians. Replace them
with a reachable location from **your** map. The client waits for Nav2,
prints the result, and cancels on Ctrl+C. It sends a goal request; Nav2
handles planning and base velocity commands.

With the optional workspace overlay, run `workspace-builder` after editing
these local packages and restart their services. Regular tools images build
from the tools repository's published `main` branch. The repository's own
Sphinx guide documents the Python API and parameters.
