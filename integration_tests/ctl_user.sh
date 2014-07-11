#!/bin/bash

HEROKU_APP=magnate-prod


source ./test_credentials.pysh

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
	output=`echo -e "from django.test import Client
c = Client()
if c.login(username=\"$USERNAME\", password=\"$PASSWORD\"):
  print 0; exit()

import forum
from forum.models.user import User
try:
  User.objects.get(username='$USERNAME')
  print 2; exit()
except forum.models.user.User.DoesNotExist:
  print 1; exit()

print 3; exit()" | heroku run python manage.py shell --app $HEROKU_APP | tail -n 1`
  return $output
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
	output=`echo -e "import forum
from forum.models.user import User
try:
  User.objects.get(username='$USERNAME')
  print 1; exit()
except forum.models.user.User.DoesNotExist:
  try:
    u=User.objects.create(username='$USERNAME')
    u.set_password('$PASSWORD')
    u.save()
    print 0; exit()
  except Exception as e:
    print str(e); exit()

exit()" | heroku run python manage.py shell --app $HEROKU_APP`
  last_output_line=`echo "$output" | tail -n 1`
  [ "$last_output_line" == "0" ] && return 0
  if [ "$last_output_line" == "1" ]; 
  then
    error="User '$USERNAME' already exists"
    return 1
  fi
	error="$output"
  return 2
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
if [ "$cmd" == "has_user" ]; 
then
  has_user "$user" "$passwd"
  case $? in
    0)
      echo "There IS a user '$user'"
      ;;
    1)
      echo "There is NO user '$user'"
      ;;
    2)
      echo "Wrong password, but the user '$user' exists"
      ;;
    *)
      echo "Unknown error"
      ;;
  esac
elif [ "$cmd" == "create_user" ];
then
  create_user "$user" "$passwd"
  code=$?
  if [ $code -eq 0 ]; then
    echo "OK, created user '$user'"
  else
    echo "ERROR: cannot create the user '$user'"
    echo "$error"
  fi
else
  usage
  exit
fi
