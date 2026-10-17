# Finding AprilTags

Complete [Docker installation](../installation/software/docker.md) first.
In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

Keep `SIM_USE_CAMERAS=true` in `.env`. Stop any active mapping/navigation task before recreating Gazebo for this exercise.

## Start the detector

```sh
xhost +si:localuser:root
SIM_WORLD=curtmini_piper_map SIM_USE_APRILTAGS=true \
  docker compose up --build gz-sim apriltag-base moveit-rviz-sim
```

Gazebo should show the office world with tag panels. The first panel starts near the initial camera view. Omit `apriltag-base` only if implementing your own detector.

## Inspect detections

In another terminal:

```sh
docker compose exec apriltag-base /opt/container/ros_entrypoint.sh \
  ros2 topic echo /base_camera/tag_detections
```

Visible tags should produce detections. RViz can show `/base_camera/color/image_raw` and the detected tag frames. Use [teleoperation](teleoperation.md) to explore for the other tags.

For a tag pose in `map`, continue to [observing a tag in the map](tag_pose.md). The project does not provide an automatic drive-to-tag behavior; see the [approach exercise](../explanation/apriltags.md#approach-exercise).

## Stop

Exit teleoperation first. Stop the topic echo with Ctrl+C, then stop the startup terminal with Ctrl+C or run:

```sh
docker compose stop apriltag-base moveit-rviz-sim gz-sim
```

See [AprilTag configuration and transforms](../explanation/apriltags.md) for tag IDs, dimensions and frames.
