# Docker Image Creation, Management, and Registry

### Dockerfile

1. There is no way to rebuild a Dockerfile from an existing image, although the 'history' option can be used to help
   see the commands that were run in building it.

```bash
# The first line can be a comment
FROM debian:stable                        # FROM image_name[:tag] [AS name]

ARG VARIABLE_NAME=xxx
ARG FROM base:${VARIABLE_NAME}

ENV ENVIRONMENT="production"

LABEL key=value                           # Add metadata to an image

LABEL maintainer="user1@email.com"        # MAINTAINER (deprecated): use LABEL maintainer

RUN apt-get update && \
    apt-get install -y --force-yes apache2
                      # Execute any commands in a new layer on top of the current image and commit the results

CMD echo "Check container IP"
                      # CMD Command the container to start, only the last CMD will be run if multiple specified 

EXPOSE 80 443         # EXPOSE <port> [<port>/<protocol>...] 
                      # Inform Docker that the container listens on the specified network ports at runtime
                      # Does NOT publish the port to external systems.

VOLUME ["/var/www", "/var/log/apache2", "/etc/apache2"]
                      # Create a mount point with the specified name and marks it as holding externally
                      # mounted volumes from native host or other containers

ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
```

1. EVERY directive in a Dockerfile, when executed, will create a new image layer when building an image.

1. The `ENTRYPOINT` directive in a Dockerfile will be the command that any container instantiated on the image will
 execute on startup by default, unless overridden when the container is started.

1. Build cache is only used from images that have a local parent chain.

1. Parser directives are optional, and affect the way in which subsequent lines in a Dockerfile are handled. Once a
   comment, empty line or builder instruction has been processed, Docker no longer looks for parser directives.

1. Escape character: \ or `

1. Environment variables
   1. ${variable:-word} indicates that if variable is set then the result will be that value. If variable is not set
      then word will be the result.
   1. ${variable:+word} indicates that if variable is set then word will be the result, otherwise the result is the
      empty string.
1. Environment variables are supported by the following list of instructions in the Dockerfile:
   1. ADD
   1. COPY
   1. ENV
   1. EXPOSE
   1. FROM
   1. LABEL
   1. STOPSIGNAL
   1. USER
   1. VOLUME
   1. WORKDIR
   1. ONBUILD (when combined with one of the supported instructions above)

1. Create an efficient image via a Dockerfile
   1. Start with an appropriate base image
   1. Avoid installing unnecessary packages
   1. Use multi-stage builds


### Build Docker Image

```bash
# When the Dockerfile is in the current context (directory), you build it with an image name and tag with the
# -t option followed by the image:tag and the directory context of the file, in this case '.'.
docker build -t myimage:v1 .

# Run it in the background (detach mode)
% docker run -d --name testweb1 --rm mywebserver:v1

# Verify if the apache server is running
% docker inspect testweb1 | grep IPAddress
% elinks http://172.12.0.2

# To see how many layers in the image
% docker history mywebserver:v1 | wc -l
12
```


### Tag and Push Docker Image

```bash
docker push [OPTIONS] NAME[:TAG]

docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
```
