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

function cleanup() {
    # Terminate all child processes
    killtree $$ TERM
}

function ctrl_c() {
    echo "Terminated with Ctrl+C"
    cleanup 
    exit 143
}

# Start Django's Dev server
python manage.py runserver 8123&


sleep 3



cleanup

exit 0
