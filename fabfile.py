"""
Different tasks to ease the development workflow of the UGA website.
"""


import os

from fabric.api import *



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



def _deploy(instance, branch):
    with lcd(BASE):
        local('gondor deploy {instance} {branch}'.format(
                instance=instance, branch=branch))



def deploy_dev(branch=None):
    """
    Deploys the given branch or the current one if none is provided to the
    development instance.
    """
    branch = branch if branch else _get_current_branch(BASE)
    _deploy(env.instance_labels['dev'], branch)



def deploy_staging():
    """
    Deploys the develop branch to the staging instance.
    """
    _deploy(env.instance_labels['staging'], 'develop')



def deploy_prod():
    """
    Deploys the master branch to the production instance.
    """
    _deploy(env.instance_labels['staging'], 'master')
