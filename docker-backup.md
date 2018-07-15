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

REF: https://docs.docker.com/v17.09/datacenter/ucp/2.2/guides/admin/backups-and-disaster-recovery/

1. UCP maintains data about:

    1. Configurations:  The UCP cluster configurations, as shown by `docker config ls`, including Docker EE license and
       swarm and client CAs
    1. Access control:  Permissions for teams to swarm resources, including collections, grants, and roles
    1. Certificates and keys:  The certificates, public keys, and private keys that are used for authentication and
       mutual TLS (mTLS) communication
    1. Metrics data:  Monitoring data gathered by UCP
    1. Organizations:  Your users, teams, and orgs
    1. Volumes:  All UCP named volumes, which include all UCP component certs and data

1. UCP restore recovers the following assets from the backup file:

    1. Users, teams, and permissions.
    1. All UCP configuration options available under Admin Settings, like the Docker EE subscription license,
       scheduling options, content trust, and authentication backends.

1. UCP restore does not include swarm assets such as cluster membership, services, networks, secrets, etc.

1. There are two ways to restore UCP:

    1. On a manager node of an existing swarm which does not have UCP installed. In this case, UCP restore will use
       the existing swarm.
    1. On a docker engine that isn’t participating in a swarm. In this case, a new swarm is created and UCP is
       restored on top.

### Backup a UCP manager node and verify its contents (`docker/ucp:2.2.4 backup`)

```bash
# Create a backup, encrypt it, and store it on /tmp/backup.tar
docker container run --log-driver none --rm -i --name ucp -v /var/run/docker.sock:/var/run/docker.sock \
  docker/ucp:2.2.4 backup --interactive > /tmp/backup.tar

# Ensure the backup is a valid tar and list its contents.
# In a valid backup file, over 100 files should appear in the list and the `./ucp-node-certs/key.pem`
# file should be present.
tar --list -f /tmp/backup.tar

# Create a backup, encrypt it, and store it on /tmp/backup.tar, with a passhrase
docker container run --log-driver none --rm -i --name ucp -v /var/run/docker.sock:/var/run/docker.sock \
  docker/ucp:2.2.4 backup --interactive --passphrase "secret" > /tmp/backup.tar

# Decrypt the backup and list its contents
$ gpg --decrypt /tmp/backup.tar | tar --list
```

### Restore UCP (`docker/ucp:2.2.4 restore`)

1. To restore an existing UCP installation from a backup, you need to uninstall UCP from the swarm by using the
   `uninstall-ucp` command.

1. When restoring, make sure you use the same version of the docker/ucp image that you’ve used to create the backup.

```bash
docker container run --rm -i --name ucp -v /var/run/docker.sock:/var/run/docker.sock  \
  docker/ucp:2.2.4 restore < /tmp/backup.tar

# If the backup file is encrypted with a passphrase, you will need to provide the passphrase to the restore
# operation:
docker container run --rm -i --name ucp -v /var/run/docker.sock:/var/run/docker.sock  \
  docker/ucp:2.2.4 restore --passphrase "secret" < /tmp/backup.tar
  
# The restore command may also be invoked in interactive mode, in which case the backup file should be mounted
# to the container rather than streamed through stdin:
docker container run --rm -i --name ucp -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp/backup.tar:/config/backup.tar \
  docker/ucp:2.2.4 restore -i
```


## DTR backup

REF: https://docs.docker.com/ee/dtr/admin/disaster-recovery/create-a-backup/

1. DTR maintains data about:

    1. Configurations:  The DTR cluster configurations
    1. Repository metadata:  The metadata about the repositories and images deployed
    1. Access control to repos and images:  Permissions for teams and repositories
    1. Notary data:  Notary tags and signatures
    1. Scan results:  Security scanning results for images
    1. Certificates and keys:  The certificates, public keys, and private keys that are used for mutual TLS (mTLS)
       communication
    1. Images content:  The images you push to DTR. This can be stored on the file system of the node running DTR, or
       other storage system, depending on the r

### Backup a DTR node (`docker/dtr:2.5.3 backup`)

```bash
# To perform a backup of a DTR node, run
docker run -i --rm docker/dtr backup [command options] > backup.tar
```

1. This command creates a tar file with the contents of the volumes used by DTR, and prints it. You can then use the
   ‘restore’ command to restore the data from an existing backup.

1. This command only creates backups of configurations, and image metadata.

    1. It does not backup the Docker images stored in your registry. You should implement a separate backup policy
       for the Docker images stored in your registry, taking in consideration whether your DTR installation is
       configured to store images on the filesystem or using a cloud provider.
    1. It does not backup users and organizations. Users and organizations can be backed up when performing a UCP
       backup.
    1. It does not backup the Vulnerability database, which can be re-downloaded after a restore.

1. This backup contains sensitive information and should be stored securely.

1. Using the `--offline-backup` flag will temporarily shut down the **rethinkdb** container. You should take the
   replica out of your load balancer to avoid downtime.

```bash
# Backup image content
sudo tar -cf {{ image_backup_file }} \
  $(dirname $(docker volume inspect --format '{{.Mountpoint}}' dtr-registry-<replica-id>))

# Backup DTR metadata
# Where:
# - <ucp-url> is the url you use to access UCP.
# - <ucp-username> is the username of a UCP administrator.
# - <replica-id> is the id of the DTR replica to backup.
read -sp 'ucp password: ' UCP_PASSWORD; \
docker run --log-driver none -i --rm \
  --env UCP_PASSWORD=$UCP_PASSWORD \
  docker/dtr:2.5.3 backup \
  --ucp-url <ucp-url> \
  --ucp-insecure-tls \
  --ucp-username <ucp-username> \
  --existing-replica-id <replica-id> > dtr-metadata-backup.tar

# Encrypt the backup, as it contains sensitive information like private keys
# This prompts you for a password to encrypt the backup, copies the backup file and encrypts it.
gpg --symmetric dtr-metadata-backup.tar

# Validate the backup by printing the contents of the tar file created
tar -tf dtr-metadata-backup.tar
> dtr-backup-v2.5.3/
> dtr-backup-v2.5.3/rethink/
> dtr-backup-v2.5.3/rethink/layers/
...
> dtr-backup-v2.5.3/rethink/properties/
> dtr-backup-v2.5.3/rethink/properties/0

# If you’ve encrypted the metadata backup, you can use
gpg -d dtr-metadata-backup.tar | tar -t
```

You can also create a backup of a UCP cluster and restore it into a new cluster. Then restore DTR on that new cluster
to confirm that everything is working as expected.


### Restore a DTR node (`docker/dtr:2.5.3 restore`)

1. To restore DTR, you need to:
    1. Stop any DTR containers that might be running
    1. Restore the images from a backup
    1. Restore DTR metadata from a backup
    1. Re-fetch the vulnerability database

1. You need to restore DTR on the same UCP cluster where you’ve created the backup.

1. When restoring, you need to use the same version of the docker/dtr image that you’ve used when creating the update.

```bash
# Start by removing any DTR container that is still running
docker run -it --rm docker/dtr:2.5.3 destroy --ucp-insecure-tls

# Restore images
# If you had DTR configured to store images on the local filesystem, you can extract your backup:
sudo tar -xf dtr-image-backup.tar -C /var/lib/docker/volumes

# Restore DTR metadata
read -sp 'ucp password: ' UCP_PASSWORD; \
docker run -i --rm \
  --env UCP_PASSWORD=$UCP_PASSWORD \
  docker/dtr:2.5.3 restore \
  --ucp-url <ucp-url> \
  --ucp-insecure-tls \
  --ucp-username <ucp-username> \
  --ucp-node <hostname> \
  --replica-id <replica-id> \
  --dtr-external-url <dtr-external-url> < dtr-metadata-backup.tar
```
