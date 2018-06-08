# Something about Docker

Subpages
- [Upgrade Docker](docker-upgrade.md)
- [Image signing](docker-image-signing.md)
- [Configurations](docker-configurations.md)

Python examples:
- [docker_checker](docker_checker/README.md)

#### Running container

```bash
# Start a container but it will exit immediately
docker run centos:6

# Container is deleted when “exit”
# i: interactive,  t: terminal; start a container and log into the container
docker run -it centos:6

# Container is not deleted when “exit”
docker run -it centos:6 /bin/bash

# Container is deleted when “exit”
docker run -it --rm centos:6 /bin/bash

# Inside container: echo $MYENV
docker run -it --rm --env MYVAR=whatever --env MYVAR2=something centos:6 /bin/bash

# Run the container in background and print container ID.
docker run -d httpd
# or
docker run --detach httpd

# Attach to a container, will cause the container to exit when “exit” the container.
docker attach

# Attach to a container, will not cause the container to exit when “exit” the container.
docker exec -it container_name /bin/bash
```

#### Removing docker images and container

```bash
# Remove all non-running containers (possible filters: created, restarting, running, paused, exited)
docker rm $(docker ps -q -f status=exited)

# Remove dangling (untagged) images
docker images prune
# OR
docker rmi $(docker images -q -f dangling=true)
```

#### Searching

```bash
# Return store
docker search image_name (e.g. docker search apache)	

# Return rating more than 50
docker search --filter stars=50 apache	

docker search --filter stars=50 --filter is-official=true apache

docker search --filter stars=50 --filter is-automated=true apache

# Return the top 10 results (based on stars)
docker search --limit 10 apache	
```

#### Docker service

```bash
# Restart docker service
sudo service docker restart
```
