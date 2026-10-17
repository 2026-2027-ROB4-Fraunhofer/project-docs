# Mapping in simulation

## Prerequisites

Complete [Docker installation](../../../installation/software/docker.md) first.
In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

Keep `SIM_USE_HOKUYO=true` in `.env`. Stop navigation and exit any teleoperation session before starting a new mapping run. Keep the arm in its initial pose; see [footprint assumptions](../../../explanation/navigation.md#how-the-pieces-connect).

## Start mapping

```sh
xhost +si:localuser:root
docker compose stop nav2-sim
SIM_WORLD=curtmini_piper_map docker compose up --build -d --force-recreate \
  gz-sim mapping-sim nav2-rviz-sim
```

Gazebo should show office walls and furniture. In RViz, the laser points should align with walls and the map should begin to fill in. If they do not, see [navigation troubleshooting](../../troubleshooting.md#mapping-and-navigation).

```{figure} ../../../_static/nav2/mapping_01.png
:alt: Gazebo simulation on the left and the RViz mapping view on the right
:width: 100%

`gz-sim` (left) and `nav2-rviz-sim` (right) while `mapping-sim` is running.
```

## Drive around

```sh
docker compose run --rm --build keyboard-teleop-sim
```

Keep the terminal focused. Use `i` forward, `,` backward, `j`/`l` to turn, and `k` to stop. Drive slowly through the area you want to map. Press `k`, then Ctrl+C to exit.

## Save the map

From another terminal:

```sh
docker compose exec mapping-sim /opt/container/ros_entrypoint.sh \
  ros2 run nav2_map_server map_saver_cli -f /maps/map \
  --ros-args -p use_sim_time:=true -p save_map_timeout:=10.0
```

Check for `map.yaml` and `map.pgm` in `rob4_fraunhofer_ws/src/curtmini_piper/curtmini_piper_navigation/maps/` on the host. Keep both files together.
To choose another name, replace `/maps/map` with `/maps/office`, for example.


```{figure} ../../../_static/nav2/office_map.png
:alt: Map visualization
:width: 100%

Map saved for the office world
```

### Reading the map

- **White:** known free space. Nav2 can plan through it, provided there is enough clearance for the robot.
- **Black:** occupied space, such as walls or furniture. Nav2 treats it as an obstacle.
- **Grey:** unknown space that has not been sufficiently observed. The current configuration preserves unknown cells (`track_unknown_space: true`) and prevents the global planner from routing through them (`allow_unknown: false`).

Nav2 also considers live sensor readings and adds costs around obstacles, so a white area is not automatically traversable. Explore the areas you want to navigate before saving the map.

## Continue or stop

Continue to [navigation on the saved map](navigation.md), leaving Gazebo running.
To end the session instead:

```sh
docker compose stop mapping-sim nav2-rviz-sim gz-sim
```

See [Nav2 configuration and map files](../../../explanation/navigation.md) for the details behind these steps.
