# Docker Security

REF: https://docs.docker.com/engine/security/

1. You can configure Docker’s trust features so that your users can push and pull trusted images.
1. You can protect the Docker daemon socket and ensure only trusted Docker client connections.
1. You can use certificate-based client-server authentication to verify a Docker daemon has the rights to access images
   on a registry. 
1. You can configure secure computing mode (**Seccomp**) policies to secure system calls in a container.
1. An **AppArmor profile** for Docker is installed with the official .deb packages. 


## docker run --privileged

Providing `--privileged` to a container at startup, will allow it to perform operations that a container may otherwise
be restricted from performing (e.g. binding a device path to an internal container path).

`docker run --privileged -it --rm ubuntu:latest bash`

So basically any container host that you allow anyone to launch a `--privileged` container on is the same as giving
them root access to every container on that host.

Unfortunately the docker project has chosen the trusted computing model, and outside of auth plugins there is no way
to protect against this, so always error on the side of adding needed features vs. using `--privileged`.

REF: [stackoverflow:privileged-containers-and-capabilities](
https://stackoverflow.com/questions/36425230/privileged-containers-and-capabilities).


## mTLS (Mutual Transport Layer Security)

REF: https://docs.docker.com/engine/swarm/how-swarm-mode-works/pki/

The swarm mode public key infrastructure (PKI) system built into Docker makes it simple to securely deploy a container
orchestration system.

The nodes in a swarm use **mutual Transport Layer Security (TLS)** to authenticate, authorize,
and encrypt the communications with other nodes in the swarm.

mTLS is used to secure communications between the manager and nodes in a Docker Swarm cluster.


## Role Based Access Control (RBAC)

REF: https://docs.docker.com/ee/ucp/authorization/

1. In Docker Universal Control Plane (UCP) Security, RBAC is an acronym that determines what a user, team, or
   organization has access to on the cluster based on the role granted to them.

1. To authorize access to cluster resources across your organization, UCP administrators might take the following
   high-level steps:
    1. Add and configure **subjects** (users, teams, organisations, and service accounts).
    1. Define custom **roles** (or use defaults) by adding permitted operations per type of resource.
    1. Group cluster **resources** into resource sets of Swarm collections or Kubernetes namespaces.
    1. Create **grants** by combining subject + role + resource set.

1. A **subject** represents a user, team, organization, or service account. A subject can be granted a role that defines
   permitted operations against one or more resource sets.
    1. User: A person authenticated by the authentication backend. Users can belong to one or more teams and one or
       more organizations.
    1. Team: A group of users that share permissions defined at the team level. A team can be in one organization only.
    1. Organization: A group of teams that share a specific set of permissions, defined by the roles of the organization.
    1. Service account: A Kubernetes object that enables a workload to access cluster resources that are assigned to a
       namespace.

1. **Roles** define what operations can be done by whom. A role is a set of permitted operations against a type of
   resource, like a container or volume, that’s assigned to a user or team with a grant.

1. **Resource sets** include **collections** and **namespaces**.
    1. To control user access, cluster resources are grouped into **Docker Swarm collections** or **Kubernetes
       namespaces**.
    1. Swarm collections: 
        1. A collection has a directory-like structure that holds Swarm resources.
        1. You can create collections in UCP by defining a directory path and moving resources into it. 
        1. Also, you can create the path in UCP and use labels in your YAML file to assign application resources to
           the path. 
        1. Resource types that users can access in a Swarm collection include containers, networks, nodes, services,
           secrets, and volumes.
    1. Kubernetes namespaces: 
        1. A namespace is a logical area for a Kubernetes cluster.
           Kubernetes comes with a default namespace for your cluster objects, plus two more namespaces for system and
           public resources.
        1. You can create custom namespaces, but unlike Swarm collections, namespaces can’t be nested. Resource types
           that users can access in a Kubernetes namespace include pods, deployments, network policies, nodes, services,
           secrets, and many more.

1. A **grant** is made up of **subject**, **role**, and **resource set**.
    1. Grants define which users can access what resources in what way.
    1. Grants are effectively **Access Control Lists (ACLs)**, and when grouped together, they provide comprehensive
       access policies for an entire organization.

    ![docker-grant](https://docs.docker.com/ee/ucp/images/ucp-grant-model.svg?sanitize=true)
    
    ([Image source: docs.docker.com](https://docs.docker.com/ee/ucp/authorization/grant-permissions/#swarm-grants))

1. Only an administrator can manage grants, subjects, roles, and access to resources.


## UCP Client Bundle

A UCP Client Bundle provides the following items to a client that intends to use or manage the cluster:

1. Account security key
1. Environment variables to set the connection destination.
1. UCP certificate files to trust.


## Client certificates for administrators

UCP issues different types of certificates depending on the user:

1. User certificate bundles: only allow running docker commands through a UCP manager node.
1. Admin user certificate bundles: allow running docker commands on the Docker Engine of any node.


## Docker image signing

Docker supports image signing since Docker 1.8 (implemented as a separate piece of plumbing called **Notary**).

REF: https://docs.docker.com/engine/security/trust/content_trust/


### Enable and disable content trust per-shell or per-invocation

```bash
# To enable content trust in a bash shell enter the following command:
export DOCKER_CONTENT_TRUST=1

# In an environment where DOCKER_CONTENT_TRUST is set, you can use the --disable-content-trust flag to run
# individual operations on tagged images without content trust on an as-needed basis.
cat Dockerfile
> FROM docker/trusttest:latest
> RUN echo

# To build a container successfully using this Dockerfile:
docker build --disable-content-trust -t <username>/nottrusttest:latest .

# The same is true for all the other commands, such as pull and push:
docker pull --disable-content-trust docker/trusttest:latest
docker push --disable-content-trust <username>/nottrusttest:latest

# To invoke a command with content trust enabled regardless of whether or how the DOCKER_CONTENT_TRUST is set:
docker build --disable-content-trust=false -t <username>/trusttest:testing .
```


### Sign images that UCP can trust

See also **Sign image and push to DTR** in [docker-dtr](docker-dtr.md).

1. With the command above you’ll be able to sign your DTR images, but UCP will not trust them because it cannot tie the
   private key you’re using to sign the images to your UCP account.

   To sign images in a way that UCP trusts them, you need to:
    1. Configure your **Notary client**.
    1. Initialize **trust metadata** for the repository.
    1. Delegate signing to the **keys in your UCP client bundle**.

1. When content trust is enabled,

    1. The docker CLI commands that operate on tagged images must either have content signatures or explicit content
       hashes. The commands that operate with content trust are: push, build, create, pull, run
    1. The Docker client only allows docker pull to retrieve signed images.  However, an operation with an explicit
       content hash always succeeds as long as the hash exists:
       E.g. 
       
       `$ docker pull someimage@sha256:d149ab53f8718e987c3a3024bb8aa0e2caadf6c0328f1d9d850b2a2a67f2819a`
    1. Trust for an image tag is managed through the use of signing keys. A key set is created when an operation using
       content trust is first invoked. A key set consists of the following classes of keys.
        1. An offline key is used to create tagging keys. Offline keys belong to a person or an organisation. Resides
           client-side. You should store these in a safe place and back them up.
        1. A tagging key is associated with an image repository. Creators with this key can push or pull any tag in this
           repository. This resides on client-side.
        1. A timestamp key is associated with an image repository. This is created by Docker and resides on the server.

    See more details in https://docs.docker.com/engine/security/trust/content_trust/


## Scan images for vulnerabilities

REF: https://docs.docker.com/ee/dtr/user/manage-images/scan-images-for-vulnerabilities/

1. Docker Security Scanning is available as an add-on to Docker Trusted Registry, and an administrator configures it
   for your DTR instance.
1. Only users with write access to a repository can manually start a scan.
1. Users with read-only access can view the scan results, but cannot start a new scan.


