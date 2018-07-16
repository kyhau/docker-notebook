# Docker Storage and Volumes

REF: https://docs.docker.com/storage/bind-mounts/

1. There is no way to add a volume to an instantiated container.


## Differences between -v and --mount behavior

1. If you use `-v` or `--volume` to bind-mount a file or directory that does not yet exist on the Docker host, `-v`
   creates the endpoint for you. It is always created as a directory.

1. If you use `--mount` to bind-mount a file or directory that does not yet exist on the Docker host, Docker does not
   automatically create it for you, but generates an error.


## Start a container with a bind mount

```bash
# Option 1: using --mount
docker run -d -it --name devtest --mount type=bind,source="$(pwd)"/target,target=/app nginx:latest

# Option 2: using -v
docker run -d -it --name devtest -v "$(pwd)"/target:/app nginx:latest

# Both options above have the same result
docker inspect devtest

# Output
...
"Mounts": [
    {
        "Type": "bind",
        "Source": "/tmp/source/target",
        "Destination": "/app",
        "Mode": "",
        "RW": true,
        "Propagation": "rprivate"
    }
],
```


## Mounting into a non-empty directory on the container

```bash
# Option 1: using --mount
docker run -d -it --name broken-container --mount type=bind,source=/tmp,target=/usr nginx:latest

# Option 2: using -v
docker run -d -it --name broken-container -v /tmp:/usr nginx:latest

# Both options have the same result:
docker: Error response from daemon: oci runtime error: container_linux.go:262:
starting container process caused "exec: \"nginx\": executable file not found in $PATH".

# The container is created but does not start. Remove it.
docker container rm broken-container
 ```


## Use a read-only bind mount

```bash
# Option 1: using --mount
docker run -d -it --name devtest --mount type=bind,source="$(pwd)"/target,target=/app,readonly nginx:latest

# Option 2: using -v
docker run -d -it --name devtest -v "$(pwd)"/target:/app:ro nginx:latest

# Both options above have the same result
docker inspect devtest

# Output
...
"Mounts": [
    {
        "Type": "bind",
        "Source": "/tmp/source/target",
        "Destination": "/app",
        "Mode": "ro",
        "RW": false,
        "Propagation": "rprivate"
    }
],
```


## Configure bind propagation

1. Bind propagation defaults to `rprivate` for both bind mounts and volumes. 
1. It is only configurable for bind mounts, and only on Linux host machines.
1. Bind propagation is an advanced topic and many users never need to configure it.
1. Bind propagation refers to whether or not mounts created within a given bind-mount or named volume can be
   propagated to replicas of that mount. Consider a mount point `/mnt`, which is also mounted on `/tmp`. The
   propagation settings control whether a mount on `/tmp/a` would also be available on `/mnt/a`. Each propagation
   setting has a recursive counterpoint. In the case of recursion, consider that `/tmp/a` is also mounted as `/foo`.
   The propagation settings control whether `/mnt/a` and/or `/tmp/a` would exist.

| Propagation setting | Description |
|---------------------|-------------|
| `shared`  | Sub-mounts of the original mount are exposed to replica mounts, and sub-mounts of replica mounts are also propagated to the original mount. |
| `slave`   | Similar to a shared mount, but only in one direction. If the original mount exposes a sub-mount, the replica mount can see it. However, if the replica mount exposes a sub-mount, the original mount cannot see it. |
| `private` | The mount is private. Sub-mounts within it are not exposed to replica mounts, and sub-mounts of replica mounts are not exposed to the original mount. |
| `rshared` | The same as shared, but the propagation also extends to and from mount points nested within any of the original or replica mount points. |
| `rslave`  | The same as slave, but the propagation also extends to and from mount points nested within any of the original or replica mount points. |
| `rprivate`| The default. The same as private, meaning that no mount points anywhere within the original or replica mount points propagate in either direction. |


## Storage Drivers

### Container size on disk

To view the approximate size of a running container, you can use the docker ps -s command. Two different columns relate to size.

- size: the amount of data (on disk) that is used for the writable layer of each container
- virtual size: the amount of data used for the read-only image data used by the container plus the container’s writable layer size. 


###  Copy-on-write (CoW) strategy

REF: https://docs.docker.com/storage/storagedriver/#container-size-on-disk

1. Copy-on-write (CoW) is a Docker strategy of sharing and copying files for maximum efficiency.


REF: https://docs.docker.com/storage/storagedriver/select-storage-driver/

### AUFS storage driver

1. AUFS is a union filesystem. 

### Btrfs storage driver

1. Btrfs is a next generation copy-on-write filesystem that supports many advanced storage technologies that make it a
   good fit for Docker.
1. Btrfs is included in the mainline Linux kernel.
1. btrfs storage driver is only supported on Docker CE on Ubuntu or Debian, and Docker EE / CS Engine on SLES.

### Device mapper storage driver 

1. Production hosts using the `devicemapper` storage driver must use `direct-lvm` mode.
1. This mode uses block devices to create the thin pool. This is faster than using `loopback` devices, uses system
   resources more efficiently, and block devices can grow as needed. However, more set-up is required than `loop-lvm`
   mode.

### OverlayFS storage driver

### ZFS storage driver

### VFS storage driver

