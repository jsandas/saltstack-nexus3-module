#!/bin/bash

echo ""
echo "Waiting for admin.password to be generated"
_dur=0
_timeout=120
until docker exec nexus3 bash -c 'test -f /nexus-data/admin.password'
do
    if [ $_dur -gt $_timeout ]; then
        echo "Couldn't get admin password after $_timeout seconds"
        echo "Please check containers logs for details"
        echo " docker logs nexus3"
        exit 1
    fi
    _dur=$((_dur+1))
    sleep 1
    echo -ne "."
done