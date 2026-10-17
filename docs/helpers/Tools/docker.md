# Docker cleanup

Docker images, volumes, containers, and build cache can quickly fill your disk.

Verify disk usage:
```sh
docker system df
```

Show a more detailed disk usage overview:
```sh
docker system df -v
```

Remove a Docker image:
```sh
docker rmi <image-tag>
```

Remove unused Docker volumes:
```sh
docker volume prune
```

Remove all stopped containers:
```sh
docker container prune
```

Remove dangling images:
```sh
docker image prune
```

Remove unused build cache:
```sh
docker builder prune
```

The `prune` commands ask for confirmation before removing resources. Only remove
volumes if you are sure they do not contain data you still need.

