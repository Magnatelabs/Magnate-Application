#!/bin/bash

# Display all commands to ease debugging
# set -x

# Trap ctrl-c and call ctrl_c()
trap ctrl_c INT

# Port to run the Django development server
DJANGO_PORT=8123


# Terminate all child processes
function killtree() {
    local _pid=$1
    local _sig=$2

    if [ ${_pid} -ne $$ ]; # Do not send it to itself, though
    then
	kill -stop ${_pid} 2>/dev/null # needed to stop quickly forking parent from producing children between child killing and parent killing
    fi

    for _child in $(ps -o pid --no-headers --ppid ${_pid}); do
        killtree ${_child} ${_sig}
    done

    if [ ${_pid} -ne $$ ]; # Do not kill itself, thuogh
    then
	kill -${_sig} ${_pid} 2>/dev/null
    fi
}

# Check if a process with a given pid is still running.
# Exit code 0 means that it IS running
function is_running() {
    local _pid=$1
    [ `ps -ef | grep -v grep | grep -w $_pid | wc -l` -ne 0 ] || return 1
}

function cleanup_and_exit() {
    # Terminate all child processes
    killtree $$ TERM
    exit $1
}

function ctrl_c() {
    echo "Terminated with Ctrl+C"
    cleanup_and_exit 143 
}


# Detect if running under python virtualenv. Will be "True" or "False".
# May not work well with Python 3. 
# http://stackoverflow.com/questions/1871549/python-determine-if-running-inside-virtualenv
INSIDE_VIRTUALENV=`python -c "import sys; print hasattr(sys, 'real_prefix')"`

if [ "$INSIDE_VIRTUALENV" != "True" ] && [ "$DATABASE_URL" == "" ];
then
    echo "VIRTUALENV is not active, and we are not on Heroku either. Cannot run the tests. Exiting."
    cleanup_and_exit 1
fi


# Start Django's Dev server
python manage.py runserver $DJANGO_PORT &
pid_django=$!
echo "Starting Django server, pid=$pid_django"

# Start Selenium server
# It may involve downloading the JAR file!
cd integration_tests
##./selenium_server.sh &
##pid_selenium=$!
##echo "Starting Selenium server, pid=$pid_selenium"

sleep 5 # give them time to start

is_running $pid_django || { wait $pid_django;  echo "ERROR! Django server not running, returned exit code $?"; cleanup_and_exit 3; }

##is_running $pid_selenium || { wait $pid_selenium; echo "ERROR! Selenium server not running, returned exit code $?"; cleanup_and_exit 4; }



# Great! Both Django and Selenium are up and running. Now run the tests...
# Remember, we are still inside integration_tests/
python all_selenium_tests.py
exit_code=$?

cleanup_and_exit $exit_code

