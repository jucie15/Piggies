# 장고 배포를 위한 서버 셋팅

# ubuntu 설치
FROM       ubuntu:18.04
MAINTAINER gustos@sinamon.io
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3-dev python3-pip libpq-dev python3-venv && \
    apt-get install -y postgresql postgresql-contrib nginx

# 소스 복사
COPY . /home/kmhk/

WORKDIR /home/kmhk

CMD echo 'python=python3' > ~/.bashrc \
    echo 'pip=pip3' > ~/.bashrc && \
    source ~/.bashrc

EXPOSE 8000 80

