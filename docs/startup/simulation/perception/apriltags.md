# Finding AprilTags

## Prerequisites

Complete [Docker installation](../../../installation/software/docker.md) first.
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

```{figure} ../../../_static/nav2/apriltags_detection_walkthrough_01.png
:alt: Gazebo simulation on the left and the RViz navigation view on the right
:width: 100%

`gz-sim` (left) and `nav2-rviz-sim` (right) with apriltags activated.
```

## Verify the camera frame

On Rviz, drag and drop the tool camera window:

```{figure} ../../../_static/perception/rviz_camera_color.png
:alt: Rviz camera window
:width: 100%

Drag and drop out the rviz camera window for the tool camera color
```

```{figure} ../../../_static/perception/camera_tool_open_visu.png
:alt: Rviz camera widen window
:width: 100%

Widen the rviz camera windows
```

## Inspect detections

In another terminal:

```sh
docker compose exec apriltag-base /opt/container/ros_entrypoint.sh \
  ros2 topic echo /base_camera/tag_detections
```

Visible tags should produce detections. 

On this example, you could see
```text
docker compose exec apriltag-base /opt/container/ros_entrypoint.sh   ros2 topic echo --once /base_camera/tag_detections
header:
  stamp:
    sec: 847
    nanosec: 638000000
  frame_id: base_camera_color_optical_frame
detections:
- family: tag36h11
  id: 2
  hamming: 0
  goodness: 0.0
  decision_margin: 69.56742095947266
  centre:
    x: 125.09929599915743
    y: 235.65759563888204
  corners:
  - x: 110.03025817871095
    y: 250.9406890869141
  - x: 140.55580139160156
    y: 251.25262451171878
  - x: 140.88943481445312
    y: 219.64315795898435
  - x: 109.37897491455081
    y: 219.79638671874997
  homography:
  - 14.571892735190787
  - 2.0739840661386237
  - 125.09929599915743
  - -1.712917925924021
  - 19.43402544541192
  - 235.65759563888204
  - -0.007452778705754323
  - 0.015914694877905724
  - 1.0
---
```

Here there is one detection of the tag36h11, with ID 2.

RViz can show `/base_camera/color/image_raw` and the detected tag frames. 

Use [teleoperation](../navigation/teleoperation.md) to explore for the other tags.

For a tag pose in `map`, first have a [saved map](../navigation/mapping.md#save-the-map), then [start Nav2](../navigation/navigation.md#start-localization-and-navigation) and [initialize AMCL](../navigation/navigation.md#set-the-initial-pose) in this tag-enabled Gazebo session. 

That would mean starting the nav2-sim service on another terminal:
```sh
docker compose up nav2-sim nav2-rviz-sim
```

You would have four windows open: 
- Rviz for navigation (top left)
- Rviz for manipulation (top right)
- Rviz Camera viewer (down right)
- Gazebo simulation (down left)


```{figure} ../../../_static/perception/apriltag_detection_multiple_windows.png
:alt: Multiple window views
:width: 100%

Multiple windows view
```

Continue to [observing a tag in the map](tag_pose.md). 

The project does not provide an automatic drive-to-tag behavior; see the [approach exercise](../../../explanation/apriltags.md#approach-exercise).

## Stop

Exit teleoperation first. Stop the topic echo with Ctrl+C, then stop the startup terminal with Ctrl+C or run:

```sh
docker compose stop apriltag-base moveit-rviz-sim gz-sim
```

See [AprilTag configuration and transforms](../../../explanation/apriltags.md) for tag IDs, dimensions and frames.
