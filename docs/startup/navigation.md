# Navigation on a saved map

Complete [Docker installation](../installation/software/docker.md) first.
In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

First [save a map](mapping.md). Keep Gazebo running in the same world.
If restarting a session, use the same `SIM_WORLD` in `.env` as when mapping, then start [simulation](simulation.md).
Exit the interactive teleoperation terminal with `k`, then Ctrl+C before letting Nav2 drive. Stopping a Compose service does not replace exiting a one-off `run` session.

## Start localization and navigation

```sh
docker compose stop mapping-sim nav2-rviz-sim
docker compose up --build -d nav2-sim nav2-rviz-sim
```

This loads `NAV2_MAP` from `.env` (`map.yaml` by default).

## Set the pose and send a goal

In RViz:

1. Select **2D Pose Estimate**. Click where the robot currently is on the map
   and drag the arrow to its heading. This initializes AMCL.
2. Check that the scan lines up with the map. Allow localization and the Nav2
   servers to become active.
3. Select **Nav2 Goal**. Click a reachable free location and drag to choose the
   final heading. The robot should plan a path and follow it.
4. Use **Cancel** in the Navigation 2 panel to cancel a goal.

Do not run keyboard teleoperation while Nav2 is driving: both publish to the
same controller.

Run mapping and AMCL separately; see [TF ownership](../explanation/navigation.md#how-the-pieces-connect).

```{figure} ../_static/nav2/nav2-sim_01.png
:alt: Gazebo simulation on the left and the RViz navigation view on the right
:width: 100%

`gz-sim` (left) and `nav2-rviz-sim` (right) while `nav2-sim` is running.
```

For scripted goals, use the [Python walkthrough](nav2_python.md).


Change the Nav2 settings from the nav2.yaml file, for example widening the local costmap from 4x4 meters to 12x12 meters :

```{figure} ../_static/nav2/nav2-sim_extend_forward_prune_distance.png
:alt: Gazebo simulation on the left and the RViz navigation view on the right
:width: 100%

`gz-sim` (left) and `nav2-rviz-sim` (right) while `nav2-sim` is running, 12x12m local costmap.
```

## Choose another map

For `maps/office.yaml`:

```sh
NAV2_MAP=office.yaml docker compose up -d nav2-sim
```

Set the initial pose again in RViz after changing maps.

## Stop

Cancel the active goal in the client that sent it, then stop navigation:

```sh
docker compose stop nav2-sim nav2-rviz-sim gz-sim
```

See [Nav2 configuration](../explanation/navigation.md) for topics, transforms and footprint assumptions, or [troubleshooting](troubleshooting.md#mapping-and-navigation) if localization or motion fails.
