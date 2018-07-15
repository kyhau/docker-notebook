# Docker Networking

## Container Network Model (CNM)

REF: https://success.docker.com/article/networking

![Alt text](https://success.docker.com/api/images/.%2Frefarch%2Fnetworking%2Fimages%2Fcnm.png)

([Image source: docs.docker.com](https://docs.docker.com))

1. A **Sandbox** contains the configuration of a container's network stack. This includes management of the container's
   interfaces, routing table, and DNS settings. An implementation of a Sandbox could be a Linux Network Namespace, a
   FreeBSD Jail, or other similar concept. A Sandbox may contain many **endpoints** from multiple **networks**.

1. An **Endpoint** joins a **Sandbox** to a **Network**. The Endpoint construct exists so the actual connection to the
   network can be abstracted away from the application. This helps maintain portability so that a service can use
   different types of network drivers without being concerned with how it's connected to that network.

1. The CNM does not specify a **Network** in terms of the OSI model. An implementation of a Network could be a Linux
   bridge, a VLAN, etc. A Network is a collection of endpoints that have connectivity between them. 
   Endpoints that are not connected to a network do not have connectivity on a network.

### CNM provides the following contract between networks and containers

1. All containers on the same network can communicate freely with each other.
1. An endpoint is added to a network sandbox to provide it with network connectivity.
1. Multiple endpoints per container are the way to join a container to multiple networks.
1. Multiple networks are the way to segment traffic between containers and should be supported by all drivers.

### CNM Driver Interfaces

1. **Network Drivers (Native or Remote)**

    Docker Network Drivers provide the actual implementation that makes networks work.
    They are pluggable so that different drivers can be used and interchanged easily to support different use cases.
    
    Multiple network drivers can be used on a given Docker Engine or Cluster concurrently, but each Docker network
    is only instantiated through a single network driver.
       
    1. Native Network Drivers (see section below)
        1. `bridge`:  **User-defined bridge network** is the best network driver type when you need multiple
           containers to communicate on the same Docker host.
        
        1. `host`:  **Host network** is the best network driver type when the network stack should not be isolated
            from the Docker host, but you want other aspects of the container to be isolated.
        
        1. `overlay`:  **Overlay network** is the best network driver type when you need containers running on
            different Docker hosts to communicate, or when multiple applications work together using swarm services.
        
        1. `macvlan`:  **Macvlan network** is the best network driver type when you are migrating from a VM setup or
           need your containers to look like physical hosts on your network, each with a unique MAC address.
        
        1. `none`:  The `none` driver gives a container its own networking stack and network namespace but does not
            configure interfaces inside the container. Without additional configuration, the container is completely
            isolated from the host networking stack.

    1. Remote Network Drivers
        1. `contiv`:  An open source network plugin led by Cisco Systems to provide infrastructure and security policies for multi-tenant microservices deployments. Contiv also provides integration for non-container workloads and with physical networks, such as ACI. Contiv implements remote network and IPAM drivers.
        1. `weave`:  A network plugin that creates a virtual network that connects Docker containers across multiple hosts or clouds. Weave provides automatic discovery of applications, can operate on partially connected networks, does not require an external cluster store, and is operations friendly.
        1. `calico`:  An open source solution for virtual networking in cloud datacenters. It targets datacenters where most of the workloads (VMs, containers, or bare metal servers) only require IP connectivity. Calico provides this connectivity using standard IP routing. Isolation between workloads — whether according to tenant ownership or any finer grained policy — is achieved via iptables programming on the servers hosting the source and destination workloads.
        1. `kuryr`:  A network plugin developed as part of the OpenStack Kuryr project. It implements the Docker networking (libnetwork) remote driver API by utilizing Neutron, the OpenStack networking service. Kuryr includes an IPAM driver as well.
   
1. **IPAM Drivers (IP Address Management Drivers)**

    Docker has a native IP Address Management Driver that provides default subnets or IP addresses for networks and
    endpoints if they are not specified. 

     1. Native IPAM Drivers
     
     1. Remote IPAM Drivers
         1. `infoblox`:  An open source IPAM plugin that provides integration with existing Infoblox tools.


## Default bridge network

1. On any host running Docker Engine, there is, by default, a local Docker network named `bridge`. 
   This network is created using a **bridge network driver** which instantiates a Linux bridge called `docker0`; i.e.

    1. `bridge` is the name of the Docker network.
    1. `bridge` is the network driver, or template, from which this network is created.
    1. `docker0` is the name of the Linux bridge that is the kernel building block used to implement this network.

1. `docker0` is the network interace that functions as both:
 
    1. the 'gateway' to the private network on the host, which is used for Docker container communication, 
    1. defining the network range available for container IP assignments.


## User-defined bridges vs. default bridges

1. Each user-defined network creates a configurable bridge.
1. Containers can be attached and detached from user-defined networks on the fly.
1. User-defined bridges provide automatic DNS resolution between containers.
1. User-defined bridges provide better isolation and interoperability between containerised applications.
1. Linked containers on the default bridge network share environment variables.


## Overlay networks

REF: https://docs.docker.com/network/overlay/

1. The overlay network driver creates a distributed network among multiple Docker daemon hosts. This network sits on
   top of (overlays) the host-specific networks, allowing containers connected to it (including swarm service
   containers) to communicate securely. Docker transparently handles routing of each packet to and from the correct
   Docker daemon host and the correct destination container.

1. When you initialize a swarm or join a Docker host to an existing swarm, two new networks are created on that Docker
   host:

   1. an overlay network called `ingress`, which handles control and data traffic related to swarm services. When you
      create a swarm service and do not connect it to a user-defined overlay network, it connects to the ingress
      network by default.
   1. a bridge network called `docker_gwbridge`, which connects the individual Docker daemon to the other daemons
      participating in the swarm.

1. Overlay networks require some pre-existing conditions before you can create one. These conditions are:
   1. Access to a key-value store. Engine supports Consul, Etcd, and ZooKeeper (Distributed store) key-value stores.
   1. A cluster of hosts with connectivity to the key-value store.
   1. A properly configured Engine daemon on each host in the cluster.

1. The `dockerd` options that support the overlay network are:
   1. `--cluster-store`
   1. `--cluster-store-opt`
   1. `--cluster-advertise`

1. Overlay Network allows Docker Trusted Registry (DTR) components running on different nodes to communicate and
   replicate Docker Trusted Registry data.
   ```
   dtr-ol
   ```

1. Which of the built-in network types has 'swarm' level scope?

   The overlay network handles routing of services for the swarm and thus has swarm level scope across all nodes.


## Host networks

1. Which of the built-in network drivers is often referred to as the 'Host Only' network driver?

    The 'host' network driver is referred to as the 'host only' network driver because the host is the only entity that
    will have network connectivity to the resources on it.


## IP address and hostname

1. When the container starts, it can only be connected to a single network, using `--network`.

1. However, you can connect a running container to multiple networks using `docker network connect`.

1. When you start a container using the `--network` flag, you can specify the IP address assigned to the container on
   that network using the `--ip` or `--ip6` flags.

1. When you connect an existing container to a different network using `docker network connect`, you can use the `--ip`
   or `--ip6` flags on that command to specify the container’s IP address on the additional network.

1. In the same way, a container’s hostname defaults to be the container’s name in Docker. You can override the hostname
   using `--hostname`. 
   
1. When connecting to an existing network using `docker network connect`, you can use the `--alias` flag to specify an
   additional network alias for the container on that network.


## `docker network`

```bash
#############################################################################################################
# Create a network
docker network create [OPTIONS] NETWORK

# The 'docker network create' command can take a network, subnet and gateway as arguments for either bridge
# or overlay drivers.
# --driver|-d:  accepts `bridge` or `overlay` (built-in network drivers); `bridge` if not specified

# Create a bridge network "my-bridge-network"
docker network create -d bridge my-bridge-network
# or
docker network create my-bridge-network

# Create a new overlay network "dev_overlay" to the cluster with a particular network range and gateway. 
docker network create --driver=overlay --subnet=192.168.1.0/24 --gateway 192.168.1.250 dev_overlay

#############################################################################################################
# Connect a container to a network; 
# options: --alias, --ip, --ip6, --link, --link-local-ip 
docker network connect [OPTIONS] NETWORK CONTAINER

# To connect a running container "my-nginx" to an existing user-defined bridge "my-net"
docker network connect my-net my-nginx
# OR
docker create --name my-nginx --network my-net --publish 8080:80 nginx:latest

#############################################################################################################
# Disconnect a container from a network; options: --force|-f
docker network disconnect	 [OPTIONS] NETWORK CONTAINER

# To disconnect a running container "my-nginx" from an existing user-defined bridge "my-net"
docker network disconnect my-net my-nginx

#############################################################################################################
# Display detailed information on one or more networks; options: --format|-f, --verbose|-v 
docker network inspect	[OPTIONS] NETWORK [NETWORK...]

#############################################################################################################
# List networks; options: --filter|-f, --format, --no-trunc, --quiet|-q
docker network ls	 [OPTIONS]   

# The 'ls' command for the 'docker network' object will list all Docker networks and their drivers installed.
$ docker network ls

NETWORK ID          NAME                DRIVER              SCOPE
aa075c363cae        bridge              bridge              local
84bba7e0b175        host                host                local
926c02ac0dc5        none                null                local

#############################################################################################################
# Remove all unused networks; options: --filter, --force|-f
docker network prune [OPTIONS]

#############################################################################################################
# Remove one or more networks
docker network rm	 NETWORK [NETWORK...] 
```


## Port mapping and publishing

1. The following docker command can be used to find out all the ports mapped:
   1. `docker inspect`
   1. `docker port`
   1. `docker ps`

1. The docker run option to publish a port so that an application is accessible externally
   1. `docker run --publish`

1. When publishing a container/service's service ports (like HTTP port 80) to the underlying host(s) with the `-P`
   option, Docker will map the container ports to port numbers above port **32768** on the host.

   The `-P` option will map the ports in a container that is EXPOSED during its build to ports on a host with a port
   number higher than *32768*.

### Routing mesh

1. Publishing a service's port using the **routing mesh** makes the service accessible at the published port on every
   swarm node.

1. The ability for any node in a cluster to answer for an exposed service port even if there is no replica for that
   service running on it, is handled by Routing Mesh.
   
1. The 'routing mesh' allows all nodes that participate in a Swarm for a given service to be aware of and capable of
   responding to any published service port request even if a node does not have a replica for said service running on it.


## DNS Services

1. By default, a container inherits the DNS settings of the Docker daemon, including the `/etc/hosts` and
   `/etc/resolv.conf`.

1. Set the DNS server for all Docker containers.

    ```bash
    # To set the DNS server for all Docker containers, use:
    $ sudo dockerd --dns 8.8.8.8
    
    # To set the DNS search domain for all Docker containers, use:
    $ sudo dockerd --dns-search example.com
    ```

1. You can override these settings on a **per-container** basis.

    ```bash
    # Use the --dns option to override the default DNS server when creating a container.
    docker container create --dns=IP_ADDRESS ...
    
    # The 'docker run' command uses the --dns option to override the default DNS servers for a container.
    docker run -d --dns=8.8.8.8 IMAGE_NAME
    
    --dns IP_ADDRESS
        The IP address of a DNS server. To specify multiple DNS servers, use multiple --dns flags. If the
        container cannot reach any of the IP addresses you specify, Google’s public DNS server 8.8.8.8 is
        added, so that your container can resolve internet domains.
    
    --dns-search
        A DNS search domain to search non-fully-qualified hostnames. To specify multiple DNS search
        prefixes, use multiple --dns-search flags.
    
    --dns-opt
        A key-value pair representing a DNS option and its value. See your operating system’s documentation
        for resolv.conf for valid options.
    
    --hostname
        The hostname a container uses for itself. Defaults to the container’s name if not specified.
    ```
