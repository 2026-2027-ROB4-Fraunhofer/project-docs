# AprilTag navigation exercise

The office simulation can spawn three AprilTag panels for a camera based
navigation exercise. Each panel has a different ID. Your task is to make the
mobile base approach a requested tag and stop at a safe distance, facing it.
The project supplies the camera streams and an optional detector; it does not
supply code that drives to a tag.

## Start the exercise

Complete the [Docker setup](../installation/software/docker.md) and use the
regular Compose files from `.env`. From `curtmini_piper_containers/`, run:

```sh
xhost +si:localuser:root
SIM_WORLD=curtmini_piper_map SIM_USE_APRILTAGS=true \
  docker compose up --build gz-sim apriltag-base moveit-rviz-sim
```

The detector service is optional: omit `apriltag-base` if you want to implement
tag detection yourself. The Gazebo window is optional, but leave
`SIM_USE_CAMERAS=true` so the base camera publishes images. If you have just
pushed simulator changes to upstream `main`, follow the
[image refresh instructions](../installation/software/docker.md#upstream-code-and-local-settings)
to avoid reusing an older cached image.

The supplied tag layout is
`curtmini_piper_gz_sim/config/apriltags.yaml`. It defines IDs 0, 1, and 2,
their 0.20 m black-square edge size, and their positions and orientations in
the world. Edit the local file and restart `gz-sim` to change the exercise.
Only those three IDs have packaged textures. If you change their edge size,
also set `APRILTAG_SIZE` to the same value for the detector service.

## Observe the tags

The base camera publishes `/base_camera/color/image_raw` and
`/base_camera/color/camera_info`. The optional detector publishes
`/base_camera/tag_detections` and tag transforms on `/tf`. To check detections:

```sh
docker compose exec apriltag-base /opt/container/ros_entrypoint.sh \
  ros2 topic echo /base_camera/tag_detections
```

The detector reports a tag pose relative to the camera frame when the tag is
visible. Gazebo does not publish the tags' true world poses into ROS. RViz can
show the camera image, robot TF tree, and detected tag frames. The first panel
starts near the robot's initial view; the others require exploration.

After starting [mapping or Nav2 localization](navigation.md), the optional
[`tag-pose-sim` tool](tools.md#observe-a-tag-in-the-map) can report an observed
tag pose in `map`. A separate [Python Nav2 client](tools.md#request-a-nav2-goal-from-python)
accepts an explicit base goal. Combining them into a safe approach behavior
is part of the exercise.

Choose an approach point in free space in front of the panel. The panel has
collision geometry, so its exact position is not a safe navigation goal. A
successful run should stop roughly 0.6–1.0 m from the requested tag, facing
it, while keeping the tag visible. You may use the existing Nav2 setup or
another controller to reach that pose.
