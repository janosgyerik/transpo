#!/bin/sh

cd $(dirname "$0")/..

. ./scripts/include.sh

for app in ${apps[@]}; do
    msg running tests for $app ...
    ./manage.sh test $app
    echo
done
