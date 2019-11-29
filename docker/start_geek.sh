#!/usr/bin/env bash

# Usage:
#   ./build_geek_pcl.sh geek.Dockerfile

ARCH=$(uname -m)
IMG=geekstyle/geek_lite:geek_pcl-x86_64-18.04-20191129_1743

GEEK_ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

function local_volumes() {
    # Apollo root and bazel cache dirs are required.
    volumes="-v $GEEK_ROOT_DIR:/python_pcl \
             -v $HOME/.cache:${DOCKER_HOME}/.cache"
    case "$(uname -s)" in
        Linux)
            case "$(lsb_release -r | cut -f2)" in
                14.04)
                    volumes="${volumes} "
                    ;;
                *)
                    volumes="${volumes} -v /dev:/dev "
                    ;;
            esac
            volumes="${volumes} -v /media:/media \
                                -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
                                -v /etc/localtime:/etc/localtime:ro \
                                -v /usr/src:/usr/src \
                                -v /lib/modules:/lib/modules"
            ;;
        Darwin)
            # MacOS has strict limitations on mapping volumes.
            chmod -R a+wr ~/.cache/bazel
            ;;
    esac
    echo "${volumes}"
}


function main(){
    echo "Start pulling docker image $IMG ..."
    docker pull $IMG
    if [ $? -ne 0 ];then
        error "Failed to pull docker image."
        exit 1
    fi

    GEEK_DOCKER="geek_${USER}"
    docker ps -a --format "{{.Names}}" | grep "$GEEK_DOCKER" 1>/dev/null
    if [ $? == 0 ]; then
        docker stop $GEEK_DOCKER 1>/dev/null
        docker rm -v -f $GEEK_DOCKER 1>/dev/null
    fi

    local display=""
    if [[ -z ${DISPLAY} ]];then
        display=":0"
    else
        display="${DISPLAY}"
    fi

    USER_ID=$(id -u)
    GRP=$(id -g -n)
    GRP_ID=$(id -g)
    LOCAL_HOST=`hostname`
    DOCKER_HOME="/home/$USER"
    if [ "$USER" == "root" ];then
        DOCKER_HOME="/root"
    fi
    if [ ! -d "$HOME/.cache" ];then
        mkdir "$HOME/.cache"
    fi

    echo "Starting docker container \"${GEEK_DOCKER}\" ..."

    DOCKER_CMD="nvidia-docker"
    USE_GPU=1
    if ! [ -x "$(command -v ${DOCKER_CMD})" ]; then
        DOCKER_CMD="docker"
        USE_GPU=0
    fi

    ${DOCKER_CMD} run -it \
        -d \
        --privileged \
        --name $GEEK_DOCKER \
        -e DISPLAY=$display \
        -e DOCKER_USER=$USER \
        -e USER=$USER \
        -e DOCKER_USER_ID=$USER_ID \
        -e DOCKER_GRP="$GRP" \
        -e DOCKER_GRP_ID=$GRP_ID \
        -e DOCKER_IMG=$IMG \
        -e USE_GPU=$USE_GPU \
        -e OMP_NUM_THREADS=1 \
        $(local_volumes) \
        --net host \
        -w /python_pcl \
        --add-host in_geek_docker:127.0.0.1 \
        --add-host ${LOCAL_HOST}:127.0.0.1 \
        --hostname in_geek_docker \
        --shm-size 2G \
        --pid=host \
        -v /dev/null:/dev/raw1394 \
        $IMG \
        /bin/bash

    if [ $? -ne 0 ];then
        error "Failed to start docker container \"${GEEK_DOCKER}\" based on image: $IMG"
        exit 1
    fi

    if [ ${ARCH} == "x86_64" ]; then
        if [ "${USER}" != "root" ]; then
            docker exec $GEEK_DOCKER bash -c 'docker_adduser.sh'
        fi
    else
        echo "!!! Due to the problem with 'docker exec' on Drive PX platform, please run 'docker_adduser.sh' for the first time when you get into the docker !!!"
    fi

    echo "Finished setting up Geek docker environment. Now you can enter with: \nbash docker/into_geek.sh"
    echo "Enjoy!"
}

main