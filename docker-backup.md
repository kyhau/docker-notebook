# Backups and disaster recovery

https://docs.docker.com/ee/ucp/admin/backups-and-disaster-recovery/#data-managed-by-ucp

1. The correct order to upgrade a Docker cluster
   1. Upgrade engine and kernel,
   1. UCP (Universal Control Plane), then
   1. DTR (Docker Trusted Registry)

1. Back up your Docker EE components in the following order:
   1. Back up your swarm
   1. Back up UCP
   1. Back up DTR

```bash
# To create a UCP backup, run this command on a single UCP manager
# This command creates a tar archive with the contents of all the volumes used by UCP to persist data and
# streams it to stdout. The backup doesn’t include the swarm-mode state, like service definitions and overlay
# network definitions.
docker/ucp:3.0.2 backup
```
