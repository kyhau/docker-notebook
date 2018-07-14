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


## UCP backup

```bash
# To create a UCP backup, run this command on a single UCP manager
# This command creates a tar archive with the contents of all the volumes used by UCP to persist data and
# streams it to stdout. The backup doesn’t include the swarm-mode state, like service definitions and overlay
# network definitions.
docker/ucp:3.0.2 backup
```


## DTR backup

https://docs.docker.com/reference/dtr/2.5/cli/backup/

```bash
docker run -i --rm docker/dtr backup [command options] > backup.tar
```

1. This command creates a tar file with the contents of the volumes used by DTR, and prints it. You can then use the
   ‘restore’ command to restore the data from an existing backup.

1. This command only creates backups of configurations, and image metadata. It doesn’t backup users and organizations.
   Users and organizations can be backed up when performing a UCP backup.

   It also does not backup the Docker images stored in your registry. You should implement a separate backup policy
   for the Docker images stored in your registry, taking in consideration whether your DTR installation is configured
   to store images on the filesystem or using a cloud provider.

1. This backup contains sensitive information and should be stored securely.

1. Using the `--offline-backup` flag will temporarily shut down the **rethinkdb** container. You should take the
   replica out of your load balancer to avoid downtime.

