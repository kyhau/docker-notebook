# Docker Overview

REF: https://docs.docker.com/engine/docker-overview/#docker-engine

## Docker Engine

Docker Engine is a client-server application with these major components:

1. A server which is a type of long-running program called a daemon process (the `dockerd` command).

1. A REST API which specifies interfaces that programs can use to talk to the daemon and instruct it what to do.

1. A command line interface (CLI) client (the `docker` command).

![docker-grant](https://docs.docker.com/engine/images/architecture.svg)

([Image source: docs.docker.com](https://docs.docker.com))

1. The **Docker daemon** (`dockerd`) listens for Docker API requests and manages Docker objects such as images, containers,
   networks, and volumes. A daemon can also communicate with other daemons to manage Docker services.

1. The **Docker client** (`docker`) is the primary way that many Docker users interact with Docker. When you use commands
   such as `docker run`, the client sends these commands to `dockerd`, which carries them out. The `docker` command
   uses the Docker API. The Docker client can communicate with more than one daemon.

1. A **Docker registry** stores Docker images. 

    1. **Docker Hub** and **Docker Cloud** are public registries that anyone can use, and Docker is configured to look
       for images on **Docker Hub** by default.
       
    1. You can even run your own private registry. If you use **Docker Datacenter (DDC)**, it includes **Docker Trusted
       Registry (DTR)**. See [docker-dtr.md](docker-dtr.md).

    1. When you use the `docker pull` or `docker run` commands, the required images are pulled from your configured
       registry. When you use the `docker push` command, your image is pushed to your configured registry.
       
1. **Docker store** allows you to buy and sell Docker images or distribute them for free.


## Swarm

1. Docker Swarm is a cluster management and deployment system. See [docker-orchestration.md](docker-orchestration.md).


## Services

1. Services allow you to scale containers across multiple Docker daemons, which all work together as a **swarm** with
   multiple **managers** and **workers**.
   
1. Each member of a swarm is a Docker daemon, and the daemons all communicate using the Docker API. 

1. A service allows you to define the desired state, such as the number of replicas of the service that must be
   available at any given time. By default, the service is load-balanced across all worker nodes. 
   
1. To the consumer, the Docker service appears to be a single application. 
   
1. Docker Engine supports swarm mode in Docker 1.12 and higher.

See [docker-orchestration.md](docker-orchestration.md).


## Namespaces - provide security and isolation

1. Docker uses a technology called **namespaces** to provide the isolated workspace called the **container**.
   When you run a container, Docker creates a set of **namespaces** for that container.

1. These namespaces provide a layer of isolation. Each aspect of a container runs in a separate namespace and its
   access is limited to that namespace.

1. Docker Engine uses namespaces such as the following on Linux:

    1. The `pid` namespace: Process isolation (PID: Process ID).
    1. The `net` namespace: Managing network interfaces (NET: Networking).
    1. The `ipc` namespace: Managing access to IPC resources (IPC: InterProcess Communication).
    1. The `mnt` namespace: Managing filesystem mount points (MNT: Mount).
    1. The `uts` namespace: Isolating kernel and version identifiers. (UTS: Unix Timesharing System).

1. The `PID` and `Network` namespaces mean that each container is isolated in terms of them, which maintains the
   isolation and separation of the container processes from underlying host services.


## Control groups (`cgroups`) - provide resource management and reporting

1. Docker Engine on Linux also relies on another technology called **control groups (`cgroups`)**. 

1. A cgroup limits an application to a specific set of resources. 

1. Control groups allow Docker Engine to share available hardware resources to containers and optionally enforce limits
   and constraints.
   
   For example, you can limit the memory available to a specific container.

1. Which of the following resource limitation options, when added to a container instantiation, is representative of a
   'Control Group (`cgroup`)'?

    1. `--memory=[amount b/k/m/g]`
    1. `--cpus=[value]`

    ```bash
    # If you have 2 CPUs, guarantee the container at most at most one and a half of the CPUs every second.
    # Docker 1.13 and higher. Docker 1.12 and lower uses --cpu-period=100000 --cpu-quota=50000
    docker run -it --cpus="1.5" ubuntu /bin/bash
    
    # The maximum amount of memory the container can use. If you set this option, the minimum allowed value is 4m
    # (4 megabyte).
    docker run -it --memory=[amount b/k/m/g] ubuntu /bin/bash
    ```


## Union file systems (UnionFS)

1. Union file systems, or UnionFS, are file systems that operate by creating layers, making them very lightweight and
   fast.
   
1. Docker Engine uses UnionFS to provide the building blocks for containers.

1. Docker Engine can use multiple UnionFS variants, including AUFS, btrfs, vfs, and DeviceMapper.


## Container format

1. Docker Engine combines the **namespaces**, **control groups**, and **UnionFS** into a wrapper called a **container
   format**. 

1. The default container format is **`libcontainer`**.
