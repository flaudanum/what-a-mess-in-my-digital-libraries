#!/usr/bin/bash

# If your default python version is earlier than version 3.5, you shall specify an absolute path to a version 3.5 or
# newer by updating the content of the variable PYTHON
PYTHON=`which python`

# Path to unit tests
UNIT_TESTS=./tests/unittests

PYTHON_VERSION=`$PYTHON --version |& awk '$1 ~ /^Python/ {print $2}' | awk 'BEGIN{FS="."} {print $1"."$2}'`
MAJOR_VERSION=`echo $PYTHON_VERSION | awk 'BEGIN{FS="."} {print $1}'`
MINOR_VERSION=`echo $PYTHON_VERSION | awk 'BEGIN{FS="."} {print $2}'`

if [ $MAJOR_VERSION -lt 3 ]; then
    echo
    echo "You are using python $MAJOR_VERSION.$MINOR_VERSION with command: $PYTHON"
    echo "Python version 3.5 or later version is required."
    echo "Please update variable PYTHON in the script ./script/config.sh with a path to a proper python executable."
    echo
    exit 1
fi

sed "s@#PYTHON#@$PYTHON@" ./scripts/whamdil.template | sed "s@#HOME#@`pwd`@" > ./scripts/whamdil
chmod a+x ./scripts/whamdil
echo "An executable script was created: `pwd`/scripts/whamdil"

echo "Run unit tests"
cd $UNIT_TESTS
$PYTHON test_ptree.py
$PYTHON test_compare.py
