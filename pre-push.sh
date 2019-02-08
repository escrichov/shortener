#!/bin/sh

make lint
RESULT=$?
[ $RESULT -ne 0 ] && exit 1

make test
RESULT=$?
[ $RESULT -ne 0 ] && exit 1

exit 0
