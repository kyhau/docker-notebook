# Docker Security


#### docker run --privileged

Providing `--privileged` to a container at startup, will allow it to perform operations that a container may otherwise
be restricted from performing (e.g. binding a device path to an internal container path).

```bash
docker run --privileged -it --rm ubuntu:latest bash
```

> So basically any container host that you allow anyone to launch a --privileged container on is the same as giving
  them root access to every container on that host.
  <br>
  Unfortunately the docker project has chosen the trusted computing model, and outside of auth plugins there is no way
  to protect against this, so always error on the side of adding needed features vs. using --privileged.

See reference in [stackoverflow:privileged-containers-and-capabilities](https://stackoverflow.com/questions/36425230/privileged-containers-and-capabilities).

#### UCP Client Bundle

A UCP Client Bundle provides the following items to a client that intends to use or manage the cluster? (Choose 3)

1. Account security key
1. Environment variables to set the connection destination.
1. UCP certificate files to trust.


#### DOCKER_CONTENT_TRUST=1

The variable `DOCKER_CONTENT_TRUST` set to '1' will inform the Docker daemon to only pull trusted content within the
 shell it is set in.


#### MTLS (Mutual Transport Layer Security)

MTLS is used to secure communications between the manager and nodes in a Docker Swarm cluster.


#### RBAC (Role Based Access Control)

In Docker UCP Security, RBAC is an acronym that determines what a user, team, or organization has access to on the
 cluster based on the role granted to them.


#### Namespaces

The following 'namespaces' Docker use to maintain its isolation and security model of the container processes
 from underlying host services.

    1. Network
    1. PID

