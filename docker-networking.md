# Docker Networking


#### `docker network`

```bash
# The 'ls' command for the 'docker network' object will list all Docker networks and their drivers installed.
docker network ls

# Add a new overlay network (dev_overlay) to the cluster with a particular network range and gateway. 
# The 'docker network create' command can take a network, subnet and gateway as arguments for either bridge or
# overlay drivers.
docker network create --driver=overlay --subnet=192.168.1.0/24 --gateway 192.168.1.250 dev_overlay
```

```bash
# When publishing a container/service's service ports (like HTTP port 80) to the underlying host(s) with the -P
# option, Docker will map the container ports to port numbers above port 32768 on the host.
# The -P option will map the ports in a container that is EXPOSED during its build to ports on a host with a port
# number higher than 32768.

# The overlay network handles routing of services for the swarm and thus has swarm level scope across all nodes.
Overlay

# Which of the following built-in network drivers is often referred to as the 'Host Only' network driver?
# The 'host' network driver is referred to as the 'host only' network driver because the host is the only entity
# that will have network connectivity to the resources on it.
host
```

#### Routing mesh

1. The ability for any node in a cluster to answer for an exposed service port even if there is no replica for that
 service running on it, is handled by Routing Mesh.
1. The 'routing mesh' allows all nodes that participate in a Swarm for a given service to be aware of and capable of
 responding to any published service port request even if a node does not have a replica for said service running on it.
