# AprilTag detection and pose transforms

The office simulation can spawn three AprilTag panels for a camera based
navigation exercise. Each panel has a different ID. Your task is to make the
mobile base approach a requested tag and stop at a safe distance, facing it.
The project supplies the camera streams and an optional detector; it does not
supply code that drives to a tag.

The supplied tag layout is
`curtmini_piper_gz_sim/config/apriltags.yaml`. It defines IDs 0, 1, and 2,
their 0.20 m black-square edge size, and their positions and orientations in
the world. Edit the local file and restart `gz-sim` to change the exercise.
Only those three IDs have packaged textures. If you change their edge size,
also set `APRILTAG_SIZE` to the same value for the detector service.

## Camera and map frames

The detector consumes `/base_camera/color/image_raw` and `/base_camera/color/camera_info`. It publishes `/base_camera/tag_detections` and detected tag transforms on `/tf`.

The detector reports a tag pose relative to the camera frame when the tag is
visible. Gazebo does not publish the tags' true world poses into ROS. RViz can
show the camera image, robot TF tree, and detected tag frames. The first panel
starts near the robot's initial view; the others require exploration.

The `tag-pose-sim` tool looks up the detector's `tag36h11:0` frame through the robot's camera TF
chain and publishes `/tag_pose_in_map` as a `PoseStamped`. Set `TAG_FRAME` to
another observed frame before starting the service to inspect a different tag.
The output stops when the tag observation is too old. The tool uses camera
observations; it does not read the panels' Gazebo world coordinates.

The result is the **tag pose**. The student task is to select a safe base pose
near it, with enough space for the robot footprint and a heading facing the
panel.

## Approach exercise

Choose an approach point in free space in front of the panel. The panel has
collision geometry, so its exact position is not a safe navigation goal. A
successful run should stop roughly 0.6–1.0 m from the requested tag, facing
it, while keeping the tag visible. You may use the existing Nav2 setup or
another controller to reach that pose.

For commands, see [finding AprilTags](../startup/apriltags.md), [observing a tag in the map](../startup/tag_pose.md), and [sending a Nav2 goal](../startup/nav2_python.md).
