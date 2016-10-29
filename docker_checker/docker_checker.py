import docker
import logging
import socket
import sys
from os.path import basename

from . import *
from .utils import read_config_from_argv

APP_NAME = basename(__file__).split('.')[0]


class DockerChecker():

    def run(self, config):
        try:
            # retrieve docker login details
            dversion = config.get(SECTION_DOCKER, PARAM_DOCKER_VERSION).strip()

            # prepare docker client
            docker_client = docker.Client(version=dversion, base_url=DOCKER_BASE_URL)

            # check if there's any non-running containers and remove them
            c_list, msg = self.find_non_running_containers(docker_client, remove_container=True)

            # check if there's any dangling images and remove them
            i_list, msg2 = self.find_dangling_and_dev_images(docker_client, remove_image=True)

            # send notifications
            if len(c_list) + len(i_list) > 0:

                msg = '{}\n{}'.format(msg, msg2) if len(c_list) else msg2

                logging.info('Docker container/images cleanup ({})'.format(socket.gethostname()))
                logging.info(msg)

        except Exception as e:
            logging.error('{}: {}'.format(socket.gethostname(), e))
            return 1

        return 0

    def find_non_running_containers(self, docker_client, remove_container=True):
        """
        Use docker-py to retrieve non-running containers
        Alternatively we can use subprocess:
        subprocess.check_output(['sudo', 'docker', 'ps', '-f', 'status=exited', '--format', 'table {{.ID}}\t{{.Image}}\t{{.Status}}'])

        Use docker-py to remove non-running containers
        Alternatively we can use subprocess:
        subprocess.check_output('sudo docker rm $(sudo docker ps -q -f status=exited)', shell=True)
        """
        logging.info('Checking non-running containers ...')

        # filter by status
        # you can filter using created, restarting, running, paused, exited
        ret = docker_client.containers(filters={'status':'exited'})

        msg = 'Docker container check: Found {} non-running containers on {}\n\n'.format(len(ret), socket.gethostname())
        if len(ret) > 0:
            msg = '{}    ContainerId    Image    Status\n'.format(msg)

        # ret is a list of dict with keys [u'Status', u'Created', u'Image', u'Labels', u'HostConfig', u'Ports', u'Command', u'Names', u'Id']
        for i in ret:
            s_msg = ''
            if remove_container is True:
                try:
                    # remove the container by name (container may have more than one name, use the first in r['Names']
                    container_name = i['Names'][0].encode('utf-8')

                    docker_client.remove_container(container_name)

                    s_msg = 'Removed '
                except Exception as e:
                    logging.error('{}: {}'.format(socket.gethostname(), e))
                    s_msg = 'Unable to remove '

            msg = '{}    {}{}\t{}\t{}\n'.format(msg, s_msg, i['Id'], i['Image'], i['Status'])
        logging.info(msg)

        return ret, msg

    def find_dangling_and_dev_images(self, docker_client, remove_image=True):
        """
        Use docker-py to retrieve dangling images
        Alternatively we can use subprocess: sudo docker images -f "dangling=true"

        Use docker-py to remove dangling images
        Alternatively we can use subprocess: docker rmi $(docker images -q -f dangling=true)
        """
        logging.info('Checking dangling and .dev images ...')

        # find dangling images
        ret = docker_client.images(filters={'dangling':True})

        # find dev images
        ret2 = docker_client.images()
        for d in ret2:
            # d['RepoTags'] is a list of repo:version
            ret.extend([d for i in d['RepoTags'] if DEV_IMAGE_TAG in i.split(':')[1]])

        msg = 'Docker image check: Found {} dangling and dev images on {}\n\n'.format(len(ret), socket.gethostname())

        if len(ret) > 0:
            msg = '{}    RepoTags    Id\n'.format(msg)

        # ret is a list of dist with keys [u'Created', u'Labels', u'VirtualSize', u'ParentId', u'RepoTags', u'RepoDigests', u'Id', u'Size']
        for i in ret:
            s_msg = ''
            if remove_image is True:
                try:
                    # remove the image by id
                    image_id = i['Id'].encode('utf-8')

                    docker_client.remove_image(image_id)

                    s_msg = 'Removed '
                except Exception as e:
                    logging.error('{}: {}'.format(socket.gethostname(), e))
                    s_msg = 'Unable to remove '

            msg = '{}    {}{}\t{}\n'.format(msg, s_msg, i['RepoTags'], i['Id'])

        logging.info(msg)

        return ret, msg


def main():
    config = read_config_from_argv(sys.argv)
    if config is None:
        return 1

    return DockerChecker().run(config)


if __name__ == '__main__':
    sys.exit(main())
