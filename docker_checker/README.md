# docker-checker
================

# Description

Utility tools for solver server maintenance

**docker_checker**

To be run on a server and check if there are any non running docker containers,
dangling images and dev images, if so, delete them.

    docker_checker config/infrastructure.ini

# Locally Installing / Testing 

**Create Virtual Environment**

*Linux:*

    virtualenv env
    . env/bin/activate

*Windows:*

    virtualenv env
    env\bin\activate


**Install the Application and its Dependencies**

    pip install -e .
