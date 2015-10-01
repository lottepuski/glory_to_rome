#!/usr/bin/env bash

# Check if in virtualenv
python -c 'import sys; print sys.real_prefix' &>/dev/null && INVENV=1 || INVENV=0

if [[ ${INVENV} == 0 ]]; then
    echo "Activating ..."
    source gtr/bin/activate
fi

python test_client_sm.py