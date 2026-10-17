# Image builds and local source workflows

## Upstream code and local settings

By default, regular application image builds fetch their owning repository from
upstream `main` (the published branch on GitHub). The four tools images use the
published `curtmini_piper_tools/main` source. Robot image builds can instead use
a local checkout; see [local robot images](../../startup/development.md#build-local-robot-images). Use the
workspace overlay for unpublished tools changes. Robot and simulator `vcs import`
steps still clone dependencies from GitHub using their manifests. Hardware's
Python SDK revision is in the robot repository's
`curtmini_piper_bringup/docker/dependencies/jazzy-hardware-python.env`.

The tools repository is private. Give the Docker builder an SSH key with access
to it before building regular `moveitpy-sim`, `moveit-action-client-sim`,
`nav2-goal-client`, or `tag-pose-sim` images. Compose uses
the SSH agent by default. If your SSH configuration selects a specific key for
a GitHub host alias, set
`CURTMINI_PIPER_TOOLS_SSH_AUTH=default=/absolute/path/to/private_key` in
`curtmini_piper_containers/.env`. The repository needs a published `main` branch
before these regular images can build.

Compose still loads service definitions from the local robot, simulator and tools
checkouts. Local edits to root or package Compose files can therefore change
commands, mounts, and build settings even for regular images. The local
`geometry.yaml`, `camera_mounts.yaml`, `initial_state.yaml`, navigation configuration, and maps
also remain runtime inputs. Review those files when checking a student's setup.

For example, the Gazebo image builds upstream `curtmini_piper_gz_sim` code and
imports `curtmini_piper`, `curt_mini`, `agx_arm_urdf`, and `neo_gz_worlds` from
its manifest. `neo_gz_worlds` uses the `gz-harmonic` branch for the office
assets. The project-level
`project-docs/dependencies.repos` creates the host workspace layout.

### Robot geometry in the simulator image

The Gazebo build gets the robot description and MoveIt configuration from
upstream `curtmini_piper/main`. The description reads
`curtmini_piper_description/config/geometry.yaml`, whose local directory is
bind-mounted into the containers. Restart the simulation and its clients after
changing mount values in that YAML; no image rebuild is needed for those values.
The simulator also publishes the camera mount TFs from the same geometry file.
Physical camera mount TFs use the separate, measured
`curtmini_piper_sensors/config/camera_mounts.yaml`.
See [Cameras](../../startup/cameras.md) for the two setups.

Changes to URDF, launch, bridge, or controller code require updating upstream
`main` and rebuilding the regular image. The local workspace workflow can test
those changes before they are published.

The simulation's starting base pose and six arm joint positions are configured
in `curtmini_piper_gz_sim/config/initial_state.yaml`. The `gz-sim` service
bind-mounts that file, so a service restart applies pose edits without
rebuilding the image. Bridge and controller YAML files use the upstream image
copies. See the [simulation guide](../simulation.md#starting-pose-and-joint-positions).

Rebuild an application image after upstream code changes. `--build` may reuse
cached Git imports even when a remote branch advances. To fetch the latest
simulator commit after pushing it to `main`, run:

```sh
docker compose build --no-cache gz-sim
```

For published navigation package changes, use `mapping-sim` in place of
`gz-sim`; the navigation services share its image. Then recreate the affected
services with the commands in the [simulation guide](../../startup/simulation.md)
or [navigation guide](../../startup/navigation.md).

## Choose a source workflow

Start with the first row unless you are changing source code:

| Your task | Workflow | Source used |
| --- | --- | --- |
| Run the published project | Regular images, without `compose.workspace.yaml` | GitHub `main` by default |
| Test changes in robot packages, including hardware bringup | [Build local robot images](../../startup/development.md#build-local-robot-images), without `compose.workspace.yaml` | Local `curtmini_piper` checkout; dependencies still come from their manifests |
| Develop simulation or tools alongside robot packages | [Local workspace](../../startup/development.md#local-workspace-development), with `compose.workspace.yaml` | Mounted local sources compiled into a shared install volume; hardware services keep their own images |

## Development commands

See [development workflows](../../startup/development.md) for refreshing images, building local robot images, and compiling a local workspace.

## Local robot image behavior

`CURTMINI_PIPER_IMAGE_SOURCE` must be an absolute path so the package Compose files resolve the same checkout. It changes robot image builds only; Gazebo and tools retain their own source inputs. Use the workspace overlay to test local robot description changes inside Gazebo.

Local and published robot builds use the same image tags. A later build without the local override selects published source again. Start a locally built image without `--build`, or retain the override in `.env` for repeated builds. Remove both the `.env` setting and any shell export when returning to published source, then rebuild.

Keep robot and infrastructure checkouts compatible. If the package Docker layout is not yet published upstream, the regular remote build cannot find it; use the local source override until it is published.

## Workspace overlay behavior

`compose.workspace.yaml` adds `workspace-builder` and mounts its shared installation into the simulation and client services. Hardware services keep their separate images. The builder compiles local simulator, navigation and tools sources, so rerun it after source edits and restart affected services.

The container repository's [workspace guide](https://github.com/ipa-may/curtmini_piper_containers/blob/main/README.md#local-simulation-workspace) describes mounts and cached dependencies.

## Developer check coverage

The optional robot `compose.test.yaml` selects Dockerfile stages for separate test images. Checks cover Xacro expansion, MoveIt launch-argument parsing, teleop package availability, and registered package tests. Coverage depends on each package.

These checks do not start hardware services or verify CAN communication, firmware or physical motion. Keep this overlay out of the normal `COMPOSE_FILE`. See the robot repository's [container checks](https://github.com/ipa-may/curtmini_piper/blob/main/doc/containers.md#checks) for the commands.
