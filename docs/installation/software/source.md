# Source installation

These instructions assume ROS 2 Jazzy on Ubuntu 24.04.
The `curtmini_piper_tools` repository is private; importing
`project-docs/dependencies.repos` requires GitHub access to it through SSH.

## Install dependencies

```bash
source /opt/ros/jazzy/setup.bash
sudo apt update
sudo apt install -y \
  python3-colcon-common-extensions \
  python3-vcstool \
  python3-rosdep \
  python3-can \
  python3-scipy \
  can-utils \
  ethtool
```

Initialize rosdep once per machine, then update it:

```bash
sudo rosdep init
rosdep update
```

An `already initialized` response from `rosdep init` can be ignored.

Import the nested Curt Mini dependencies:

```bash
cd ~/ROB4_Fraunhofer/rob4_fraunhofer_ws
vcs import --recursive --skip-existing src \
  < src/curt_mini/ipa_ros2_control/ipa_ros2_control.repos
vcs import --recursive --skip-existing src \
  < src/curt_mini/curt_mini_bringup/curt_mini.repos
```

Install the Piper Python SDK using
[`uv`](https://docs.astral.sh/uv/):

```bash
uv venv .venv
source .venv/bin/activate
uv pip install --break-system-packages \
  "git+https://github.com/agilexrobotics/pyAgxArm.git"
uv pip install numpy pyyaml
```

Install the declared ROS and system dependencies:

```bash
rosdep install --from-paths src --ignore-src --rosdistro jazzy -ry
```

## Build

From `rob4_fraunhofer_ws`:

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-up-to \
  curtmini_piper_bringup \
  curtmini_piper_gz_sim \
  curtmini_piper_moveitpy_example \
  curtmini_piper_sensors \
  curtmini_piper_tag_tools \
  curtmini_piper_nav_examples
source install/setup.bash
```

`curtmini_piper_sensors` provides the two physical D435i launch instances.
See [Cameras](../../startup/cameras.md) for their serial numbers and measured
mount offsets.
