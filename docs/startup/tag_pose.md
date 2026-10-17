# Observing a tag in the map

Start [AprilTag detection](apriltags.md) first. Keep the same Gazebo session running.

Complete [Docker installation](../installation/software/docker.md) first.
In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

## Provide a map frame

Choose one mode. To build a map in the current tag-enabled world:

```sh
docker compose stop nav2-sim
docker compose up --build -d mapping-sim nav2-rviz-sim
```

Drive and save using the [mapping walkthrough](mapping.md#drive-around); skip its Gazebo startup step so the tag-enabled world stays running.
Alternatively, use a compatible saved map and follow [navigation](navigation.md), including the initial pose estimate. Do not run mapping and AMCL together.

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

The output is the tag's pose. Choose a separate reachable base goal before using the [Python Nav2 client](nav2_python.md).

## Stop

Stop the echo and pose-tool terminals with Ctrl+C, or run:

```sh
docker compose stop tag-pose-sim
```

Stop mapping/navigation and AprilTag services using their walkthroughs when finished.
See [pose transforms and freshness](../explanation/apriltags.md#camera-and-map-frames) for details.
