# Docker Installation and Configurations

## Configurations

### `docker info`

```bash
# Displays system wide configuration information as seen by the Docker service.
# e.g. see the storage driver Docker is currently using
docker info
```

### `docker0`

When Docker is first installed, the installation creates a network interface called `docker0` that functions as both:
 
1. the 'gateway' to the private network on the host, which is used for Docker container communication, 
1. defining the network range available for container IP assignments.

### Configuration files and directories

1. `/run/docker.sock` determines which accounts can use the service.
    1. `docker.sock` command is owned by `docker`.
    1. To add a user to this group (to allow them to run Docker commands with unprivileged accounts):
    
       `usermod -aG docker user`

1. `/run/docker.pid` file contains the PID (Process ID) of the Docker service when it is running.

1. `/etc/docker/daemon.json` file is used to override various Docker defaults, including
    1. the Docker logging driver (`log-driver`)
    1. the Docker storage driver (`storage-driver`)


1. `/var/lib/docker`: Storage related to Docker image and container layers are stored in `/var/lib/docker` on a host
   unless changed in the configuration or daemon at launch time.


#### `DOCKER_OPTS`

```bash
# Build a Docker image depending on another image from Docker registry.
# Edit "/etc/default/docker"
DOCKER_OPTS="--insecure-registry <docker registry url>"
```


## Installation notes

1. Which of the following is how to configure the Docker daemon to start on boot?

    1. Use `upstart` for Ubuntu 14.10 and below
    1. Use `systemd` for most current Linux distributions (RHEL, CentOS, Fedora, Ubuntu 16.04 and higher)

1. All major x86 based operating systems, and even some 'arm', support Docker, including

   1. Apple OSX/sierraOS
   1. Linux (all flavors)
   1. Microsoft Windows

1. The three major cloud providers support local image Docker installs as well as container services:

    1. AWS
    1. Azure
    1. Google

1. The following are requirements for Docker to run but are NOT installed as dependencies as they exist on most full
   system installations:

    1. `device-mapper-persistent-data`
    1. `lvm2`
    1. `yum-utils`

1. A virtual machine relies on some type of **hypervisor** that is responsible for translating calls from applications
   to the underlying hardware: storage, CPU, and memory requests.

1. Which of the following items need to be considered before installing Docker Enterprise?

    1. Docker Engine, DTR, and UCP version compatibility
    1. Disk space
    1. Time Synchronisation
    1. Network ports

