# docker-utils

## [Upgrade Docker](docker-upgrade.md)

## [Image signing](docker-image-signing.md)

## Clean up docker images and container

**Python:** 
[docker_checker](docker_checker/README.md)

**Command-line:**

1. Find all non-running containers (possible filters: created, restarting, running, paused, exited)
    ```sh
    $ docker rm $(docker ps -q -f status=exited)
    ```

2. Remove dangling (untagged) images
    ```sh
    docker rmi $(docker images -q -f dangling=true)
    ```

3.  Build a Docker image depending on another image from Docker registry.

    Edit "/etc/default/docker"
    ```sh
    DOCKER_OPTS="--insecure-registry <docker registry url>"
    ```

    Restart docker service

    ```sh
    $ sudo service docker restart
    ```
