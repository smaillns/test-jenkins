#!/bin/bash

SSH_USER=$1
SSH_IP=$2
SSH_KEY=$3
SSH_PROJECT_FOLDER=$4

(
    ssh $SSH_USER@$SSH_IP -i $SSH_KEY -o StrictHostKeyChecking=no <<-EOF
    export ID_RSA_KEY=$(cat $HOME/.ssh/jwt_id_rsa)
    cd $SSH_PROJECT_FOLDER
    docker-compose pull
    docker-compose stop
    docker-compose up -d
EOF
)
