# Curt Mini with Piper Arm

Project documentation for the Curt Mini mobile base, AgileX Piper arm, Gazebo simulation and supporting tools.

- [Installation](docs/installation/index.md): workspace, Docker, native ROS 2 and hardware setup.
- [Startup and walkthrough](docs/startup/index.md): start available components and run a specific task.
- [Explanation](docs/explanation/index.md): project architecture, Compose, Nav2, MoveIt and sensors.
- [Helpers](docs/helpers/index.md): general Git, Docker and ROS 2 guidance.

Start with [workspace setup](docs/installation/software/index.md#create-the-workspace), then [Docker configuration](docs/installation/software/docker.md). The tools repository is private and requires GitHub access.
The full real-robot deployment is still in progress; see [deployment architecture](docs/explanation/compose_project/system_deployment_architecture.md).

## Build the documentation

From `project-docs`, install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```sh
uv venv
source .venv/bin/activate
uv pip install -r docs/requirements.txt
sphinx-build -W --keep-going -b html docs docs/_build/html
```

Open `docs/_build/html/index.html`, or preview it with:

```sh
uv run python -m http.server 8000 --directory docs/_build/html
```

GitHub Actions builds and deploys the guide on pushes to `main` and manual workflow runs.
