# Docker Installation, Configurations, Storage and Volumes


### Configuration commands

```bash
# Displays system wide configuration information as seen by the Docker service.
docker info
```


### Configurations

#### `docker0`

When Docker is first installed, the installation creates a network interface called `docker0` that functions as both:
 
1. the 'gateway' to the private network on the host, which is used for Docker container communication, 
1. defining the network range available for container IP assignments.


#### Configuration files and directories

##### `/run/docker.sock`

- Determine which accounts can use the service.
- `docker.sock` command is owned by `docker`.
- To add a user to this group (to allow them to run Docker commands with unprivileged accounts):
    ```bash
    usermod -aG docker user
    ```

##### `/run/docker.pid`

- Contain the PID (Process ID) of the Docker service when it is running.


##### `/etc/docker/daemon.json`

- The `/etc/docker/daemon.json` file is used to override various Docker defaults, including

   1. the Docker logging driver
   1. the Docker storage driver


##### `/var/lib/docker`

- Storage related to Docker image and container layers are stored in `/var/lib/docker` on a host unless
  changed in the configuration or daemon at launch time.


#### `DOCKER_OPTS`

```bash
# Build a Docker image depending on another image from Docker registry.
# Edit "/etc/default/docker"
DOCKER_OPTS="--insecure-registry <docker registry url>"
```



### Installation notes

1. The following are requirements for Docker to run but are NOT installed as dependencies as they exist on most full
    system installations.

    1. `device-mapper-persistent-data`
    1. `lvm2`
    1. `yum-utils`
