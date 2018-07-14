# Docker Trusted Registry (DTR)

1. Docker Trusted Registry is the image storage solution that is part of Docker Enterprise Edition.

1. DTR can be installed on-premise or on a virtual private cloud.

1. DTR uses the same authentication mechanism as Docker Universal Control Plane (UCP). Users can be managed manually
   or synched from LDAP or Active Directory. 
   
   DTR uses **Role Based Access Control (RBAC)** to allow you to implement fine-grained access control policies for
   who has access to your Docker images. See [docker-security.md](docker-security.md).

1. Requirements to install Docker Trusted Registry (DTR):

    1. DTR can be installed on-premises or a cloud provider.
    1. All nodes must be a worker node managed by Universal Control Plane.
    1. All nodes must have a fixed hostname.

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

1. Endpoints exposed by DTRDocker Trusted Registry that can be used to assess the health of a Docker Trusted Registry
   replica:
    ```
    /health
    /nginx_status
    /api/v0/meta/cluster_status
    ```

# Docker image signing

Ref: https://docs.docker.com/ee/dtr/user/manage-images/sign-images/#sign-images-that-ucp-can-trust

1. Docker supports image signing since Docker 1.8 (implemented as a separate piece of plumbing called Notary).

1. Target version to be updated to > Docker 1.8 (Docker registry 2.1)

1. By default, when you push an image to DTR, the Docker CLI client doesn’t sign the image.

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

1. Example

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


### Sign images that UCP can trust

1. With the command above you’ll be able to sign your DTR images, but UCP won’t trust them because it can’t tie the
   private key you’re using to sign the images to your UCP account.

    To sign images in a way that UCP trusts them, you need to:

    1. Configure your Notary client
    1. Initialize trust metadata for the repository
    1. Delegate signing to the keys in your UCP client bundle


1. When content trust is enabled,

    1. The docker CLI commands that operate on tagged images must either have content signatures or explicit content
       hashes. The commands that operate with content trust are: push, build, create, pull, run

    1. The Docker client only allows docker pull to retrieve signed images.  However, an operation with an explicit
       content hash always succeeds as long as the hash exists:
       E.g. $ docker pull someimage@sha256:d149ab53f8718e987c3a3024bb8aa0e2caadf6c0328f1d9d850b2a2a67f2819a

    1. Trust for an image tag is managed through the use of signing keys. A key set is created when an operation using
       content trust is first invoked. A key set consists of the following classes of keys.

        1. An offline key is used to create tagging keys. Offline keys belong to a person or an organisation. Resides
           client-side. You should store these in a safe place and back them up.

        1. A tagging key is associated with an image repository. Creators with this key can push or pull any tag in this
           repository. This resides on client-side.

        1. A timestamp key is associated with an image repository. This is created by Docker and resides on the server.

    See more details in https://docs.docker.com/engine/security/trust/content_trust/


## Scan images for vulnerabilities

https://docs.docker.com/ee/dtr/user/manage-images/scan-images-for-vulnerabilities/

1. Docker Security Scanning is available as an add-on to Docker Trusted Registry, and an administrator configures it
   for your DTR instance.

1. Only users with write access to a repository can manually start a scan. Users with read-only access can view the
   scan results, but cannot start a new scan.


