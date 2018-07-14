# Docker Security

https://docs.docker.com/engine/security/

1. You can configure Docker’s trust features so that your users can push and pull trusted images.

1. You can protect the Docker daemon socket and ensure only trusted Docker client connections.

1. You can use certificate-based client-server authentication to verify a Docker daemon has the rights to access images
   on a registry. 

1. You can configure secure computing mode (Seccomp) policies to secure system calls in a container. 

1. An AppArmor profile for Docker is installed with the official .deb packages. 


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


#### MTLS (Mutual Transport Layer Security)

MTLS is used to secure communications between the manager and nodes in a Docker Swarm cluster.


#### Role Based Access Control (RBAC)

Ref: https://docs.docker.com/ee/ucp/authorization/

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

1. **Roles** define what operations can be done by whom. A role is a set of permitted operations against a type of resource,
   like a container or volume, that’s assigned to a user or team with a grant.

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


#### DOCKER_CONTENT_TRUST=1

The variable `DOCKER_CONTENT_TRUST` set to '1' will inform the Docker daemon to only pull trusted content within the
shell it is set in.

See [docker-dtr](docker-dtr.md).

```bash
# To sign an image, you can run:
export DOCKER_CONTENT_TRUST=1
docker push <dtr-domain>/<repository>/<image>:<tag>
```
