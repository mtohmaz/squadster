FROM ubuntu:16.04


RUN apt-get update \
    && apt-get remove python-pip \
    && apt-get -y upgrade \
    && apt-get install -y \
        postgresql \
        postgresql-contrib \
        python3-pip


CMD /bin/bash
EXPOSE 8000
