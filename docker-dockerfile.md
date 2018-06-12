# Dockerfile


1. There is no way to rebuild a Dockerfile from an existing image, although the 'history' option can be used to help see the commands that were run in building it.

1. EVERY directive in a Dockerfile, when executed, will create a new image layer when building an image.

1. The `ENTRYPOINT` directive in a Dockerfile will be the command that any container instantiated on the image will
 execute on startup by default, unless overridden when the container is started.

