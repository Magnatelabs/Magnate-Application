#!/bin/bash
# 
# Start local Selenium server for testing.
#
# First download the jar file to the current directory, if necessary.
# End with Ctrl+C.

SELENIUM_URL_PATH=http://selenium-release.storage.googleapis.com/2.42/
SELENIUM_FILE=selenium-server-standalone-2.42.2.jar
SELENIUM_FULL_URL="$SELENIUM_URL_PATH$SELENIUM_FILE"

if [ -f "$SELENIUM_FILE" ] 
then
    echo "File exists: $SELENIUM_FILE"
else
    echo "File does not exist: $SELENIUM_FILE"
    echo "Downloading from $SELENIUM_FULL_URL..."
    set -x
    wget "$SELENIUM_FULL_URL" || exit 1
fi

# Start the server
java -jar "$SELENIUM_FILE"

