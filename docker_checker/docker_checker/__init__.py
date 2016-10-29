################################################################################
# SECTION and PARAM names in config (ini) file

# Section docker
SECTION_DOCKER = 'docker'
PARAM_DOCKER_VERSION = 'docker.version'


################################################################################
# Default docker dock path
DOCKER_SOCK_FILE = '/var/run/docker.sock'

# Default Docker daemon
DOCKER_BASE_URL = 'unix:/{}'.format(DOCKER_SOCK_FILE)

# Default tag for DEV version of image
DEV_IMAGE_TAG = '.dev'
