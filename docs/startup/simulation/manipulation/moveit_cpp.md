# Moving the arm with the C++ MoveIt client

## Prerequisites

- Complete [Docker installation](../../../installation/software/docker.md).
- Start MoveIt through the [first arm motion walkthrough](moveit_gui.md#start-moveit-and-rviz).
- Keep the backend running and finish any previous arm motion before sending a new goal.

In each terminal, run commands from:

```sh
cd ~/ROB4_Fraunhofer/curtmini_piper_containers
```

## Configure and build

Edit `curtmini_piper_tools/curtmini_piper_moveit_action_client_example/config/goal.yaml` to choose the six joint positions in radians.
Build the shared base image before the first client build:

```sh
docker compose build moveit-rviz-sim
```

## Plan

```sh
MOVEIT_PLAN_ONLY=true docker compose run --rm --build moveit-action-client-sim
```

The client should report the action result without moving the arm.

## Execute

```sh
MOVEIT_PLAN_ONLY=false docker compose run --rm --build moveit-action-client-sim
```

The simulated arm should move to the requested joint goal.

## Finish

The client exits when the action completes. Finish the motion request before stopping the backend through its startup page. Closing the client is not a documented motion-cancellation mechanism.

See [C++ action interface](../../../explanation/moveit.md#c-action-client) for the direct action client and the separate pose examples.
