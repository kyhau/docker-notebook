# Docker Secrets

REF: https://docs.docker.com/engine/swarm/secrets/

REF: https://docs.docker.com/engine/reference/commandline/secret_create/

```bash
# Create a secret
echo <secret> | docker secret create my_secret -

# Create a secret with a file
docker secret create my_secret ./secret.json

# Create a secret with labels
docker secret create --label env=dev --label rev=20170324 my_secret ./secret.json
> eo7jnzguqgtpdah3cm5srfb97

docker secret ls
> ID                          NAME                CREATED             UPDATED
> eo7jnzguqgtpdah3cm5srfb97   my_secret           6 seconds ago       6 seconds ago

docker secret inspect my_secret
> [
    {
        "ID": "eo7jnzguqgtpdah3cm5srfb97",
        "Version": {
            "Index": 17
        },
        "CreatedAt": "2017-03-24T08:15:09.735271783Z",
        "UpdatedAt": "2017-03-24T08:15:09.735271783Z",
        "Spec": {
            "Name": "my_secret",
            "Labels": {
                "env": "dev",
                "rev": "20170324"
            }
        }
    }
]

# Remove a secret
docker secret rm my_secret
> sapth4csdo5b6wz2p5uimh5xg
```


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

### Example

REF: https://docs.docker.com/engine/swarm/secrets/#defining-and-using-secrets-in-compose-files

```bash
# Add a secret to Docker
printf "This is a secret" | docker secret create my_secret_data -

# Create a redis service and grant it access to the secret. By default, the container can access the secret at
# /run/secrets/<secret_name>, but you can customize the file name on the container using the target option.

docker service  create --name redis --secret my_secret_data redis:alpine

# Verify that the task is running without issues
docker service ps redis
> ID            NAME     IMAGE         NODE              DESIRED STATE  CURRENT STATE          ERROR  PORTS
> bkna6bpn8r1a  redis.1  redis:alpine  ip-172-31-46-109  Running        Running 8 seconds ago  

# If there were an error, and the task were failing and repeatedly restarting, you would see something like
# this:

> NAME                      IMAGE         NODE  DESIRED STATE  CURRENT STATE          ERROR                      PORTS
> redis.1.siftice35gla      redis:alpine  moby  Running        Running 4 seconds ago                             
>  \_ redis.1.whum5b7gu13e  redis:alpine  moby  Shutdown       Failed 20 seconds ago      "task: non-zero exit (1)"  
>  \_ redis.1.2s6yorvd9zow  redis:alpine  moby  Shutdown       Failed 56 seconds ago      "task: non-zero exit (1)"  
>  \_ redis.1.ulfzrcyaf6pg  redis:alpine  moby  Shutdown       Failed about a minute ago  "task: non-zero exit (1)"  
>  \_ redis.1.wrny5v4xyps6  redis:alpine  moby  Shutdown       Failed 2 minutes ago       "task: non-zero exit (1)"

# Get the ID of the redis service task container
docker ps --filter name=redis -q
> 5cb1c2348a59

docker container exec $(docker ps --filter name=redis -q) ls -l /run/secrets
> total 4
> -r--r--r--    1 root     root            17 Dec 13 22:48 my_secret_data

docker container exec $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data
> This is a secret

# Verify that the secret is not available if you commit the container.
docker commit $(docker ps --filter name=redis -q) committed_redis

docker run --rm -it committed_redis cat /run/secrets/my_secret_data
> cat: can't open '/run/secrets/my_secret_data': No such file or directory

# Try removing the secret. The removal fails because the redis service is running and has access to the secret.
docker secret rm my_secret_data
> Error response from daemon: rpc error: code = 3 desc = secret
> 'my_secret_data' is in use by the following service: redis

# Remove access to the secret from the running redis service by updating the service.
docker service update --secret-rm my_secret_data redis

docker container exec -it $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data
> cat: can't open '/run/secrets/my_secret_data': No such file or directory
> Stop and remove the service, and remove the secret from Docker.

docker service rm redis

docker secret rm my_secret_data
```


### Rotate a secret for a way to remove a secret without disrupting running services.

REF: https://docs.docker.com/engine/swarm/secrets/#example-rotate-a-secret


# Docker Configs

REF: https://docs.docker.com/engine/swarm/configs/

TODO



