# Docker Networking

1. **User-defined bridge networks** is the best network driver type when you need multiple containers to communicate on
   the same Docker host.

1. **Host networks** is the best network driver type when the network stack should not be isolated from the Docker host,
   but you want other aspects of the container to be isolated.

1. **Overlay networks** is the best network driver type when you need containers running on different Docker hosts to
   communicate, or when multiple applications work together using swarm services.

1. **Macvlan networks** is the best network driver type when you are migrating from a VM setup or need your containers
   to look like physical hosts on your network, each with a unique MAC address.


## User-defined bridge networks

User-defined bridges vs. default bridges

1. User-defined bridges provide better isolation and interoperability between containerised applications.
1. User-defined bridges provide automatic DNS resolution between containers.
1. Containers can be attached and detached from user-defined networks on the fly.
1. Each user-defined network creates a configurable bridge.
1. Linked containers on the default bridge network share environment variables.


## Overlay networks

https://docs.docker.com/network/overlay/

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

1. Overlay Network allows Docker Trusted Registry (DTR) components running on different nodes to communicate and replicate
   Docker Trusted Registry data.
   ```
   dtr-ol
   ```


## `docker network`

```bash
#############################################################################################################
# Create a network
docker network create	 [OPTIONS] NETWORK

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

1. When publishing a container/service's service ports (like HTTP port 80) to the underlying host(s) with the -P
   option, Docker will map the container ports to port numbers above port 32768 on the host.
   The -P option will map the ports in a container that is EXPOSED during its build to ports on a host with a port
   number higher than 32768.

### Routing mesh

1. Publishing a service's port using the **routing mesh** makes the service accessible at the published port on every
   swarm node.

1. The ability for any node in a cluster to answer for an exposed service port even if there is no replica for that
   service running on it, is handled by Routing Mesh.
   
1. The 'routing mesh' allows all nodes that participate in a Swarm for a given service to be aware of and capable of
   responding to any published service port request even if a node does not have a replica for said service running on it.


## Container Network Model (CNM)

https://blog.docker.com/2015/04/docker-networking-takes-a-step-in-the-right-direction-2/

1. Network Sandbox
   1. An isolated environment where the Networking configuration for a Docker Container lives.

1. Endpoint
   1. A network interface that can be used for communication over a specific network. Endpoints join exactly one network and multiple endpoints can exist within a single Network Sandbox.

1. Network
   1. A network is a uniquely identifiable group of endpoints that are able to communicate with each other. You could create a “Frontend” and “Backend” network and they would be completely isolated.

The CNM provides the following contract between networks and containers.

1. All containers on the same network can communicate freely with each other.
1. Multiple networks are the way to segment traffic between containers and should be supported by all drivers.
1. Multiple endpoints per container are the way to join a container to multiple networks.
1. An endpoint is added to a network sandbox to provide it with network connectivity.
