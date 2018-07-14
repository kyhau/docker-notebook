# Docker notebook

Subpages
- [Docker Overview - Docker Engine, dockerd, namespaces, cgroups, UnionFD](docker-overview.md)
- [Installation and Configurations](docker-configurations.md)
- [Dockerfile, Image Creation, Management, and Registry](docker-image-creation-management-registry.md)
- [Storage and Volumes](docker-storage-and-volumes.md)
- [Orchestration - Swarm, Node, Service](docker-orchestration.md)
- [Networking](docker-networking.md)
- [Docker Trusty Registry, Image Signing, Image Scanning](docker-dtr.md)
- [Universal Control Plane (UCP), Manager, Worker, Pause Containers](docker-ucp.md)
- [Security](docker-security.md)
- [Backups and disaster Recovery](docker-backup.md)
- [Docker upgrade](docker-upgrade.md)
- Python examples: [docker_checker](docker_checker/README.md)

Other references:
- [Docker Advanced multi-stage build patterns – Tõnis Tiigi](
  https://medium.com/@tonistiigi/advanced-multi-stage-build-patterns-6f741b852fae)
- [Docker ARG, ENV and .env - a Complete Guide](https://vsupalov.com/docker-arg-env-variable-guide/)


## Cheat Sheet

### Running container

```bash
# Start a container from the image 'centos:6'; it will exit immediately.
docker run centos:6

# Start a container from the image 'httpd:latest' in background (-d or --detach) and print container ID.
docker run -d httpd

# Launch a container in 'interactive' mode in the current 'terminal'; i: interactive, t: terminal
# Container is deleted at “exit”.
docker run -it centos:6

# Container is not deleted at “exit”.
docker run -it centos:6 /bin/bash

# Container is deleted at “exit”.
docker run -it --rm centos:6 /bin/bash

# Attach local standard input, output, and error streams to a running container
# Will cause the container to exit when “exit” the container.
docker attach [OPTIONS] CONTAINER_NAME

# Run a command in a running container
docker exec [OPTIONS] CONTAINER_NAME COMMAND [ARG...]

# Executing another shell in a running container and then exiting that shell will not stop the underlying
# container process started on instantiation.
docker exec -it CONTAINER_NAME /bin/bash

# Inside container: echo $MYVAR and $MYVAR2
docker run -it --rm --env MYVAR=whatever --env MYVAR2=something centos:6 /bin/bash

# Note: To specify container name, use '--name'. Note that '--name' has no short form ('-n' is not valid).

# Instantiate a docker container called 'myweb' that is running an Apache web server on port 80 by default within
# it, you can allow direct access to the container service via the host's IP by redirecting the container port 80
# to the host port 80. Redirecting ports is through the '-p [host port]:[container port]' syntax.
docker run -d --name myweb -p 80:80 httpd:latest

# Instantiate a container called 'myweb' running an Apache application from the image 'httpd:latest' on your
# system, and allow the container port 80 to be redirected to the underlying host's port somewhere in the range
# of 80-85, based on port availability.
docker run -d --name myweb -p 80-85:80 httpd:latest

# Instantiate a container (named myweb) running Apache from an image called 'httpd:latest', mount the underlying
# hosts's '/var/www/html' directory in the container's '/usr/local/apache2/htdocs'
# Option 1: use (-v or --volume <src>:<dest>)
docker run -d --name myweb -v /var/www/html:/usr/local/apache2/htdocs httpd:latest
# OR
# Option 2: use (--mount type=bind,src=<src>,target=<dest>)
docker run -d --name myweb --mount type=bind,src=/var/www/html,target=/usr/local/apache2/htdocs httpd:latest

# Note: you cannot add a volume to an instantiated container.

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
docker run -d --dns=8.8.8.8 IMAGE_NAME

# Allow the container to perform operations that a container may otherwise be restricted from performing. So
# basically any container host that you allow anyone to launch a --privileged container on is the same as giving
# them root access to every container on that host.
docker run --privileged -it --rm ubuntu:latest /bin/bash
```


### Removing docker images and container

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

# Force removal of an image (e.g. remove an image with containers based on it); --force or -f
docker rmi IMAGE_NAME --force

# Do not delete untagged parents
docker rmi IMAGE_NAME --no-prune

# Remove all non-running containers (filters: created, restarting, running, paused, exited)
docker rm $(docker ps -q -f status=exited)

docker rm <CONTAINER_NAME or CONTAINER_ID>
```


### General commands to manage containers and images

```bash
# List all containers (both running or not running)
docker ps -a

# The column ‘size’ shows the amount of data that is used for the writable layer of each container.
# The column ‘virtual size’ shows the amount of data used for the read-only image data used by the container
# plus the container’s writable layer ‘size’.
docker ps -s

# List the locally installed images that can be used to instantiate containers from
docker images

# List all locally installed images including intermediate images and dangling images
docker images -a

```


### `docker image`

```bash

# Display detailed information on one or more images
docker image inspect IMAGE_ID
```


### `docker container`

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


### `docker inspect` (or `docker container inspect`)

- `docker inspect` returns low-level information on Docker objects. 
- Default format is json.

```bash
# The '--pretty' option will format the associated output in a more easily readable format.
# JSON, is thde default output from an inspect command.
docker inspect [NODE_ID] --pretty

# The output will be formatted as to be more easily readable on standard output.
docker inspect --format="{{.Structure.To.Review}}" [objectid/name] myweb

# Display the IP address of the running container `myweb`.
# There are multiple references to the key search term IP, but only one specifically called
# 'IPAddress' when running the 'inspect' command on any container.
docker inspect myweb | grep IPAddress

# Show JUST the IP address of a running container called 'testweb'
docker container inspect --format="{{.NetworkSettings.Networks.bridge.IPAddress}" testweb
```


### `docker history`

The 'history' option will display the image layers, the number of them, and how they were built on the image.

```bash
# Review an image's storage layers
docker history IMAGE_ID
```


### `docker search`

```bash
# Return store
docker search IMAGE_NAME (e.g. docker search apache)	

# Return rating more than 50
docker search --filter stars=50 apache	

docker search --filter stars=50 --filter is-official=true apache

docker search --filter stars=50 --filter is-automated=true apache

# Return the top 10 results (based on stars)
docker search --limit 10 apache	
```


### `docker pull`

```bash
docker pull docker.example.com/<image_path_and_name>

# Pull only latest
docker pull docker.example.com/examples/simple_image

docker pull docker.example.com/examples/simple_image:3.0

docker pull docker.example.com/examples/simple_image:3.0.0	

# Download all tagged images : -a or --all-tags
docker pull -a docker.example.com/examples/simple_image

# Skip image verification: --disable-content-trust=true  
docker pull --disable-content-trust docker.example.com/examples/simple_image
```


### `docker build`

```bash
# Skip image verification: --disable-content-trust=true  
docker build --disable-content-trust -t docker.example.com/examples/simple_image .
```

### `docker push`

```bash
# Skip image verification: --disable-content-trust=true  
docker push --disable-content-trust docker.example.com/examples/simple_image
```

### `docker-compose`

1. `docker-compose` allows you to define one or more containers in a single configuration file that
    can then be deployed all at once.


### `docker commit`

The `docker commit` command is used to take a container's build and commit it to the indicated image name.


```bash
docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]

# OPTIONS
# --author ,  -a		Author (e.g., “John Hannibal Smith hannibal@a-team.com”)
# --change ,  -c		Apply Dockerfile instruction to the created image
# --message , -m		Commit message
# --pause ,   -p	  true	Pause container during commit

# Commit a container
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS              NAMES
c3f279d17e0a        ubuntu:12.04        /bin/bash           7 days ago          Up 25 hours                            desperate_dubinsky

$ docker commit c3f279d17e0a  svendowideit/testimage:version3
f5283438590d

$ docker images
REPOSITORY                        TAG                 ID                  CREATED             SIZE
svendowideit/testimage            version3            f5283438590d        16 seconds ago      335.7 MB

# Commit a container with new configurations
$ docker ps
CONTAINER ID       IMAGE               COMMAND             CREATED             STATUS              PORTS              NAMES
c3f279d17e0a        ubuntu:12.04        /bin/bash           7 days ago          Up 25 hours                            desperate_dubinsky

$ docker inspect -f "{{ .Config.Env }}" c3f279d17e0a
[HOME=/ PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin]

$ docker commit --change "ENV DEBUG true" c3f279d17e0a  svendowideit/testimage:version3
f5283438590d

$ docker inspect -f "{{ .Config.Env }}" f5283438590d
[HOME=/ PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin DEBUG=true]

# Commit a container with new CMD and EXPOSE instructions
$ docker ps

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS              NAMES
c3f279d17e0a        ubuntu:12.04        /bin/bash           7 days ago          Up 25 hours                            desperate_dubinsky

$ docker commit --change='CMD ["apachectl", "-DFOREGROUND"]' -c "EXPOSE 80" c3f279d17e0a  svendowideit/testimage:version4
f5283438590d

$ docker run -d svendowideit/testimage:version4
89373736e2e7f00bc149bd783073ac43d0507da250e999f3f1036e0db60817c0

$ docker ps
CONTAINER ID        IMAGE               COMMAND                 CREATED             STATUS              PORTS              NAMES
89373736e2e7        testimage:version4  "apachectl -DFOREGROU"  3 seconds ago       Up 2 seconds        80/tcp             distracted_fermat
c3f279d17e0a        ubuntu:12.04        /bin/bash               7 days ago          Up 25 hours                            desperate_dubinsky

```
