# docker build -t ubuntu1804py36
FROM ubuntu:18.04

RUN apt update && \
        apt install -y software-properties-common vim && \
        add-apt-repository ppa:jonathonf/python-3.6

ARG DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Add Bionic source
RUN echo "deb https://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse" > /etc/apt/sources.list
RUN echo "deb https://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse" >> /etc/apt/sources.list
RUN echo "deb https://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse" >> /etc/apt/sources.list
RUN echo "deb https://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse" >> /etc/apt/sources.list
RUN echo "deb https://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse" >> /etc/apt/sources.list

RUN apt update -y

RUN apt install -y cmake wget \
    build-essential python3.6 python3.6-dev python3-pip python3.6-venv \
    git \
    openni2-utils \
    #libvtk7-dev vtk7 libvtk7.1 \
    libpcl-dev

# fork module
#RUN git clone -b rc_patches4 https://github.com/Sirokujira/python-pcl.git
# main
#RUN git clone -b master https://github.com/strawlab/python-pcl.git
RUN git clone -b master https://github.com/mickeyouyou/python-pcl

WORKDIR /python-pcl

# update pip
RUN python3.6 -m pip install pip --upgrade && \
    python3.6 -m pip install wheel

RUN pip install -r requirements.txt && \
    python3.6 setup.py build_ext -i && \
    python3.6 setup.py install

