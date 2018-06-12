# Docker Networking

```bash

# When publishing a container/service's service ports (like HTTP port 80) to the underlying host(s) with the -P option,
# Docker will map the container ports to port numbers above port 32768 on the host.
# The -P option will map the ports in a container that is EXPOSED during its build to ports on a host with a port
# number higher than 32768.

# The overlay network handles routing of services for the swarm and thus has swarm level scope across all nodes.
Overlay

# Which of the following built-in network drivers is often referred to as the 'Host Only' network driver?
# The 'host' network driver is referred to as the 'host only' network driver because the host is the only entity that
# will have network connectivity to the resources on it.
host
```
