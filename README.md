# docker-stuff

### To find all non-running containers (possible filters: created, restarting, running, paused, exited)
````sh
$ docker rm $(docker ps -q -f status=exited)
````

### To remove dangling (untagged) images
````sh
docker rmi $(docker images -q -f dangling=true)
````

### To build a Docker image depending on another image from Docker registry.
Edit "/etc/default/docker"
````sh
DOCKER_OPTS="--insecure-registry <docker registry url>"
````

Restart docker service

````sh
$ sudo service docker restart
````
