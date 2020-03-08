# Docker notebook

Subpages
- [Docker Overview - Docker Engine, dockerd, namespaces, cgroups, UnionFD](docker-overview.md)
- [Installation and Configurations](docker-configurations.md)
- [Dockerfile](docker-dockerfile.md)
- [Storage and Volumes](docker-storage-and-volumes.md)
- [Orchestration - Swarm, Node, Service, Docker Secrets, Docker Configs](docker-orchestration.md)
- [Networking](docker-networking.md)
- [Docker Trusty Registry (DTR), Image Signing](docker-dtr.md)
- [Universal Control Plane (UCP), Manager, Worker, Pause Containers](docker-ucp.md)
- [Docker Secrets and Docker Config](docker-secrets-and-config.md)
- [Security - RBAC, Image Signing, Image Scanning](docker-security.md)
- [Backups and disaster Recovery](docker-backup.md)
- [Docker upgrade](docker-upgrade.md)
- Python examples: [docker_checker](docker_checker/README.md)

Best practice
- [Docker development best practices](https://docs.docker.com/develop/dev-best-practices/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Intro Guide to Dockerfile Best Practices](https://www.docker.com/blog/intro-guide-to-dockerfile-best-practices/)

Other references:
- [Docker Advanced multi-stage build patterns – Tõnis Tiigi](
  https://medium.com/@tonistiigi/advanced-multi-stage-build-patterns-6f741b852fae)
- [Docker ARG, ENV and .env - a Complete Guide](https://vsupalov.com/docker-arg-env-variable-guide/)


## Cheat Sheet

[Docker cheat sheet (2019-09)](https://www.docker.com/sites/default/files/d8/2019-09/docker-cheat-sheet.pdf)

### Running container

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

# Start a container from the image 'centos:6'; it will exit immediately.
docker run centos:6

# Start a container from the image 'httpd:latest' in background (--detach|-d) and print the container ID.
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

# --expose        :  Expose a port or a range of ports; does not actually publish the port
# --publish|-p    :  Publish a container’s port(s) to the host
# --publish-all|-P:  Publish all exposed ports to random ports

# This binds port 8080 of the container to TCP port 80 on 127.0.0.1 of the host machine.
# You can also specify udp and sctp ports. 
docker run -p 127.0.0.1:80:8080/tcp ubuntu bash

# This exposes port 80 of the container without publishing the port to the host system’s interfaces.
docker run --expose 80 ubuntu bash

# Instantiate a docker container called 'myweb' that is running an Apache web server on port 80 by default within
# it, you can allow direct access to the container service via the host's IP by redirecting the container port 80
# to the host port 80. Redirecting ports is through the '-p [host port]:[container port]' syntax.
docker run -d --name myweb -p 80:80 httpd:latest

# Instantiate a container called 'myweb' running an Apache application from the image 'httpd:latest' on your
# system, and allow the container port 80 to be redirected to the underlying host's port somewhere in the range
# of 80-85, based on port availability.
docker run -d --name myweb -p 80-85:80 httpd:latest

# Note: To specify container name, use '--name'. Note that '--name' has no short form ('-n' is not valid).

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

# Processes in container can be executed on cpu 1 and cpu 3.
docker run -it --cpuset-cpus="1,3" ubuntu:14.04 /bin/bash

# Processes in container can be executed on cpu 0, cpu 1 and cpu 2.
docker run -it --cpuset-cpus="0-2" ubuntu:14.04 /bin/bash

# The maximum amount of memory the container can use. If you set this option, the minimum allowed value is 4m
# (4 megabyte).
docker run -it --memory=[amount b/k/m/g] ubuntu /bin/bash

# If --memory and --memory-swap are set to the same value, this prevents containers from using any swap. This is
# because --memory-swap is the amount of combined memory and swap that can be used, while --memory is only the
# amount of physical memory that can be used.
docker run -it --memory=[amount b/k/m/g] --memory-swap=[amount b/k/m/g] ubuntu /bin/bash

# This example restricts the processes in the container to only use memory from memory nodes 1 and 3.
docker run -it --cpuset-mems="1,3" ubuntu:14.04 /bin/bash

# This example restricts the processes in the container to only use memory from memory nodes 0, 1 and 2.
$ docker run -it --cpuset-mems="0-2" ubuntu:14.04 /bin/bash

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

# Force removal of an image with --force|-f (e.g. remove an image with containers based on it)
docker rmi IMAGE_NAME --force

# Do not delete untagged parents
docker rmi IMAGE_NAME --no-prune

# Remove all non-running containers (filters: created, restarting, running, paused, exited)
docker rm $(docker ps -q -f status=exited)

# Remove container by container name or container ID
docker rm <CONTAINER_NAME or CONTAINER_ID>
```


### `docker ps`

```bash
# List all containers (both running or not running): --all|-a
docker ps -a

# --filter|-f  : Filter output: 
# --last int|-n int : Show n last created containers (default -1)
# --latest|-l  : Show the latest created container (includes all states)
# --no-trunc   : Don't truncate output
# --quiet|-q   : Only display numeric IDs

# Display total file size: --size|-s
# The column ‘size’ shows the amount of data that is used for the writable layer of each container.
# The column ‘virtual size’ shows the amount of data used for the read-only image data used by the container
# plus the container’s writable layer ‘size’.
docker ps -s
```

### `docker images`

```bash
# List the locally installed images that can be used to instantiate containers from
docker images
> REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
> image1              latest              eeae25ada2aa        4 minutes ago        188.3 MB
> image2              uclibc              dea752e4e117        9 minutes ago        188.3 MB
> image3              glibc               511136ea3c5a        25 minutes ago       188.3 MB

# Show untagged images (dangling)
docker images --filter "dangling=true"

# Filter image by time: --filter|-f
docker images --filter "before=image1"
> image2              uclibc              dea752e4e117        9 minutes ago        188.3 MB
> image3              glibc               511136ea3c5a        25 minutes ago       188.3 MB

docker images --filter "since=image3"
> image1              latest              eeae25ada2aa        4 minutes ago        188.3 MB
> image2              uclibc              dea752e4e117        9 minutes ago        188.3 MB

# Filter with `reference`
docker images --filter=reference='image*:*libc'
> image2              uclibc              dea752e4e117        9 minutes ago        188.3 MB
> image3              glibc               511136ea3c5a        25 minutes ago       188.3 MB

# Show image with the give label
docker images --filter "label=com.example.version"
docker images --filter "label=com.example.version=1.0"

# List all locally installed images including intermediate images and dangling images: -a|--all
docker images -a

# List the full length of image IDs
docker images --no-trunc
> REPOSITORY                   TAG     IMAGE ID                                                                  CREATED             SIZE
> <none>                       <none>  sha256:77af4d6b9913e693e8d0b4b294fa62ade6054e6b2f1ffb617ac955dd63fb0182   19 hours ago        1.089 GB
> committest                   latest  sha256:b6fa739cedf5ea12a620a439402b6004d057da800f91c7524b5086a5e4749c9f   19 hours ago        1.089 GB

# List image digests
docker images --digests
> REPOSITORY                   TAG     DIGEST                                                                    IMAGE ID            CREATED             SIZE
> localhost:5000/test/busybox  <none>  sha256:cbbf2f9a99b47fc460d422812b6a5adff7dfee951d8fa2e4a98caa0382cfbdbf   4986bf8c1536        9 weeks ago         2.43 MB

# Show only numeric ID: --quiet|-q
docker images -f "dangling=true" -q
> 8abc22fbb042

# Format the output: --format
# Placeholders: .ID, .Repository, .Tag, .Digest, .CreatedSince, .CreatedAt, .Size

docker images --format "{{.ID}}: {{.Repository}}"
> 30557a29d5ab: docker
> 5ed6274db6ce: <none>
> 746b819f315e: postgres
> 746b819f315e: postgres

# To list all images with their repository and tag in a "table" format
$ docker images --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}"
> IMAGE ID            REPOSITORY                TAG
> 30557a29d5ab        docker                    latest
> 5ed6274db6ce        <none>                    <none>
> 746b819f315e        postgres                  9
> 746b819f315e        postgres                  9.3
```


### `docker image`

New way to do docker image commands (make it clearer).

```bash
docker image COMMAND

# Display detailed information on one or more images
docker image inspect IMAGE_ID

# Build an image from a Dockerfile
docker image build [OPTIONS] PATH | URL | -

# Import the contents from a tarball to create a filesystem image
docker image import [--change|-c DOCKERFILE_INSTRUCTION] [--message|-m COMMIT_MESSAGE] [REPOSITORY[:TAG]]

# Load an image from a tar archive or STDIN
docker image load [--input|-i TAR] [--quiet|-q]

# Save one or more images to a tar archive (streamed to STDOUT by default)
docker image save [--output|-o FILE] IMAGE [IMAGE...]

# Create a backup that can then be used with docker load.
docker save busybox > busybox.tar
# OR
docker save --output busybox.tar busybox
# OR
docker save -o fedora-all.tar fedora
# OR
docker save -o fedora-latest.tar fedora:latest
```


### `docker container`

New way to do docker container commands (make it clearer).

```bash
# New way to do `docker ps`
docker container ls

# Create a new container
docker create [OPTIONS] IMAGE [COMMAND] [ARG...]
# OR
docker container create [OPTIONS] IMAGE [COMMAND] [ARG...]

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

1. `docker inspect` returns low-level information on Docker objects (e.g. container, node, etc.)
   (e.g. current logging driver for a running container). 

1. Default format of `docker inspect` is **json**.

```bash
# Examples of `docker inspect` on containers 

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
docker history [OPTIONS] IMAGE_ID

# --format:  Pretty-print images using a Go template
# --human|-H:  Print sizes and dates in human readable format; default is true
# --no-trunc:  Don’t truncate output
# --quiet|-q:  Only show numeric IDs

# To see how many layers in the image
docker history mywebserver:v1 | wc -l
> 12
```


### `docker logs`

```bash
# Fetch the logs of a container
docker logs [OPTIONS] CONTAINER

# --details:  Show extra details provided to logs
# --follow|-f:  Follow log output
# --since:  Show logs since timestamp (e.g. 2013-01-02T13:23:37) or relative (e.g. 42m for 42 minutes)
# --tail:  Number of lines to show from the end of the logs; default is `all1
# --timestamps|-t:  Show timestamps
# --until:  Show logs before a timestamp (e.g. 2013-01-02T13:23:37) or relative (e.g. 42m for 42 minutes)
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
# When the Dockerfile is in the current context (directory), you build it with an image name and tag with the
# --tag|-t option followed by the image:tag and the directory context of the file, in this case '.'.
docker build -t docker.example.com/examples/simple_image:v1 .

# --file|-f Name of the Dockerfile
docker build -t docker.example.com/examples/simple_image:v1 -f PATH_TO/Dockerfile

# Skip image verification: --disable-content-trust=true  
docker build --disable-content-trust -t docker.example.com/examples/simple_image .
```


### `docker tag`

```bash
# Tag an image referenced by Name, ImageID, Name:Tag
docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
```


### `docker login`

```bash
# Log in to a Docker registry
docker login [OPTIONS] [SERVER]

# OPTIONS:
# --username|-u:  Username
# --password|-p:  Password
# --password-stdin:  Take the password from stdin

docker login dtr.example.org

docker login dtr.example.org -u kay -p xxxxxx
```


### `docker push`

```bash
docker push [OPTIONS] NAME[:TAG]

# OPTIONS:
#   --disable-content-trust	:  Skip image signing; default is `true`.

# Skip image verification: --disable-content-trust=true  
docker push --disable-content-trust docker.example.com/examples/simple_image
```

### `docker-compose`

`docker-compose` allows you to define one or more containers in a single configuration file that
    can then be deployed all at once.

`docker-compose [-f <arg>...] [options] [COMMAND] [ARGS...]`


### `docker commit`

`docker commit` creates a new image from a container's change. It can be useful to commit a container’s file changes or
settings into a new image. 


```bash
docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]

# OPTIONS
# --author|-a	  Author (e.g., “John Hannibal Smith hannibal@a-team.com”)
# --change|-c   Apply Dockerfile instruction to the created image
# --message|-m  Commit message
# --pause|-p    Pause container during commit; default is `true`

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
