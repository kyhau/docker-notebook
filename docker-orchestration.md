# Docker Orchestration

### Docker service

The Docker service can be managed via standard systemd service management utilities.

```bash
# Enable and start Docker CE (Ubuntu 16 or above)
systemctl enable docker && systemctl start docker

# Start docker service (Ubuntu 14)
service docker start
# OR (Ubuntu 16+)
systemctl start docker

# Query docker state (e.g. stopped or running) (Ubuntu 14)
service docker status
# OR (Ubuntu 16+)
systemctl status docker
```


### Docker Swarm

1. Docker swarm allows you to deploy clusters of Docker containers across multiple nodes and manage their behavior.

1. Two types of Docker Swarm Services
    1. **Replicated**: Number of identical tasks can be specified for a replicated service.
    1. **Global**: There is no pre-specified number of tasks for global service.

1. **Raft** (**Docker Consensus Algorithm**)
   1. In Docker swarm mode, manager nodes implement the Raft Consensus Algorithm to manage the global cluster state.
   1. The consensus algorithm is to make sure that all the manager nodes that are in charge of managing and scheduling
      tasks in the cluster, are storing the same consistent state.
   1. Raft requires a majority or quorum of (N/2)+1 members to agree on values proposed to the cluster.
   1. Raft tolerates up to (N-1)/2 failures.
   1. If a quorum is not reached, the existing tasks will keep running.
   1. If a quorum is not reached, the system will not process any more requests to schedule additional tasks.

This means that in a cluster of 5 Managers running Raft, if 3 nodes are unavailable, the system cannot process any
more requests to schedule additional tasks. The existing tasks keep running but the scheduler cannot rebalance tasks
to cope with failures if the manager set is not healthy.


#### `docker swarm`

```bash
# Set up a swarm
docker swarm init [OPTIONS]

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

# When executed from the node you are removing, you can gracefully leave the cluster without having to use the
# NODE ID.
docker swarm leave

# Enable autolock on an existing swarm cluster
docker swarm update --autolock=true
```

#### `docker node`

```bash
# The simple 'ls' command applied to the 'node' object from the manager provides a list of all nodes that the
# manager is aware of.
docker node ls

# Undo the 'drain' task applied to a node so that it can be used again for services.
# Once a node has been drained, it is marked DOWN and must be updated to ACTIVE status so that it's availability
# for services as advertised.
docker node update --availability active [NODE_ID]

# Drain the indicated node so that future services will not run on it unless the command is undone (when run from
# the manager node).
# Docker updates the object (node) to DOWN when the availability is indicated to be 'drain' on the indicated NODE
# ID.
docker node update --availability drain [NODE_ID]

# Add or update multiple node labels of the node `worker1`
docker node update --label-add foo --label-add bar worker1

# Remove a node marked as 'DOWN' from the cluster
docker node rm [NODE_ID]

# When run on the manager node, this command will remove the indicated node from the swarm it is a member of.
docker node rm [NODE_ID]
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
docker service scale [SERVICE_NAME]=5

# Scale your service, called 'my_api', from whatever its current replica count is to TEN replicas in the cluster
docker service scale my_api=10

# Roll back to the previous version of a service
docker service update --rollback [SERVICE_NAME]

# Add or update a mount on a service
docker service update --mount-add ... [SERVICE_NAME]

# Add a network to a service
docker service update --network-add ... [SERVICE_NAME]

# Add or update a published port
docker service update --publish-add ... [SERVICE_NAME]

# Add or update a placement constraint to the service 'redis'
docker service update --constraint-add "engine.labels.purpose==database" redis

# Add or update a placement preference
docker service update --placement-pref-add ... [SERVICE_NAME]

# Stop a service called 'myweb' on your cluster
# Docker requires you to specify the 'service' object when removing a service rather than a single container from
# a host.
docker service rm myweb

# Remove a service called 'my_api' from the running swarm.
docker service rm my_api

# When executed on one of the master nodes, will display the logs for the indicated service running on the swarm.
docker service logs [SERVICE_NAME]
```
