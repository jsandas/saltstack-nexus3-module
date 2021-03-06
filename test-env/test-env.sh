#!/bin/bash

START=0
STOP=0
RELOAD_MINION=0
CMD=0

docker_shell () {
    docker exec -it salt-master ash
}
    
start () {
    docker-compose pull
    docker-compose up -d

    # dependencies required for gitfs testing
    # echo ""
    # echo "installing dependencies..."
    # docker exec salt-master sh -c "apk --no-cache add git libgit2-dev && pip3 install pygit2"

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

    # sync salt files for the first time
    docker exec salt-master sh -c 'salt \* saltutil.sync_all' > /dev/null 2>&1
    docker-compose restart salt-minion

    echo ""
    echo "admin password: $(docker exec nexus3 bash -c 'cat /nexus-data/admin.password')"
    echo ""
}

stop () {
    docker-compose down
}

reload () {
    docker exec -it salt-master salt-key -D -y
    docker rm -f salt-minion
    docker-compose up -d  
    docker exec salt-master sh -c 'salt \* saltutil.sync_all' > /dev/null 2>&1
    docker-compose restart salt-minion  
}

usage () {
    echo "invalid input"
    echo " Usage:" 
    echo " ./salt-env (start|stop|reload|cmd) ARGS"
    echo ""
}

_setup_minio () {
    echo "setting up minio..."
    docker-compose exec minio curl -o /usr/bin/mc https://dl.min.io/client/mc/release/linux-amd64/mc
    docker-compose exec minio chmod +x /usr/bin/mc
    docker-compose exec minio mc mb local/nexus3
    echo "done"
}

while [[ $# -gt 0 ]]
do
    key=$1
    case "$key" in
        start)
        START=1
        shift # past argument
        ;;
        stop)
        STOP=1
        shift # past argument
        ;;
        reload)
        RELOAD_MINION=1
        shift # past argument
        ;;
        cmd)
        CMD=1
        shift # past argument
        ;;
    esac
done

if [[ $START -gt 0 ]]; then
    start
    _setup_minio
elif [[ $STOP -gt 0 ]]; then
    stop
elif [[ $RELOAD_MINION -gt 0 ]]; then
    reload
elif [[ $CMD -gt 0 ]]; then
    docker_shell
else
    usage
fi