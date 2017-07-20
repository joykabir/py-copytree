#!/usr/bin/env bash

set -e
set -x

ROOT_DIR=$(pwd)

# Required packages
pip install --upgrade\
 pytest\
 pylint

cd $ROOT_DIR
find . -name \*.pyc -delete -print
find . -name __pycache__ -delete -print

echo "##[Test running: 'pytest']"
(py.test\
  --showlocals\
  --junit-xml=$ROOT_DIR/tests/pytest-result.xml
 result=$?
 echo "py.test exit code: $result"
 if [ $result -ge 2 ]; then exit $result; fi)
