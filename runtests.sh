#!/usr/bin/env bash
set -e

TEST_PACKAGES="boxfile_manager"

while getopts "1s" opt; do
    case $opt in
        1) RUN_ONCE=1;;
        s) numprocs=1;;
    esac
done

shift $((OPTIND - 1))

if [ -z $numprocs ]; then
    if [ -e "/proc/cpuinfo" ]; then
        numprocs=$(cat /proc/cpuinfo  | grep processor | wc -l | cut -d ' ' -f 1)
    elif [ "x$(uname)" = "xDarwin" ]; then
        numprocs=$(sysctl -n hw.ncpu)
    else
        numprocs=1
    fi
fi

export PYTHONDONTWRITEBYTECODE=1  # Avoid .pyc files that can mess up coverage

test_cmd="
    echo 'Removing pyc files';\
    echo 'Running hypernode-box-manager software tests';
    echo $TEST_PACKAGES | xargs -n 1 nosetests --processes=$numprocs;
    echo 'Running PEP8 tests';
    echo $TEST_PACKAGES | xargs -n 1 autopep8 -ri --select E303,E302,E261,E231;
"

find . -type f -name *.pyc -delete

if [ -z $RUN_ONCE ]; then
	watch -c -n 0.1 -- "$test_cmd"
else
	sh -ec "$test_cmd"
fi

