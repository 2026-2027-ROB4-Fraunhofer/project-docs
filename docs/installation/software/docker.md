# Docker installation

The [container repository](https://github.com/ipa-may/curtmini_piper_containers)
provides Compose services for simulation, hardware, RViz, MoveItPy, and
teleoperation.

For local development, its `workspace-builder` mounts the source checkouts and
runs `colcon build` without requiring the changes to be pushed:

```bash
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
cp -n .env.example .env
docker compose -f compose.yaml -f compose.workspace.yaml build workspace-builder
docker compose -f compose.yaml -f compose.workspace.yaml run --rm workspace-builder
```

See the container repository's
[Compose file guide](https://github.com/ipa-may/curtmini_piper_containers/blob/main/README_compose_files.md)
and
[service reference](https://github.com/ipa-may/curtmini_piper_containers/blob/main/README_compose_service.md)
for the complete workflow.
