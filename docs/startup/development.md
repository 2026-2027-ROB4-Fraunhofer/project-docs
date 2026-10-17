# Development workflows

Complete [Docker installation](../installation/software/docker.md) first. In each terminal:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

Choose a workflow using [image builds and local sources](../explanation/compose_project/image_builds.md#choose-a-source-workflow).

## Refresh published images

Stop the affected services first, then rebuild without the Git-import cache:

```sh
docker compose build --no-cache gz-sim
```

Use `mapping-sim` for the shared navigation image, or `piper-bringup moveit-rviz-hardware` for arm and hardware RViz images. Include `base-bringup` when updating the base. Restart using the relevant startup page.

## Build local robot images

Keep the regular `COMPOSE_FILE` in `.env`, without `compose.workspace.yaml`:

```sh
CURTMINI_PIPER_IMAGE_SOURCE="$(realpath ../rob4_fraunhofer_ws/src/curtmini_piper)" \
  docker compose build piper-bringup moveit-rviz-hardware
```

Replace the service names with the robot images you need. This builds images without starting hardware. After [hardware preparation](hardware/bringup.md#prepare-can-and-gui-access), start these built images without `--build`:

```sh
docker compose up piper-bringup moveit-rviz-hardware
```

For repeated builds, set the absolute `CURTMINI_PIPER_IMAGE_SOURCE` path in `.env`. To return to published images, remove that setting, clear any shell override, and rebuild:

```sh
unset CURTMINI_PIPER_IMAGE_SOURCE
docker compose build --no-cache piper-bringup moveit-rviz-hardware
```

See [local robot image behavior](../explanation/compose_project/image_builds.md#local-robot-image-behavior) for which packages this affects.

## Local workspace development

Stop the affected simulation/client services. In `.env`, select:

```ini
COMPOSE_FILE=compose.yaml:compose.cyclonedds.yaml:compose.workspace.yaml:compose.gui.yaml
```

Build the development image and your mounted sources:

```sh
docker compose build workspace-builder
docker compose run --rm workspace-builder
```

After a successful build, start the services from the relevant walkthrough. After further edits, stop affected services, rerun `workspace-builder`, and restart them.
To return to regular images, remove `compose.workspace.yaml` from `.env` and start the affected services with `--build`.
See [workspace overlay behavior](../explanation/compose_project/image_builds.md#workspace-overlay-behavior) for mounts and hardware exclusions.

## Optional developer checks

Use the robot repository's [container check commands](https://github.com/ipa-may/curtmini_piper/blob/main/doc/containers.md#checks) when changing container or robot configuration.
Keep `compose.test.yaml` out of the normal `COMPOSE_FILE`. See [check coverage](../explanation/compose_project/image_builds.md#developer-check-coverage) for what these checks verify.
