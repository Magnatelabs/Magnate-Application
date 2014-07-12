#!/bin/bash

HEROKU_APP=magnate-prod

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# The file is in the same directory as the script itself
source "$DIR/test_credentials.pysh"

# Check if there is such a user in a django Heroku app.
# Log into Heroku using heroku run python manage.py shell 
# Assumes that the name of the heroku app is $HEROKU_APP
# @arg  USERNAME
# @arg   PASSWORD
# @returns   0 if there is such a user (USERNAME, PASSWORD), 
#            1 if there is no such user USERNAME,
#            2 if the password is incorrect, but the user exists,
#            3 otherwise (just in case)
function has_user() {
  USERNAME="$1"
  PASSWORD="$2"
	echo -e "from glue_osqa.user import has_user
print has_user(\"$USERNAME\", \"$PASSWORD\"); exit()" | heroku run python manage.py shell --app $HEROKU_APP | tail -n 1
}

# Create a user in a django Heroku app. Uses user model forum.models.User
# Assumes that the name of the heroku app is $HEROKU_APP
# @arg  USERNAME
# @arg  PASSWORD
# @returns   0 on success, 1 if the user already exists, 2 on other errors
# Sets $error if the return value is not 0.
function create_user() {
  USERNAME="$1"
  PASSWORD="$2"
	echo -e "from glue_osqa.user import create_user
print str(create_user(\"$USERNAME\", \"$PASSWORD\")); exit()" | heroku run python manage.py shell --app $HEROKU_APP | tail -n 1
}


function usage {
  name=`basename $0`
  echo "This tool connects to Heroku with 'heroku run python manage.py shell'"
  echo "Usage:"
  echo "$name has-test-user       See if there is a test user '$TEST_USERNAME'"
  echo "$name create-test-user    Create a test user '$TEST_USERNAME'"
  echo "$name has-user <user> <passwd>"
  echo "$name create-user <user> <passwd>"
}

case $1 in
  has-test-user)
    cmd=has_user
    user="$TEST_USERNAME"
    passwd="$TEST_PASSWORD"
    ;;
  has-user)
    cmd=has_user
    user="$2"
    passwd="$3"
    ;;
  create-test-user)
    cmd=create_user
    user="$TEST_USERNAME"
    passwd="$TEST_PASSWORD"
    ;;
  create-user)
    cmd=create_user
    user="$2"
    passwd="$3"
    ;;
  *)
    usage
    exit
    ;;
esac

echo "Cmd: $cmd, user: $user"
echo "Connecting to heroku app $HEROKU_APP..."
$cmd "$user" "$password"
