#!/bin/sh

check_result() {
    RESULT=$?
    [ $RESULT -ne 0 ] && exit 1
}

make lint
check_result

make test
check_result

exit 0
