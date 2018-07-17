# Docker Installation and Configurations

## Installation notes

1. All major x86 based operating systems, and even some 'arm', support Docker, including

   1. Apple OSX/sierraOS
   1. Linux (all flavors)
   1. Microsoft Windows

1. The three major cloud providers support local image Docker installs as well as container services:

    1. AWS
    1. Azure
    1. Google

1. How to configure the Docker daemon to start on boot (on Ubuntu)

    1. Use `upstart` for Ubuntu 14.10 and below
    1. Use `systemd` for most current Linux distributions (RHEL, CentOS, Fedora, Ubuntu 16.04 and higher)

1. The following are requirements for Docker to run but are NOT installed as dependencies as they exist on most full
   system installations:

    1. `device-mapper-persistent-data`
    1. `lvm2`
    1. `yum-utils`

1. What does a virtual machine directly rely on that a container does not?

   **Hypervisor**. A virtual machine relies on some type of **hypervisor** that is responsible for translating calls
   from applications to the underlying hardware: storage, CPU, and memory requests.

1. Which of the following items need to be considered before installing Docker Enterprise?

    1. Docker Engine, DTR, and UCP version compatibility
    1. Disk space
    1. Network ports
    1. Time Synchronisation

1. `docker info` displays system wide configuration information as seen by the Docker service.

    e.g. See the storage driver Docker is currently using

1. When Docker is first installed, the installation creates a network interface called **`docker0`** that functions as
   both:
 
    1. the 'gateway' to the private network on the host, which is used for Docker container communication, 
    1. defining the network range available for container IP assignments.

    See also **Default bridge network** in [docker-networking.md](docker-networking.md).


## Configurations files and directories

1. `/run/docker.sock` file determines which accounts can use the service.

    1. `docker.sock` command is owned by `docker`.
    1. To add a user to this group (to allow them to run Docker commands with unprivileged accounts):
    
       `usermod -aG docker user`

1. `/run/docker.pid` file contains the PID (Process ID) of the Docker service when it is running.

1. `/etc/docker/daemon.json` file is used to override various Docker defaults, including

    1. the Docker logging driver (`log-driver`)
    1. the Docker storage driver (`storage-driver`)

1. `/var/lib/docker` is the directory on a host, stores Docker image and container layers;
   unless changed in the configuration or daemon at launch time.

 
### Running an Insecure Docker Registry
 
On Ubuntu 14.x:

1. Edit `/etc/default/docker` file
    ```bash
    # for a registry running on port 80 on example.com.
    DOCKER_OPTS="--insecure-registry registry.example.com -H tcp://127.0.0.1:2375 -H unix:///var/run/docker.sock"
    ```

2. `sudo service docker restart`

On Ubuntu 16.x and CentOS:

1. Edit `/etc/docker/daemon.json` file
    ```bash
    {
        "insecure-registries" : ["registry.example.com"]
    }
    ```

2. `sudo systemctl restart docker`
