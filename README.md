# Something about Docker

Subpages
- [Installation, Configurations, Storage and Volumes](docker-configurations.md)
- [Image Creation, Management, and Registry](docker-image-creation-management-registry.md)
- [Orchestration - Swarm, Node, Service](docker-orchestration.md)
- [Docker Trust Registry](docker-trusted-registry.md)
- [Docker upgrade](docker-upgrade.md)
- [Image signing](docker-image-signing.md)

Python examples:
- [docker_checker](docker_checker/README.md)

Other references:
- [Docker: Advanced multi-stage build patterns – Tõnis Tiigi](https://medium.com/@tonistiigi/advanced-multi-stage-build-patterns-6f741b852fae)


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
docker attach [containername]

# Interact inside a container and will noy cause the container to stop when you exit the running shell.
# Executing another shell in a running container and then exiting that shell will not stop the underlying container
# process started on instantiation.
docker exec -it [containername] /bin/bash
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


#### Pulling

```bash
docker pull docker.example.com/<image_path_and_name>

# Pull only latest
docker pull docker.example.com/examples/simple_image

docker pull docker.example.com/examples/simple_image:3.0

docker pull docker.example.com/examples/simple_image:3.0.0	
```

