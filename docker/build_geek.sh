#!/usr/bin/env bash

# Usage:
#   ./build_geek_pcl.sh geek.Dockerfile
# Commit 
# docker commit 5a69f1c7051c geekstyle/geek_lite:geek_pcl
DOCKERFILE=$1

CONTEXT="$(dirname "${BASH_SOURCE[0]}")"

REPO=geekstyle/geek_lite
ARCH=$(uname -m)
TIME=$(date +%Y%m%d_%H%M)

TAG="${REPO}:geek_pcl-${ARCH}-18.04-${TIME}"

# Fail on first error.
set -e
if [[ $DOCKERFILE == *$ARCH* ]]; then
    echo "docker file gets matched"
    docker build -t ${TAG} -f ${DOCKERFILE} ${CONTEXT}
else
    echo "docker file '$DOCKERFILE' doesn't match"
    exit
fi

echo "Built new image ${TAG}"


# Please provide credential if you want to login automatically.
DOCKER_USER=""
DOCKER_PASSWORD=""
if [ ! -z "${DOCKER_PASSWORD}" ]; then
  docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD} ${DOCKER_REGISTRY}
fi

docker push ${TAG}


function gen_docker(){
    CONTAINER_ID=$(docker ps | grep geek_${USER}| awk '{print $1}')
    docker commit "$CONTAINER_ID" "$DEFAULT_NAME"
    docker tag "$DEFAULT_NAME" "$RELEASE_NAME"
    docker stop "$CONTAINER_ID"
}