FROM ubuntu:bionic
RUN apt-get update && \
      apt-get -y install sudo vim curl wget net-tools default-jdk

RUN useradd -m dku && echo "dku:dku" | chpasswd && adduser dku sudo
USER dku
WORKDIR /home/dku
COPY install.sh install.sh
CMD /bin/bash