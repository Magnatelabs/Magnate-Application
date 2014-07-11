#!/bin/bash

HEROKU_APP=magnate-prod
TEST_USERNAME=root2363432r322332
TEST_PASSWORD=root

function has_user() {
  USERNAME="$1"
  PASSWORD="$2"
	output=`echo "from django.test import Client; c = Client(); c.login(username=\"$USERNAME\", password=\"$PASSWORD\"); exit()" | heroku run python manage.py shell --app $HEROKU_APP | tail -n 1`
	[ "$output" == "True" ] && return 0 || return 1
}

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
    User.objects.create(username='$USERNAME', password='$PASSWORD')
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


echo "Connecting to heroku app $HEROKU_APP..."
#if ( has_test_user )
#then
#	echo "This app HAS a test user"
#else
#	echo "This app HAS NO test user"
#fi

create_user "$TEST_USERNAME" "$TEST_PASSWORD"
code=$?
if [ $code -eq 0 ]; then
  echo "OK, created test user '$TEST_USERNAME'"
else
  echo "ERROR: cannot create a test user"
  echo "$error"
fi
