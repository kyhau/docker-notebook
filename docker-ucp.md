# Universal Control Plane (UCP)

1. Universal Control Plane (UCP) is a containerized application that runs on Docker Enterprise Edition and extends
   its functionality to make it easier to deploy, configure, and monitor your applications at scale.

1. Once Universal Control Plane (UCP) instance is deployed, developers/devops no longer interact with Docker Engine
   directly, but interact with UCP instead. 

   ![Alt text](https://docs.docker.com/ee/ucp/images/ucp-architecture-1.svg?sanitize=true)

   ([Image source: docs.docker.com](https://docs.docker.com))

1. UCP also secures Docker with **Role Based Access Control (RBAC)** so that only authorized users can make changes
   and deploy applications to your Docker cluster.

   See [docker-security.md](docker-security.md).

1. Since UCP exposes the standard Docker API, you can use tools like the Docker CLI client and Docker Compose.

1. UCP leverages the clustering and orchestration functionality provided by Docker.

   ![Alt text](https://docs.docker.com/ee/ucp/images/ucp-architecture-2.svg?sanitize=true)

   ([Image source: docs.docker.com](https://docs.docker.com))

    1. A swarm is a collection of nodes that are in the same Docker cluster.
    1. Nodes in a Docker swarm operate in one of two modes: **Manager** or **Worker**. 
    1. If nodes are not already running in a swarm when installing UCP, nodes will be configured to run in swarm mode.

1. When you deploy UCP, it starts running a globally scheduled service called `ucp-agent`. 

   If the node is a:

    1. **Manager**: 
        1. The `ucp-agent` service automatically starts serving all UCP components, including the UCP web UI and data
           stores used by UCP. The `ucp-agent` accomplishes this by deploying several containers on the node. 
        1. By promoting a node to manager, UCP automatically becomes highly available and fault tolerant.

    1. **Worker**: on worker nodes,
        1. The `ucp-agent` service starts serving a proxy service that ensures only authorized users and other UCP
           services can run Docker commands in that node. 
        1. The `ucp-agent` deploys a subset of containers on worker nodes.

1. What is the endpoint that we can use to check the health of a single UCP manager node?

   `https:///_ping`   
   `https://<ucp-manager-url>/_ping`

1. There are two ways to interact with UCP: the web UI or the CLI.

1. Where is the option to integrate Docker Enterprise with LDAP? UCP


## Pause Containers

1. Every pod in Kubernetes has a **pause** container, which is an “empty” container that bootstraps the pod to
   establish all of the namespaces. 
   
1. Pause containers hold the cgroups, reservations, and namespaces of a pod before its individual containers are
   created.

1. The **pause** container’s image is always present, so the allocation of the pod’s resources is instantaneous.

1. **pause** containers are hidden but you can see them by running

```bash
docker ps -a | grep -I pause

8c9707885bf6        dockereng/ucp-pause:3.0.0-6d332d3        "/pause"                 47 hours ago        Up 47 hours                                                                                               k8s_POD_calico-kube-controllers-559f6948dc-5c84l_kube-system_d00e5130-1bf4-11e8-b426-0242ac110011_0
258da23abbf5        dockereng/ucp-pause:3.0.0-6d332d3        "/pause"                 47 hours ago        Up 47 hours                                                                                               k8s_POD_kube-dns-6d46d84946-tqpzr_kube-system_d63acec6-1bf4-11e8-b426-0242ac110011_0
2e27b5d31a06        dockereng/ucp-pause:3.0.0-6d332d3        "/pause"                 47 hours ago        Up 47 hours                                                                                               k8s_POD_compose-698cf787f9-dxs29_kube-system_d5866b3c-1bf4-11e8-b426-0242ac110011_0
5d96dff73458        dockereng/ucp-pause:3.0.0-6d332d3        "/pause"                 47 hours ago        Up 47 hours 
```

### UCP Client Bundle

See [docker-security.md](docker-security.md).

### Client certificates for administrators

See [docker-security.md](docker-security.md).
