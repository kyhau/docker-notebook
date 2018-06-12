# Dockerfile


1. EVERY directive in a Dockerfile, when executed, will create a new image layer when building an image.

1. The `ENTRYPOINT` directive in a Dockerfile will be the command that any container instantiated on the image will
 execute on startup by default, unless overridden when the container is started.

