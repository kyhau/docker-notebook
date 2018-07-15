# Docker Trusted Registry (DTR)

1. Docker Trusted Registry is the image storage solution that is part of Docker Enterprise Edition.

1. Requirements to install Docker Trusted Registry (DTR):
    1. DTR can be installed on-premises or a cloud provider (or a virtual private cloud).
    1. All nodes must be a worker node managed by Universal Control Plane (UCP).
    1. All nodes must have a fixed hostname.

1. DTR uses the same authentication mechanism as Docker Universal Control Plane (UCP). Users can be managed manually
   or synched from LDAP or Active Directory. 
   
   DTR uses **Role Based Access Control (RBAC)** to allow you to implement fine-grained access control policies for
   who has access to your Docker images. See [docker-security.md](docker-security.md).

1. DTR requires that a majority (N/2 + 1) of its replicas are healthy at all times for it to work.
   So if a majority of replicas is unhealthy or lost, the only way to restore DTR to a working state, is by recovering
   from a backup. This is why it’s important to ensure replicas are healthy and perform frequent backups.
   See [docker-backup.md](docker-backup.md).

1. Endpoints exposed by DTRDocker Trusted Registry that can be used to assess the health of a Docker Trusted Registry
   replica:
    ```
    /health
    /nginx_status
    /api/v0/meta/cluster_status
    ```

## Sign image and push to DTR

REF: https://docs.docker.com/ee/dtr/user/manage-images/sign-images/#sign-images-that-ucp-can-trust

See Also [Content Trust] in [docker-security.md](docker-security.md).

```bash
# Pull NGINX from Docker Store
docker pull nginx:latest

# Re-tag NGINX
docker tag nginx:latest dtr.example.org/dev/nginx:1

# Log into DTR
docker login dtr.example.org

# Sign and push the image to DTR
export DOCKER_CONTENT_TRUST=1
docker push dtr.example.org/dev/nginx:1
```

1. By default, when you push an image to DTR, the Docker CLI client does not sign the image.

   ![Alt text](https://docs.docker.com/ee/dtr/images/sign-an-image-1.svg?sanitize=true)

   ([Image source: docs.docker.com](https://docs.docker.com))

1. You can configure the Docker CLI client to sign the images you push to DTR. This allows whoever pulls your image to
   validate if they are getting the image you created, or a forged one.

   ```bash
   # To sign an image, you can run:
   export DOCKER_CONTENT_TRUST=1
   docker push <dtr-domain>/<repository>/<image>:<tag>
   ```

   This pushes the image to DTR and creates trust metadata. It also creates public and private key pairs to sign the
   trust metadata, and pushes that metadata to the Notary Server internal to DTR.

   ![Alt text](https://docs.docker.com/ee/dtr/images/sign-an-image-2.svg?sanitize=true)

   ([Image source: docs.docker.com](https://docs.docker.com))


