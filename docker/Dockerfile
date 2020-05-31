# FROM ubuntu
# FROM alpine:3.7

FROM python:3.7-stretch

MAINTAINER Mohammad Nadji-Tehrani

#RUN apk upgrade --update && apk add --no-cache python3 python3-dev gcc gfortran freetype-dev musl-dev libpng-dev g++ lapack-dev && apk add --no-cache bash git openssh

# Git 
#######
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install wget

# FEAGI
#######
RUN mkdir -p /opt/source-code/feagi-core/
RUN git clone https://github.com/m-nadji-tehrani/feagi-core.git /opt/source-code/feagi-core
WORKDIR /opt/source-code/feagi-core/
RUN git checkout dev

# MNIST
#######
RUN wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz -P /opt/source-code/feagi-core/raw/MNIST/ -q
RUN wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz -P /opt/source-code/feagi-core/raw/MNIST/ -q
RUN wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz -P /opt/source-code/feagi-core/raw/MNIST/ -q
RUN wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz -P /opt/source-code/feagi-core/raw/MNIST/ -q


RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/source-code/feagi-core/requirements.txt
WORKDIR /opt/source-code/feagi-core/cython_libs
RUN python3 ./cython_setup.py build_ext --inplace
RUN mkdir /opt/source-code/feagi-core/connectome
WORKDIR /opt/source-code/feagi-core/

RUN ls /opt/source-code/

CMD ["python3", "main-auto.py"]
