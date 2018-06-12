# Docker Orchestration

### Docker service

The Docker service can be managed via standard systemd service management utilities.

```bash
# Enable and start Docker CE (Ubuntu 16 or above)
systemctl enable docker && systemctl start docker

# Start docker service (Ubuntu 14)
sudo service docker start

# Query docker state (e.g. stopped or running)
systemctl status docker
```


### Docker Swarm

1. Docker swarm allows you to deploy clusters of Docker containers across multiple nodes and manage their behavior.

1. `docker-compose` allows you to define one or more containers in a single configuration file that can then be deployed all at once.


#### `docker swarm`

```bash
# Docker allows a node with the appropriate token to join the swarm indicated by the IP and port.
# A node to join the indicated cluster of the IP (of 10.0.1.100), with a token 'ighhsjkd6637'
docker swarm join --token ighhsjkd6637 10.0.1.100:2377

# Docker will display the necessary information for a manager or node to join a cluster during initialization. 
# This command will allow you to retrieve that information for subsequent joins.
# Retrieve the necessary information for a 'manager' node to join an existing cluster.
docker swarm join-token manager

# Docker provides the necessary command for any node to join upon creation. 
# The indicated command will allow you to redisplay that information for additional nodes to use.
# Retrieve the command needed for a node to join a cluster
docker swarm join-token worker

# When executed from the node you are removing, you can gracefully leave the cluster without having to use the NODE ID.
docker swarm leave
```

#### `docker node`

```bash
# The simple 'ls' command applied to the 'node' object from the manager provides a list of all nodes that the manager
# is aware of.
docker node ls

# Undo the 'drain' task applied to a node so that it can be used again for services.
# Once a node has been drained, it is marked DOWN and must be updated to ACTIVE status so that it's availability for
# services as advertised.
docker node update --availability active [NODE ID]

# Drain the indicated node so that future services will not run on it unless the command is undone (when run from the
# manager node).
# Docker updates the object (node) to DOWN when the availability is indicated to be 'drain' on the indicated NODE ID.
docker node update --availability drain [NODE ID]

# Remove a node marked as 'DOWN' from the cluster
docker node rm [NODE ID]

# When run on the manager node, this command will remove the indicated node from the swarm it is a member of.
docker node rm [NODE ID]
```

#### `docker service`

```bash
# When run on the master, list all the service processes running in a swarm
docker service ps

# Create a service called 'my_api' that contains three replicas from a service image called MYAPI:
docker service create --name my_api --replicas 3 MYAPI

# Create a service called 'my_api' as if it is being run on the manager node based on a locally installed image
# called 'httpd'.
docker service create --name my_api httpd

# Scale the number of replicas in your swarm to FIVE once the cluster is already running
# The 'scale' option allows you to indicate the service to scale along with the number of replicas to scale to.
docker service scale [SERVICE NAME]=5

# Scale your service, called 'my_api', from whatever its current replica count is to TEN replicas in the cluster
docker service scale my_api=10

# Stop a service called 'myweb' on your cluster
# Docker requires you to specify the 'service' object when removing a service rather than a single container from
# a host.
docker service rm myweb

# Remove a service called 'my_api' from the running swarm.
docker service rm my_api

# When executed on one of the master nodes, will display the logs for the indicated service running on the swarm.
docker service logs [SERVICE NAME]
```

#### `docker inspect` (or `docker container inspect`)


```bash
# The '--pretty' option will format the associated output in a more easily readable format.
# JSON, is thde default output from an inspect command.
docker inspect [NODE ID] --pretty

# There are multiple references to the key search term IP, but only one specifically called 'IPAddress' when running
# the 'inspect' command on any container.
docker inspect myweb | grep IPAddress

# The output will be formatted as to be more easily readable on standard output.
docker inspect --format="{{.Structure.To.Review}}" [objectid/name] myweb

# Show JUST the IP address of a running container called 'testweb'
docker container inspect --format="{{.NetworkSettings.Networks.bridge.IPAddress}" testweb
```