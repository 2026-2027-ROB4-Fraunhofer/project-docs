# General Q&A

## Linux, Windows or Mac OS?

A PC with Ubuntu OS is required.

You could use WSL on windows however I will recommend to not waste your time and just use a linux PC. Reasons:

1. using hardware with WSL is tricky because of windows firewall
2. using NVIDIA GPU on WSL for running the gazebo simulation needs some settings

Don't use a VM, it's also too tricky to setup and you will just waste your time.

As I dont have experience with Mac OS, I will not support you if you have a Mac OS. Gazebo docker container won't build on Mac OS as it's ARM architecture.

Therefore just use a dual boot with ubuntu if you don't have a second laptop with ubuntu.

## What ubuntu version to use?

I recommand `Ubuntu 24.04`.

You can also use 20.04 or 22.04 if you plan to just use docker.

## What specs should my laptop have?

The most performance needy app is Gazebo harmonics, the simulation tool used. It needs a dedicated NVIDIA/AMD GPU and minimum 8GB RAM.

For real robot development, Intel i5 without dedicated GPU is enough.

## What is docker and why use it?

Docker runs isolated containers. We use it so everyone gets the same environment, dependencies and versions, regardless of their computers.

If you use docker -which I recommend-, you don't need to install ROS 2 or any tools on your laptop. Of course you do need docker ;)

Docker compopse lets you define and start multiple Docker containers together using one configuration file.

Examples (allows to start the realsense driver in a container)

- [Dockerfile](https://github.com/ipa-may/docker_ros2_tutorial/blob/main/03_ros2_realsense/Dockerfile-jazzy-realsense) (to build a docker image)
- [Compose file](https://github.com/ipa-may/docker_ros2_tutorial/blob/main/03_ros2_realsense/compose.ros2_camera_jazzy.yaml) (to start a service -aka docker container-)


See the [Docker training documentation](https://ros-industrial.github.io/ros2_i_training/_source/getting_started/docker.html).

## What are ROS 2 distributions and which one to use?

ROS 2 distributions ("distros") are different released versions of ROS 2.

Each distro has its own supported software versions and lifetime, the list is [here](https://docs.ros.org/en/jazzy/Releases.html).

- Humble is ubuntu 22.04
- Jazzy is ubuntu 24.04

ROS 2 rolling is the continuously updated development version of ROS 2. It gets the newest features first, but can change often and is less stable than fixed releases.

For this project we will use **ROS 2 Jazzy**. However the robot is on ROS 2 kilted, so we should verify that we can downmigrate to Jazzy.

## Do I need to install ROS 2 and how to?

I would recommend to just use docker, therefore it shouldnt be necessary to install ROS 2 on your laptop. I understand however that it's convenient to use ROS 2 directly on your host, especially for beginners.

To install ROS 2 Jazzy, follow the steps from the [official doc](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html). Prefer install the deb packages.

## What programming language should I use?

As you wish, but I suppose python is simpler.

## Where to start learning ROS 2 and Nav2?

- workshop from ROS-Industrial [here](https://ros-industrial.github.io/ros2_i_training/).

- official [ROS 2 documentation](https://docs.ros.org/en/jazzy/index.html)

- [Nav2 documentation](https://docs.nav2.org/jazzy/)

