# Docker image signing
Docker supports image signing since Docker 1.8 (implemented as a separate piece of plumbing called Notary).

Target version to be updated to > Docker 1.8 (Docker registry 2.1)

When content trust is enabled,

1. The docker CLI commands that operate on tagged images must either have content signatures or explicit content hashes. The commands that operate with content trust are: push, build, create, pull, run

2. The Docker client only allows docker pull to retrieve signed images.  However, an operation with an explicit content hash always succeeds as long as the hash exists:
E.g. $ docker pull someimage@sha256:d149ab53f8718e987c3a3024bb8aa0e2caadf6c0328f1d9d850b2a2a67f2819a

3. Trust for an image tag is managed through the use of signing keys. A key set is created when an operation using content trust is first invoked. A key set consists of the following classes of keys

    3.1 An offline key is used to create tagging keys. Offline keys belong to a person or an organisation. Resides client-side. You should store these in a safe place and back them up.

    3.2 A tagging key is associated with an image repository. Creators with this key can push or pull any tag in this repository. This resides on client-side.

    3.3 A timestamp key is associated with an image repository. This is created by Docker and resides on the server.

See more details in https://docs.docker.com/engine/security/trust/content_trust/
