FROM ubuntu:latest

RUN apt-get -y install python3 wget && \
    python3 -m pip install backoff && \
    wget http://www.christianbenner.com/finemap_v1.4_x86_64.tgz && \
    tar xfvz finemap_v1.4_x86_64.tgz && \
    cp finemap_v1.4_x86_64/finemap_v1.4_x86_64 /bin/finemap
