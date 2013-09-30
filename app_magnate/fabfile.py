from fabric.api import local
from fabric.api import lcd


def prepare_deployment(branch_name):
#    local('python manage.py test myapp') *I do not have tests setup properly
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)

"""
Above runs the tests, commits the branch changes, 
and merges them into master.
"""

def deploy():
    with lcd('~/Documents/new/Smelly/'):
        local('git pull ~/Dropbox/Magnate/Application/')
#        local('python manage.py migrate myapp') *South is not installed yet
#        local('python manage.py test myapp') *I do not have tests setup properly
#        local('/my/command/to/restart/webserver')

"""
This will pull changes from the development master branch, 
run any migrations that have beene made, run tests, 
and restart the webserver.
"""
