from setuptools import setup, find_packages

version = '1.0.0.dev0'

requirements = [
    'docker-py==1.10.5',
]

entry_points = {
    'console_scripts': [
        'docker_checker = docker_checker.docker_checker:main'
    ],
    'gui_scripts': []
}

setup(
    name='docker_checker',
    version=version,
    description="Docker Checker",
    author='Kayan Hau',
    author_email='virtualda@gmail.com',
    url="https://github.com/kyhau/docker-stuff",
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=requirements,
    entry_points=entry_points,
)
