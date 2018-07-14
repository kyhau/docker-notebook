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

Ref: https://docs.docker.com/v17.09/datacenter/ucp/2.2/guides/admin/backups-and-disaster-recovery/

1. UCP maintains data about:

    1. Configurations:  The UCP cluster configurations, as shown by `docker config ls`, including Docker EE license and
      swarm and client CAs
    1. Access control:  Permissions for teams to swarm resources, including collections, grants, and roles
    1. Certificates and keys:  The certificates, public keys, and private keys that are used for authentication and
       mutual TLS communication
    1. Metrics data:  Monitoring data gathered by UCP
    1. Organizations:  Your users, teams, and orgs
    1. Volumes:  All UCP named volumes, which include all UCP component certs and data


### Backup policy

TODO

```bash
# To create a UCP backup, run this command on a single UCP manager
# This command creates a tar archive with the contents of all the volumes used by UCP to persist data and
# streams it to stdout. The backup doesn’t include the swarm-mode state, like service definitions and overlay
# network definitions.
docker/ucp:3.0.2 backup
```

### Backup a UCP manager node and verify its contents:

TODO


## DTR backup

Ref: https://docs.docker.com/ee/dtr/admin/disaster-recovery/create-a-backup/

1. DTR maintains data about:

    1. Configurations:  The DTR cluster configurations
    1. Repository metadata:  The metadata about the repositories and images deployed
    1. Access control to repos and images:  Permissions for teams and repositories
    1. Notary data:  Notary tags and signatures
    1. Scan results:  Security scanning results for images
    1. Certificates and keys:  The certificates, public keys, and private keys that are used for mutual TLS
       communication
    1. Images content:  The images you push to DTR. This can be stored on the file system of the node running DTR, or
       other storage system, depending on the configuration

### Backup a DTR node

```bash
# To perform a backup of a DTR node, run
docker run -i --rm docker/dtr backup [command options] > backup.tar
```

1. This command creates a tar file with the contents of the volumes used by DTR, and prints it. You can then use the
   ‘restore’ command to restore the data from an existing backup.

1. This command only creates backups of configurations, and image metadata.

    1. It  does not backup the Docker images stored in your registry. You should implement a separate backup policy
       for the Docker images stored in your registry, taking in consideration whether your DTR installation is
       configured to store images on the filesystem or using a cloud provider.
    
    1. It does not backup users and organizations. Users and organizations can be backed up when performing a UCP
       backup.

    1. It does not backup the Vulnerability database, which can be re-downloaded after a restore.

1. This backup contains sensitive information and should be stored securely.

1. Using the `--offline-backup` flag will temporarily shut down the **rethinkdb** container. You should take the
   replica out of your load balancer to avoid downtime.


### Backup image content

```bash
sudo tar -cf {{ image_backup_file }} \
$(dirname $(docker volume inspect --format '{{.Mountpoint}}' dtr-registry-<replica-id>))
```


### Backup DTR metadata

```bash
read -sp 'ucp password: ' UCP_PASSWORD; \
docker run --log-driver none -i --rm \
  --env UCP_PASSWORD=$UCP_PASSWORD \
  docker/dtr:2.5.3 backup \
  --ucp-url <ucp-url> \
  --ucp-insecure-tls \
  --ucp-username <ucp-username> \
  --existing-replica-id <replica-id> > dtr-metadata-backup.tar
```
Where:
- <ucp-url> is the url you use to access UCP.
- <ucp-username> is the username of a UCP administrator.
- <replica-id> is the id of the DTR replica to backup.


#### Encrypt the backup

Also, the backup contains sensitive information like private keys, so you can encrypt the backup by running:

```bash
gpg --symmetric dtr-metadata-backup.tar
```

This prompts you for a password to encrypt the backup, copies the backup file and encrypts it.


### Test your backups

To validate that the backup was correctly performed, you can print the contents of the tar file created. The backup
of the images should look like:

```bash
tar -tf dtr-metadata-backup.tar

dtr-backup-v2.5.3/
dtr-backup-v2.5.3/rethink/
dtr-backup-v2.5.3/rethink/layers/
```

And the backup of the DTR metadata should look like:

```bash
tar -tf dtr-metadata-backup.tar

# The archive should look like this
dtr-backup-v2.5.3/
dtr-backup-v2.5.3/rethink/
dtr-backup-v2.5.3/rethink/properties/
dtr-backup-v2.5.3/rethink/properties/0
```

If you’ve encrypted the metadata backup, you can use:

```bash
gpg -d dtr-metadata-backup.tar | tar -t

```

You can also create a backup of a UCP cluster and restore it into a new cluster. Then restore DTR on that new cluster
to confirm that everything is working as expected.
