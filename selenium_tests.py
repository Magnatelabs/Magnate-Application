#!/bin/bash

# Display all commands to ease debugging
# set -x

# Trap ctrl-c and call ctrl_c()
trap ctrl_c INT



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

# Start Django's Dev server
python manage.py runserver 8123 &
pid_django=$!
echo "Starting Django server, pid=$pid_django"

# Start Selenium server
# It may involve downloading the JAR file!
cd integration_tests
./selenium_server.sh &
pid_selenium=$!
echo "Starting Selenium server, pid=$pid_selenium"

sleep 5 # give them time to start

is_running $pid_django || { wait $pid_django;  echo "ERROR! Django server not running, returned exit code $?"; cleanup_and_exit 3; }

is_running $pid_selenium || { wait $pid_selenium; echo "ERROR! Selenium server not running, returned exit code $?"; cleanup_and_exit 4; }


sleep 4

cleanup_and_exit 0

