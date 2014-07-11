#!/bin/bash

HEROKU_APP=magnate-prod
TEST_USERNAME=root
TEST_PASSWORD=root
function has_test_user() {
	output=`echo "from django.test import Client; c = Client(); c.login(username=\"$TEST_USERNAME\", password=\"$TEST_PASSWORD\"); exit()" | heroku run python manage.py shell --app $HEROKU_APP | tail -n 1`
	[ "$output" == "True" ] && return 0 || return 1
}


echo "Connecting to heroku app $HEROKU_APP..."
if ( has_test_user )
then
	echo "This app HAS a test user"
else
	echo "This app HAS NO test user"
fi
