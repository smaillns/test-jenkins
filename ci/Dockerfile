FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python3.7 python3-pip wait-for-it
COPY .. /mnt/application
WORKDIR /mnt/application
RUN pip3 install pipenv
# Nameko is a pre release version, we need --pre flag
RUN pipenv lock --pre -r > requirements.txt
RUN pip3 install -r requirements.txt

RUN export PYTHONPATH=/mnt/application
CMD alembic upgrade head && nameko run --config ci/config.yml installation_requests.service
