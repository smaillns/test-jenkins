FROM ubuntu:20.04
MAINTAINER Fouad CHENNOUF<fouad@myem.fr>
RUN apt-get update && \
    apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.7 python3-pip wait-for-it
COPY ./ /mnt/application
WORKDIR /mnt/application
RUN pip3 install pipenv
# Nameko is a pre release version, we need --pre flag
RUN pipenv lock --pre -r > requirements.txt
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/bin/bash", "-c" ]
