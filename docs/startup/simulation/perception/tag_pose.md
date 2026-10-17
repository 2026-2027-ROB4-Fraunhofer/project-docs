# Observing a tag in the map

## Prerequisites

- Have a saved map of the simulation environment: follow [Mapping](../navigation/mapping.md#save-the-map).
- Have Gazebo running with cameras and AprilTags enabled, and `apriltag-base` publishing detections: follow [Finding AprilTags](apriltags.md).
- Have `nav2-sim` running with that saved map: follow [Start localization and navigation](../navigation/navigation.md#start-localization-and-navigation), then [Set the initial pose](../navigation/navigation.md#set-the-initial-pose).
- Keep `mapping-sim` stopped while Nav2 localization is running.

Prepare these in this order: save a map, start the tag-enabled simulation, then start Nav2 and initialize AMCL. Keep that Gazebo session running; changing the world or restarting Gazebo afterward requires checking localization again. No navigation goal is needed to observe a tag pose.

In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

## Start the pose tool

```sh
docker compose up --build tag-pose-sim
```

In another terminal, inspect the result:

```sh
docker compose exec tag-pose-sim /opt/container/ros_entrypoint.sh \
  ros2 topic echo /tag_pose_in_map
```

Expect a `PoseStamped` in `map` while tag 0 is freshly observed. To select another tag:

```sh
TAG_FRAME=tag36h11:1 docker compose up tag-pose-sim
```

The output is the tag's pose. Choose a separate reachable base goal before using the [Python Nav2 client](../navigation/nav2_python.md).

## Stop

Stop the echo and pose-tool terminals with Ctrl+C, or run:

```sh
docker compose stop tag-pose-sim
```

Stop navigation and AprilTag services using their walkthroughs when finished.
See [pose transforms and freshness](../../../explanation/apriltags.md#camera-and-map-frames) for details.
