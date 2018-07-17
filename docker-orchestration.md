# Docker Orchestration

### Docker service

The Docker service can be managed via standard systemd service management utilities.

```bash
# Enable and start Docker CE (Ubuntu 16 or above)
systemctl enable docker && systemctl start docker

# Query docker state (e.g. stopped or running) (Ubuntu 16)
systemctl status docker
# OR (Ubuntu 14)
service docker status
```


### Docker Swarm

1. Docker Swarm is a cluster management and deployment system.

1. Docker Swarm allows you to deploy clusters of Docker containers across multiple nodes and manage their behavior.

1. Two types of Docker Swarm Services
    1. **Replicated**: Number of identical tasks can be specified for a replicated service.
    1. **Global**: There is no pre-specified number of tasks for global service.

1. **Raft** (**Docker Consensus Algorithm**)
   1. In Docker Swarm mode, **manager nodes** implement the Raft Consensus Algorithm to manage the **global cluster**
      state. The consensus algorithm is to make sure that all the manager nodes that are in charge of managing and
      scheduling tasks in the cluster, are storing the same consistent state.
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

# For a cluster to have dedicated manager nodes that are not served as worker nodes.
docker swarm init --availability=drain

# Docker will display the necessary information for a manager or node to join a cluster during initialization. 
# This command will allow you to retrieve that information for subsequent joins.
docker swarm join-token manager

# Docker provides the necessary command for any node to join upon creation. 
# The command will allow you to redisplay the command needed for a node to join a cluster.
docker swarm join-token worker

# Docker allows a node with the appropriate token to join the swarm indicated by the IP and port.
# A node to join the indicated cluster of the IP (of 10.0.1.100), with a token 'ighhsjkd6637'
docker swarm join --token ighhsjkd6637 10.0.1.100:2377

# Execute this command from the node you are removing, you can gracefully leave the cluster without having to use
# the NODE ID.
docker swarm leave
> Node left the defauly swarm.
# The node will still appear in the node list, and marked as `down`. Use `node rm` to remove inactive node.

# Enable autolock on an existing swarm cluster
docker swarm update --autolock=true

# This flag specifies the availability of the node at the time the node joins a master.
# Possible availability values are active, pause, or drain.
docker swarm update --availability active
```

#### `docker node`

```bash
# Lists all the nodes that the Docker Swarm manager knows about; OPTIONS: --filter"-f, --format, --quiet|-q
docker node ls [OPTIONS]
docker node ls
> ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
> 7ln70fl22uw2dvjn2ft53m3q5    worker2   Ready   Active
> dkp8vy1dq1kxleu9g4u78tlag    worker1   Ready   Active
> dvfxp4zseq4s0rih1selh0d20 *  manager1  Ready   Active        Leader

# Add or update multiple node labels of the node `worker1`
docker node update --label-add foo --label-add bar worker1

# Drain the indicated node so that future services will not run on it unless the command is undone (when run from
# the manager node).
# Docker updates the object (node) to DOWN when the availability is indicated to be 'drain' on the indicated NODE
# ID.
# Possible availability values are active, pause, or drain.
docker node update --availability drain [NODE_ID]

# Undo the 'drain' task applied to a node so that it can be used again for services.
# Once a node has been drained, it is marked DOWN and must be updated to ACTIVE status so that it's availability
# for services as advertised.
docker node update --availability active [NODE_ID]

# Remove a node marked as 'DOWN' from the cluster
docker node rm [NODE_ID]

# When run on the manager node, this command will remove the indicated node from the swarm it is a member of.
docker node rm [NODE_ID]

# `docker inspect` returns low-level information on Docker objects (e.g. container, node, etc.)
# For nodes: 
# The '--pretty' option will format the associated output in a more easily readable format.
# JSON, is thde default output from an inspect command.
docker node inspect [OPTIONS] self|NODE [NODE...]

# Print the inspect output in a human-readable format instead of the default JSON output
docker node inspect --pretty self|NODE

docker node inspect --format '{{ .ManagerStatus.Leader }}' self
```

#### `docker service`

```bash
# When run on the master, list all the service processes running in a swarm
docker service ps

docker service create [OPTIONS] IMAGE [COMMAND] [ARG...]

# Create a service called 'my_api_service' as if it is being run on the manager node based on a locally installed
# image called MYAPI_IMAGE.
docker service create --name my_api_service MYAPI_IMAGE

# Create a service called 'my_api_service' that contains three replicas from a service image called MYAPI_IMAGE
docker service create --name my_api_service --replicas 3 MYAPI_IMAGE

# Scale the number of replicas in your swarm to 5 once the cluster is already running
# The 'scale' option allows you to indicate the service to scale along with the number of replicas to scale to.
docker service scale [SERVICE_NAME]=5

# The following commands are equivalent:
# https://docs.docker.com/engine/reference/commandline/service_scale/#scale-a-single-service
docker service scale frontend=50
docker service update --replicas=50 frontend

# Scale your service (my_api_service) from whatever its current replica count is to 10 replicas in the cluster
docker service scale my_api_service=10

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

# Use the --secret-add or --secret-rm options add or remove a service’s secrets.
# Add a secret named ssh-2 and removes ssh-1:
docker service update \
  --secret-add source=ssh-2,target=ssh-2 \
  --secret-rm ssh-1 \
  myservice

# Remove a service (my_api_service) from the running swarm.
docker service rm my_api_service

# Stop a service (my_api_service) on your cluster
# Docker requires you to specify the 'service' object when removing a service rather than a single container from
# a host.
docker service rm my_api_service

# When executed on one of the master nodes, will display the logs for the indicated service running on the swarm.
docker service logs [SERVICE_NAME]

# `docker inspect` returns low-level information on Docker objects (e.g. container, node, etc.)
# For nodes: 
# The '--pretty' option will format the associated output in a more easily readable format.
# JSON, is thde default output from an inspect command.
docker service inspect [OPTIONS] SERVICE [SERVICE...]

# Print the inspect output in a human-readable format instead of the default JSON output
docker service inspect --pretty [SERVICE_NAME]

# Find the number of tasks running as part of the service "redis".
docker service inspect --format="{{.Spec.Mode.Replicated.Replicas}}" redis 
```


## Docker Configs

REF: https://docs.docker.com/engine/swarm/configs/


## Docker Secrets

REF: https://docs.docker.com/engine/swarm/secrets/

1. Docker secrets are only available to swarm **services**, not to standalone containers. 
1. To use this feature, consider adapting your container to run as a service. Stateful containers can typically run
   with a scale of 1 without changing the container code.

### How Docker manages secrets

1. When you add a secret to the swarm, Docker sends the secret to the swarm manager over a mutual TLS connection. 
   
1. The secret is stored in the Raft log, which is encrypted. The entire Raft log is replicated across the other
   managers, ensuring the same high availability guarantees for secrets as for the rest of the swarm management data.

1. When you grant a newly-created or running service access to a secret, the decrypted secret is mounted into the
   container in an in-memory filesystem. The location of the mount point within the container defaults to
   `/run/secrets/<secret_name>` in Linux containers, or `C:\ProgramData\Docker\secrets` in Windows containers.
   You can specify a custom location in Docker 17.06 and higher.

1. You can update a service to grant it access to additional secrets or revoke its access to a given secret at any time.

1. A node only has access to (encrypted) secrets if the node is a swarm manager or if it is running service tasks which
   have been granted access to the secret. When a container task stops running, the decrypted secrets shared to it are
   unmounted from the in-memory filesystem for that container and flushed from the node’s memory.

1. If a node loses connectivity to the swarm while it is running a task container with access to a secret, the task
   container still has access to its secrets, but cannot receive updates until the node reconnects to the swarm.

1. You can add or inspect an individual secret at any time, or list all secrets. You cannot remove a secret that a
   running service is using.

1. To update or roll back secrets more easily, consider adding a version number or date to the secret name. This is
   made easier by the ability to control the mount point of the secret within a given container.

### Rotate a secret for a way to remove a secret without disrupting running services.

REF: https://docs.docker.com/engine/swarm/secrets/#example-rotate-a-secret

