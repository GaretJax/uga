"""
Different tasks to ease the development workflow of the UGA website.
"""


import os
import subprocess

from fabric.api import *
from fabric.contrib.project import rsync_project


env.hosts = ['garetjax.info']


BASE = os.path.dirname(__file__)

env.instance_labels = {
    'dev': 'development',
    'staging': 'staging',
    'production': 'production',
}



def _get_current_branch(repository):
    """
    Returns the current active branch on the given git repository.
    """

    with lcd(repository):
        out = local('git branch', capture=True)

    for branch in out.strip().splitlines():
        if branch.startswith('*'):
            return branch.split(' ', 1)[-1]

def deploy_dev(branch=None):
    """
    Deploys the given branch or the current one if none is provided to the
    development instance.
    """
    branch = branch if branch else _get_current_branch(BASE)
    _deploy(env.instance_labels['dev'], branch)


def upload():
    REMOTE_KEEP = [
        'apache2',
        'bin',
        'collected-static',
        'lib',
        'media'
    ]

    LOCAL_IGNORE = [
        '.git*',
        '.DS_Store',
        '.gondor',
        '.sass-cache',
        '.virtualenv',
        'Gemfile*',
        'Guardfile',
        'collected-static',
        'fabfile.py',
        'media',
        'support',
        '*.pyc',
        'settings/development.py',
    ]

    rsync_project(
        remote_dir='/home/garetjax/webapps/uga_django',
        local_dir='.',
        exclude=set(REMOTE_KEEP + LOCAL_IGNORE),
        delete=True
    )


def restart():
    run('touch /home/garetjax/webapps/uga_django/myproject.wsgi')


def push():
    upload()
    restart()


def rundev():
    with lcd(BASE):
        guard = subprocess.Popen(['bundle', 'exec', 'Guard'])
        try:
            while True:
                server = subprocess.Popen(['./manage.py', 'runserver'])
                server.wait()
        except KeyboardInterrupt:
            guard.wait()
            server.wait()
