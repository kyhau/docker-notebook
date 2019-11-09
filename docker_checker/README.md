# docker-checker

Check if there are any non running docker containers, dangling images and dev images, if so, delete them.

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

**Create a config/ini file**

    [docker]
    docker.version=<docker_version>

**Run**

    python docker_checker\docker_checker.py <config-file>

