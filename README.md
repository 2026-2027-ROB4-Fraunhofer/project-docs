# How to setup the workspace


## 1. clone the doc repo
Create a Folder in which you want to work
```sh
mkdir ROB4_Fraunhofer
cd ROB4_Fraunhofer
```

Clone this repo inside the folder
```sh
git clone git@github.com:2026-2027-ROB4-Fraunhofer/project-docs.git
```


## 2. Create a ROS 2 workspace

From the `ROB4_Fraunhofer` folder, create a ROS 2 workspace in this folder:
```sh
mkdir rob4_fraunhofer_ws
```

Go to this workspace and create an src folder:
```sh
cd rob4_fraunhofer_ws
```

```sh
mkdir src
```

## 3. Clone the dependency repos

Go to your `ROB4_Fraunhofer` folder. From it, use vcs tools to clone the dependency repo.

```sh
vcs import . < project-docs/dependencies.repos
```


Now you should have in the `ROB4_Fraunhofer` folder:

```text
ROB4_Fraunhofer
    |-- project-docs/
    |-- curtmini_piper_containers/
    |-- rob4_fraunhofer_ws/
        |--src/
            |-- curt_mini/
            |-- curtmini_piper/
            |-- piper_driver/
```

## 4. Start the docker containers

From the folder `ROB4_Fraunhofer`, go to the docker infrastructure repo:
```sh
cd curtmini_piper_containers
```

Copy the .env.example:
```sh
cp --update=none .env.example .env
```

Set `ROS_DISTRO=jazzy` and `RMW=cyclonedds` in `.env`. All container source
repositories and commit revisions are defined in `curtmini_piper_containers/locks/jazzy/*.repos`,
including the `ipa-may/curt_mini` fork. The workspace checkouts imported above
are for local development; Docker builds do not use them or this project's
`dependencies.repos`. To change container sources, edit the relevant lock manifests.

Build the three images for `gz-sim`, `moveit-rviz-sim`, and `moveitpy-sim` (from the `curtmini_piper_containers` folder):
```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  build gz-sim moveit-rviz-sim moveitpy-sim
```

On terminal #1, run the gazebo container:
```sh
xhost +local:docker
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.gui.yaml \
  up gz-sim
```

On terminal #2, run RViZ with the MotionPlanning Panel (Moveit Plugin):
```sh
xhost +local:docker

docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.gui.yaml \
  run --rm moveit-rviz-sim
```

You could also run Moveitpy:
```sh
MOVEIT_PLAN_ONLY=false docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  run --rm moveitpy-sim
```

This takes some time to build the image for the first time.


Run the keyboard teleoperation for the mobile base on another terminal
```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  run --rm --build keyboard-teleop-sim
```

## 5. Quit

```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.gui.yaml \
  --profile "*" down
```

## 6. Build and run the local workspace

Use the workspace builder to test local changes without pushing them or
rebuilding the application images. From `curtmini_piper_containers`, verify the
local checkout paths in `.env`:

```dotenv
CURT_MINI_SOURCE=../rob4_fraunhofer_ws/src/curt_mini
CURTMINI_PIPER_SOURCE=../rob4_fraunhofer_ws/src/curtmini_piper
CURTMINI_PIPER_GZ_SIM_SOURCE=../rob4_fraunhofer_ws/src/curtmini_piper_gz_sim
```

Build the workspace image once, then compile the mounted sources:

```sh
docker compose -f compose.yaml -f compose.workspace.yaml build workspace-builder
docker compose -f compose.yaml -f compose.workspace.yaml run --rm workspace-builder
```

After changing source code or checkout paths, rerun `workspace-builder`. An
image rebuild is only needed when the workspace image's ROS or system
dependencies change. See the
[`curtmini_piper_containers` README](../curtmini_piper_containers/README.md) for
the complete container workflow.


## 7. Running the simulation

### Terminal 1: Start Gazebo:

```sh
xhost +local:docker
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.workspace.yaml \
  -f compose.gui.yaml \
  up gz-sim
```
### Terminal #2: Start RViZ + Moveit
Start Rviz + Moveit:
```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.workspace.yaml \
  -f compose.gui.yaml \
  run --rm moveit-rviz-sim
```

### Terminal #3: Start MoveitPy

Run MoveItPy in another terminal:

```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  -f compose.workspace.yaml \
  run --rm moveitpy-sim
```

## Build the documentation

Install uv: https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1

```sh
uv venv
source .venv/bin/activate
uv pip install -r docs/requirements.txt
sphinx-build -W --keep-going -b html docs docs/_build/html
```

Open `docs/_build/html/index.html` in a browser to view the local build.

You can start a local web server for previewing the generated documentation:
```sh
uv run python -m http.server 8000 --directory docs/_build/html
```