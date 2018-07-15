# Dockerfile

```bash
# The first line can be a comment
FROM debian:stable                        # FROM image_name[:tag] [AS name]

ARG VARIABLE_NAME=xxx
ARG FROM base:${VARIABLE_NAME}

ENV ENVIRONMENT="production"

LABEL key=value                           # Add metadata to an image

LABEL maintainer="user1@email.com"        # MAINTAINER (deprecated): use LABEL maintainer

USER <user>[:<group>] or <UID>[:<GID>]

WORKDIR /path/to/workdir
                      # The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT, COPY
                      # and ADD instructions that follow it in the Dockerfile. If the WORKDIR doesn’t exist,
                      # it will be created.
                      # even if it’s not used in any subsequent Dockerfile instruction.
                      # The WORKDIR instruction can be used multiple times in a Dockerfile. If a relative
                      # path is provided, it will be relative to the path of the previous WORKDIR
                      # instruction. 

ADD <src> <dest>      # Copying files, directories, url, tar file from the host to the image during build

COPY <src> <dest>     # Same as 'ADD', but without the tar and remote URL handling.

RUN apt-get update && \
    apt-get install -y --force-yes apache2
                      # Execute any commands in a new layer on top of the current image and commit the results

EXPOSE 80 443         # EXPOSE <port> [<port>/<protocol>...] 
                      # Inform Docker that the container listens on the specified network ports at runtime
                      # Does NOT publish the port to external systems.

VOLUME ["/var/www", "/var/log/apache2", "/etc/apache2"]
                      # Create a mount point with the specified name and marks it as holding externally
                      # mounted volumes from native host or other containers

CMD echo "Check container IP"
                      # CMD Command the container to start, only the last CMD will be run if multiple specified.
                      # The CMD instruction has three forms:
                      #   CMD ["executable","param1","param2"] (exec form, this is the preferred form)
                      #   CMD ["param1","param2"] (as default parameters to ENTRYPOINT)
                      #   CMD command param1 param2 (shell form)

ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
                      # The command that any container instantiated on the image will execute on startup by
                      # default, unless overridden when the container is started.

ONBUILD [INSTRUCTIONS]
                      # The ONBUILD instruction adds to the image a trigger instruction to be executed at a
                      # later time, when the image is used as the base for another build. The trigger will be
                      # executed in the context of the downstream build, as if it had been inserted immediately
                      # after the FROM instruction in the downstream Dockerfile.

```

1. There is no way to rebuild a Dockerfile from an existing image, although the 'history' option can be used to help
   see the commands that were run in building it.

1. EVERY directive in a Dockerfile, when executed, will create a new image layer when building an image.

1. Build cache is only used from images that have a local parent chain.

1. Parser directives are optional, and affect the way in which subsequent lines in a Dockerfile are handled. Once a
   comment, empty line or builder instruction has been processed, Docker no longer looks for parser directives.

1. Escape character: `\` or `

1. `CMD` vs. `ENTRYPOINT`
   1. Docker has a default entrypoint which is `/bin/sh -c` but does not have a default command.

   1. When you run docker like this: `docker run -i -t ubuntu bash`, the entrypoint is the default `/bin/sh -c`,
      the image is `ubuntu` and the command is `bash`.

   1. The command is run via the entrypoint. i.e., the actual thing that gets executed is `/bin/sh -c bash`. 
      This allowed Docker to implement `RUN` quickly by relying on the shell's parser.

1. Environment variables
   1. `${variable:-word}` indicates that if variable is set then the result will be that value. If variable is not set
      then word will be the result.
   1. `${variable:+word}` indicates that if variable is set then word will be the result, otherwise the result is the
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


## Example of building a image and running a container

```bash
# When the Dockerfile is in the current context (directory), you build it with an image name and tag with the
# --tag|-t option followed by the image:tag and the directory context of the file, in this case '.'.
docker build -t mywebserver:v1 .

# Run it in the background (detach mode: --detach|-d) and remove at the end (--rm)
% docker run -d --name testweb1 --rm mywebserver:v1

# Verify if the apache server is running
% docker inspect testweb1 | grep IPAddress
% elinks http://172.12.0.2

# To see how many layers in the image
% docker history mywebserver:v1 | wc -l
12
```
