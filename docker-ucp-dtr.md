# Universal Control Plane (UCP) and Docker Trusted Registry (DTR)


## Backups and disaster recovery

https://docs.docker.com/ee/ucp/admin/backups-and-disaster-recovery/#data-managed-by-ucp

1. The correct order to upgrade a Docker cluster
   1. Upgrade engine and kernel,
   1. UCP (Universal Control Plane), then
   1. DTR (Docker Trusted Registry)

1. Back up your Docker EE components in the following order:
   1. Back up your swarm
   1. Back up UCP
   1. Back up DTR

1. To create a UCP backup, run the `docker/ucp:3.0.2 backup` command on a single UCP manager.
   This command creates a tar archive with the contents of all the volumes used by UCP to persist data and streams it
   to stdout. The backup doesn’t include the swarm-mode state, like service definitions and overlay network definitions.

## Universal Control Plane (UCP)

1. UCP is used to create users and teams.

1. What is the endpoint that we can use to check the health of a single UCP manager node?

   `https:///_ping`

1. You can monitor the status of UCP by using the web CI or the CLI.

## Docker Trusted Registry (DTR)

1. Docker Trusted Registry is the image storage solution that is part of Docker Enterprise Edition.

1. Requirements to install Docker Trusted Registry (DTR):
    1. DTR can be installed on-premises or a cloud provider.
    1. All nodes must be a worker node managed by Universal Control Plane.
    1. All nodes must have a fixed hostname.

1. Endpoints exposed by Docker Trusted Registry that can be used to assess the health of a Docker Trusted Registry replica
    ```
    /health
    /nginx_status
    /api/v0/meta/cluster_status
    ```

## docker hub

The most common public repository for published Docker images.

