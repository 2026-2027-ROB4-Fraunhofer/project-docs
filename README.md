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

Now go back to your `ROB4_Fraunhofer` folder:
```sh
cd ..
```

Create a ROS 2 workspace in this folder:
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
cp -n .env.example .env
```

Run the container (from the `curtmini_piper_containers` folder)
```sh
docker compose \
  -f compose.yaml \
  -f compose.cyclonedds.yaml \
  build gz-sim moveit-rviz-sim
```


This takes some time to build the image for the first time.

