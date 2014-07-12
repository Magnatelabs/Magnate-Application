#!/bin/bash

HEROKU_APP=magnate-prod
REMOTE_SHELL="heroku run python manage.py shell --app $HEROKU_APP"
LOCAL_SHELL="python manage.py shell"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# The file is in the same directory as the script itself
source "$DIR/test_credentials.pysh"



function remote_command() {
  CMD="$1"
  USERNAME="$2"
  PASSWORD="$3"
	echo -e "from glue_osqa.user import $CMD
print $CMD(\"$USERNAME\", \"$PASSWORD\"); exit()" | $REMOTE_SHELL | tail -n 1
}


function usage {
  name=`basename $0`
  echo "This tool connects to Heroku with 'heroku run python manage.py shell'"
  echo "Usage: $name [local] <command> [username] [password]"
  echo
  echo "$name has-test-user       See if there is a test user '$TEST_USERNAME'"
  echo "$name create-test-user    Create a test user '$TEST_USERNAME'"
  echo "$name has-user <user> <passwd>"
  echo "$name create-user <user> <passwd>"
  echo "$name create-siteowner <user> <passwd>"
}

if [ "$1" == "local" ]; 
then
  REMOTE_SHELL=$LOCAL_SHELL
  shift
fi

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
  create-siteowner)
    cmd=create_siteowner
    user="$2"
    passwd="$3"
    ;;
  *)
    usage
    exit
    ;;
esac

echo "Cmd: $cmd, user: $user"
echo "Connecting to $REMOTE_SHELL..."

remote_command "$cmd" "$user" "$passwd"
