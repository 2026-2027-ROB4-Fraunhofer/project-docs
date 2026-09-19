# Docker installation

## About Docker

Why use Docker?

There are many reaons.

- **Consistent environment**: Everyone develops and runs the application with the same dependencies, libraries, and versions.

- **Avoid host-specific issues**: You don’t have to worry about differences in Ubuntu versions, installed packages, or system configurations.

- **Reproducibility**: The same Docker image can be used by different developers and in CI/CD or deployment environments.

- **Easy setup** and **Easier onboarding**: Once the Docker configuration is in place, setting up the project on a new machine is much simpler. New developers can get the project running without manually installing and configuring all dependencies.

- **Dependency isolation** and **Cleaner host machine**: ROS 2 and other application dependencies are isolated from the host system. You also avoid installing project-specific dependencies directly on the host.

and others.

That is why you'll get docker containers for starting robot bringup and Gazebo simulation. 


## On Docker installation

Install docker following the [official documentation](https://docs.docker.com/engine/install/ubuntu/).

If you have root access on your PC, complete Docker’s [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/).


### On using docker in general

Have a look into [this page](https://ros-industrial.github.io/ros2_i_training/_source/getting_started/docker.html) for commands.

Docker can quickly fill your disk space if not used correctly or if you have alot of different images. [Here](https://2026-2027-rob4-fraunhofer.github.io/project-docs/student_helpers/Tools/docker.html) some commands to help you remove unused docker images, containers and volumes and free your disk space.

## On Docker usage for this project

The [container repository](https://github.com/ipa-may/curtmini_piper_containers)
provides Compose services for simulation, hardware, RViz, MoveItPy, and teleoperation.

Run docker commands from this repository. That mean, you should be inside the folder `curtmini_piper_containers/`.

See the container repository's
[Compose file guide](https://github.com/ipa-may/curtmini_piper_containers/blob/main/README_compose_files.md)
and
[service reference](https://github.com/ipa-may/curtmini_piper_containers/blob/main/README_compose_service.md)
for the complete workflow.
