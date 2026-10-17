# Sending a Nav2 goal from Python

## Prerequisites

Start [navigation](navigation.md) and initialize AMCL in RViz first. Exit keyboard teleoperation before sending a goal.

Complete [Docker installation](../../../installation/software/docker.md) first.
In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

## Send a goal

Replace the example coordinates with a reachable location in your map:

```sh
docker compose run --rm --build nav2-goal-client \
  ros2 run curtmini_piper_nav_examples nav_to_pose 1.0 0.0 0.0 \
  --ros-args -p use_sim_time:=true
```

The numbers are `x`, `y` in metres and yaw in radians in `map`. The client waits for Nav2, prints the result and exits. The base should follow the planned path.

## Cancel and finish

Press Ctrl+C in this Python client to request cancellation. Stop navigation using [its stop commands](navigation.md#stop) when finished.

## Optional ROS CLI alternative

You can also send a goal through the ROS action interface:

```bash
docker compose exec nav2-sim /opt/container/ros_entrypoint.sh \
  ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  '{pose: {header: {frame_id: map}, pose: {position: {x: 1.0, y: 0.0}, orientation: {w: 1.0}}}}' \
  --feedback
```

Those coordinates are an example, not a known free point in your map. Choose
coordinates from RViz. The orientation is a quaternion; `w: 1.0` means yaw zero.
Closing the CLI is not a reliable way to cancel an accepted goal. RViz's
Cancel button is for goals sent from RViz. To cancel the active navigation
goal from a terminal:

```bash
docker compose exec nav2-sim /opt/container/ros_entrypoint.sh \
  ros2 service call /navigate_to_pose/_action/cancel_goal \
  action_msgs/srv/CancelGoal '{}'
```

The empty request asks Nav2 to cancel all current NavigateToPose goals.

See [navigation interfaces](../../../explanation/navigation.md#how-the-pieces-connect) for the action, topics and TF requirements.
