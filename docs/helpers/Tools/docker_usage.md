# Docker usage

## Useful commands

```{list-table}
:class: command-reference
:widths: 42 58
:header-rows: 1

* - Command
  - Purpose
* - `docker compose up SERVICE`
  - Starts a service and shows its logs. Add `--build` when its image needs building.
* - `docker compose up -d SERVICE`
  - Starts a service in the background.
* - `docker compose run --rm SERVICE`
  - Runs a separate container for a tool, then removes that container when it exits. Useful for the builder and interactive keyboard driving.
* - `docker compose logs -f SERVICE`
  - Follows service logs. Ctrl+C stops following the logs, not the service.
* - `docker compose stop SERVICE`
  - Stops the named service started with `up`.
* - `docker compose ps`
  - Shows the current project's service containers and their status.
* - `docker compose --profile '*' config --services`
  - Lists all services in the configuration selected by `.env`, including optional profiles.
```

Inspect running container: 
```sh
docker compose logs --tail 120 SERVICE1 SERVICE2
```

Replace `SERVICE` with a name from the tables. Naming a service explicitly
activates its profile for that command.

For `run --rm` keyboard sessions, stop driving and
exit that terminal session with Ctrl+C.


## Useful tutorials and docs

- [docker official doc](https://docs.docker.com/)
- [docker tutorial from Nav2](https://docs.nav2.org/jazzy/tutorials/general_tutorials/docker_dev/#docker-for-development-zero-to-hero)
