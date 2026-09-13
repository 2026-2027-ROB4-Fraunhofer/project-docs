# ROS 2 workspace basics

## ROS 2 filesystem

A ROS 2 workspace is a folder in which there is a `src` (source) folder containing the ROS 2 packages of the workspace.

Usually, the workspace folder ends with `*_ws`. In this example we will use `rob4_fraunhofer_ws` as the ROS 2 workspace name.

The file structure is:

```text
rob4_fraunhofer_ws/
    |-- src
        |--  curt_mini
        |--  curtmini_piper
        |--  curtmini_piper_gz_sim
```

The `src` folder contains ROS 2 packages and metapackages.

For example, `curtmini_piper` contains four ROS 2 packages:

- `curtmini_piper_bringup`
- `curtmini_piper_description`
- `curtmini_piper_moveit_config`
- `curtmini_piper_motion_examples`

## Building ROS 2 packages

To build (aka compile) the ROS 2 package, you run the `colcon build` command from the ROS 2 workspace. In our case you run it from  `rob4_fraunhofer_ws`.

```sh
colcon build
```

If the build succeeds, you should see `build`, `install` and `log` folders in the ROS 2 workspace.

```text
rob4_fraunhofer_ws/
    |-- build
    |-- install
    |-- log
    |-- src
```

Do not run `colcon build` somewhere else than from the ROS 2 workspace. If you did by mistake, remove the `build`, `install` and `log` folders that should not be there.

Once you built, source the install folder:

```sh
source install/setup.bash
```

you can add this command directly into the `.bashrc` file. This file is sourced on every terminal startup.

This allows you to run executables or launch scripts of the installed package from anywhere on your terminal:

```sh
ros2 run <package-name> <executable-name>
```

or

```sh
ros2 launch <package-name> <launch-script>
```
