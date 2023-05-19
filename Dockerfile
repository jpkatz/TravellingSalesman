#use ubuntu as the base image
FROM ubuntu:latest

#Set env variables
ENV PATH "/root/miniconda3/bin:${PATH}"

RUN apt-get update &&\
 apt-get -y install wget &&\
 wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh &&\
 bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3

RUN apt-get -y install git && \
 git clone https://github.com/jpkatz/TravellingSalesman.git

# TODO: Add environment.yml to path
RUN conda config --append channels conda-forge &&\
 conda install --file environment.yml
