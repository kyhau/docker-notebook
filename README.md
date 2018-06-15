# Docker notebook

Subpages
- [Installation and Configurations](docker-configurations.md)
- [Image Creation, Management, and Registry](docker-image-creation-management-registry.md)
- [Dockerfile](docker-dockerfile.md)
- [Orchestration - Swarm, Node, Service](docker-orchestration.md)
- [Storage and Volumes](docker-storage-and-volumes.md)
- [Networking](docker-networking.md)
- [Security](docker-security.md)
- [Docker Trust Registry](docker-trusted-registry.md)
- [Docker upgrade](docker-upgrade.md)
- [Image signing](docker-image-signing.md)

Python examples:
- [docker_checker](docker_checker/README.md)

Other references:
- [Docker Advanced multi-stage build patterns – Tõnis Tiigi](https://medium.com/@tonistiigi/advanced-multi-stage-build-patterns-6f741b852fae)
- [Docker ARG, ENV and .env - a Complete Guide](https://vsupalov.com/docker-arg-env-variable-guide/)


#### Running container

```bash
# Start a container from the image 'centos:6'; it will exit immediately
docker run centos:6

# Container is deleted when “exit”
# i: interactive,  t: terminal; launch a container in 'interactive' mode in the current 'terminal'
docker run -it centos:6

# Container is not deleted when “exit”
docker run -it centos:6 /bin/bash

# Container is deleted when “exit”
docker run -it --rm centos:6 /bin/bash

# Inside container: echo $MYVAR and $MYVAR2
docker run -it --rm --env MYVAR=whatever --env MYVAR2=something centos:6 /bin/bash

# Run the container from the image 'httpd:latest' in background (-d or --detach) and print container ID.
docker run -d httpd

# Attach to a container, will cause the container to exit when “exit” the container.
docker attach [container_name]

# Interact inside a container and will noy cause the container to stop when you exit the running shell.
# Executing another shell in a running container and then exiting that shell will not stop the underlying
# container process started on instantiation.
docker exec -it [container_name] /bin/bash

# Instantiate a docker container called 'myweb' that is running an Apache web server on port 80 by default within
# it, you can allow direct access to the container service via the host's IP by redirecting the container port 80
# to the host port 80. Redirecting ports is through the '-p [host port]:[container port]' syntax.
docker run -d --name myweb -p 80:80 httpd:latest

# Instantiate a container called 'myweb' running an Apache application from the image 'httpd:latest' on your
# system, and allow the container port 80 to be redirected to the underlying host's port somewhere in the range
# of 80-85, based on port availability.
docker run -d --name myweb -p 80-85:80 httpd:latest

# Instantiate a container (named myweb) running Apache from an image called 'http:latest', mount the underlying
# hosts's '/var/www/html' directory in the container's '/usr/local/apache2/htdocs'
docker run -d --name myweb -v /var/www/html:/usr/local/apache2/htdocs httpd:latest
# OR
docker run -d --name myweb --mount type=bind,src=/var/www/html,target=/usr/local/apache2/htdocs httpd:latest

# If you have 2 CPUs, guarantee the container at most at most one and a half of the CPUs every second.
# Docker 1.13 and higher. Docker 1.12 and lower uses --cpu-period=100000 --cpu-quota=50000
docker run -it --cpus="1.5" ubuntu /bin/bash

# The maximum amount of memory the container can use. If you set this option, the minimum allowed value is 4m
# (4 megabyte).
docker run -it --memory=[amount b/k/m/g] ubuntu /bin/bash

# If --memory and --memory-swap are set to the same value, this prevents containers from using any swap. This is
# because --memory-swap is the amount of combined memory and swap that can be used, while --memory is only the
# amount of physical memory that can be used.
docker run -it --memory=[amount b/k/m/g] --memory-swap=[amount b/k/m/g] ubuntu /bin/bash

# The 'docker run' command uses the --dns option to override the default DNS servers for a container.
docker run -d --dns=8.8.8.8 [image_name]

# Allow the container to perform operations that a container may otherwise be restricted from performing. So
# basically any container host that you allow anyone to launch a --privileged container on is the same as giving
# them root access to every container on that host.
docker run --privileged -it --rm ubuntu:latest /bin/bash
```


#### Removing docker images and container

```bash
# Remove ALL stopped containers, images without at least one container associated, all build cache, and all
# networks not used by at least one container, from a Docker host
docker system prune -a

# Remove dangling (untagged) images
docker images prune
# OR
docker rmi $(docker images -q -f dangling=true)
# OR
docker image rm $(docker images -q -f dangling=true)

# Remove an image with containers based on it as they will otherwise be left orphaned
docker rmi [image_name] --force

# Remove all non-running containers (filters: created, restarting, running, paused, exited)
docker rm $(docker ps -q -f status=exited)

docker rm [container_name or container_id]
```


#### `docker image`

```bash
# Display detailed information on one or more images
docker image inspect [image_id]
```


#### `docker history`

The 'history' option will display the image layers, the number of them, and how they were built on the image.

```bash
# Review an image's storage layers
docker history [image_id]
```


#### `docker search`

```bash
# Return store
docker search [image_name] (e.g. docker search apache)	

# Return rating more than 50
docker search --filter stars=50 apache	

docker search --filter stars=50 --filter is-official=true apache

docker search --filter stars=50 --filter is-automated=true apache

# Return the top 10 results (based on stars)
docker search --limit 10 apache	
```


#### `docker pull`

```bash
docker pull docker.example.com/<image_path_and_name>

# Pull only latest
docker pull docker.example.com/examples/simple_image

docker pull docker.example.com/examples/simple_image:3.0

docker pull docker.example.com/examples/simple_image:3.0.0	
```


#### `docker container`

New way to do docker container commands (make it clearer).

```bash
# New way to do `docker ps`
docker container ls

# You have to temporarily use a public DNS (8.8.8.8) when launching transient detached containers
# while your corporate DNS servers are undergoing maintenance. Which docker command would use that
# public DNS server for name resolution?
# The 'docker run' command uses the --dns option to override the default DNS servers for a
# container.
docker container run -d --dns=8.8.8.8 [image]
# OR
docker run -d --dns=8.8.8.8 [image]

```


#### `docker inspect` (or `docker container inspect`)

- `docker inspect` returns low-level information on Docker objects. 
- Default format is json.

```bash
# The '--pretty' option will format the associated output in a more easily readable format.
# JSON, is thde default output from an inspect command.
docker inspect [NODE ID] --pretty

# There are multiple references to the key search term IP, but only one specifically called
# 'IPAddress' when running the 'inspect' command on any container.
docker inspect myweb | grep IPAddress

# The output will be formatted as to be more easily readable on standard output.
docker inspect --format="{{.Structure.To.Review}}" [objectid/name] myweb

# Show JUST the IP address of a running container called 'testweb'
docker container inspect --format="{{.NetworkSettings.Networks.bridge.IPAddress}" testweb
```


#### `docker-compose`

1. `docker-compose` allows you to define one or more containers in a single configuration file that
    can then be deployed all at once.

