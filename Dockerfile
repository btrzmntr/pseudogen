FROM ubuntu:16.04

RUN apt update && \
	apt install -y git libboost-all-dev autoconf automake autotools-dev libtool zlib1g-dev cmake build-essential python3 python3-pip wget && \
	pip3 install nltk && \
    pip3 install sqlparse && \
    sysctl vm.swappiness=1
ARG CACHE_DATE=2016-01-04
RUN git clone https://github.com/btrzmntr/pseudogen.git && \
	cd pseudogen && \
	./tool_setup.sh && \
	#mkdir data && \
	cd data && \
	wget -O- http://ahclab.naist.jp/pseudogen/en-django.tar.gz | tar zxvf - && \
	mv en-django/all.* . 

ARG CACHE_DATE=2016-01-31
RUN cd pseudogen && \
    git config --global user.email "btrzmntr@gmail.com" && \
    git config --global user.name "Beatriz" && \
    git stash && \
    git pull