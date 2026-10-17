# Simulation configuration

For commands, see [simulation startup](../startup/simulation/bringup.md).

## Gazebo real-time factor

The percentage at Gazebo's bottom right is the **real-time factor**: simulation time divided by elapsed real time, expressed as a percentage.

```{figure} ../_static/simulation/gz-sim_real_time_factor.png
:alt: Gazebo window with the real-time factor of 13.95 percent highlighted at the bottom right
:width: 100%

The highlighted 13.95% means the simulation runs about seven times slower than real time.
```

| Factor | Meaning |
| --- | --- |
| 100% | One simulated second takes one real second. |
| 50% | One simulated second takes two real seconds. |
| 20% | One simulated second takes five real seconds. |

A low factor slows the whole simulation. If the factor is near 100% but the robot moves slowly, check its commanded speed and motion limits instead.

CPU load, physics, sensor generation, and rendering all affect performance. On hosts with NVIDIA graphics, check [Gazebo GPU selection](compose_project/environment.md#gazebo-gpu-selection); GPU selection alone does not guarantee real-time speed.

## Worlds

`curtmini_piper_map` is the office world.

Use `SIM_WORLD=curtmini_piper` for the simple ground-plane world, either in `.env` or before a command:
```sh
SIM_WORLD=curtmini_piper docker compose up --build gz-sim moveit-rviz-sim
```

To load a world from `neo_gz_worlds`, use its name without a path, for example
`SIM_WORLD=neo_workshop` in the same command.

Other choices include:
- `neo_office_empty`
- `neo_workshop_2`
- `office_harmonic_02`.

The Neo world files do not load the sensor systems used by the simulator's own worlds, so
lidar, camera, and IMU data may be unavailable in them.

## Starting pose and joint positions

Edit `curtmini_piper_gz_sim/config/initial_state.yaml` to set the starting
`base.x`, `base.y`, and `base.z` in metres, `base.orientation` as a rotation
around Z in radians, and all six `arm.piper_joint*` positions in radians. The
launch checks those joint positions against the Piper limits. The `gz-sim`
service bind-mounts this YAML file, so restart the service after editing it;
an image rebuild is not needed for this setting. Bridge and controller YAML
files come from the upstream simulator in regular images.

For a native ROS workspace launch, point to the source YAML to apply edits
without rebuilding the package. Run this from the simulator repository root:

```sh
ros2 launch curtmini_piper_gz_sim simulation.launch.py \
  initial_state_file:=$(pwd)/config/initial_state.yaml
```

The launch uses its installed copy of `initial_state.yaml` when no path is
provided. Arm, TCP, lidar, and simulated camera mounts are configured
separately in `curtmini_piper_description/config/geometry.yaml`; see
[robot geometry in the simulator image](compose_project/image_builds.md#robot-geometry-in-the-simulator-image)
for when to restart or rebuild.

## Controller and MoveIt checks

One spawner activates `joint_state_broadcaster`, `base_controller`, and
`arm_controller` in that order. After startup, check their states from the
infrastructure repository:

```sh
docker compose exec gz-sim /opt/container/ros_entrypoint.sh \
  ros2 control list_controllers
```

All three should be `active`. If the broadcaster is loaded but `inactive`,
`/joint_states` will be missing; inspect the spawner output before planning or
executing a motion. The simulator's `config/moveit_controllers.yaml` sets
`trajectory_execution.allowed_start_tolerance` to `0.0`, which disables
MoveIt's trajectory start-position check. MoveIt still needs current joint
states from the broadcaster.
