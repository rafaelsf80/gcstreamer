# To build a new docker image, please run:
# docker build -t streaming-api:v1.0 -f env/Dockerfile .

FROM ubuntu:xenial

LABEL description="GCS Streaming build environment."

RUN apt-get update && apt-get upgrade -y

RUN apt-get update && apt-get install -y \
    apt-utils \
    autoconf \
    autoconf-archive \
    automake \
    binutils-dev \
    build-essential \
    clang \
    cmake \
    curl \
    g++ \
    gcc \
    git \
    google-perftools \
    libass-dev \
    libboost-all-dev \
    libdouble-conversion-dev \
    libevent-dev \
    libgflags-dev \
    libfreetype6-dev \
    libgoogle-glog-dev \
    libgtest-dev \
    libiberty-dev \
    libjemalloc-dev \
    liblz4-dev \
    liblzma-dev \
    libopenmpi-dev \
    libsdl2-dev \
    libsdl2-ttf-dev \
    libsdl2-2.0 \
    libsnappy-dev \
    libssl-dev \
    libtool \
    libva-dev \
    libvdpau-dev \
    libvorbis-dev \
    libxcb1-dev \
    libxcb-shm0-dev \
    libxcb-xfixes0-dev \
    make \
    pkg-config \
    python-dev \
    python-setuptools \
    software-properties-common \
    unzip \
    wget \
    vim \
    zip \
    zlib1g-dev \
    && apt-get clean

RUN easy_install pip

#RUN add-apt-repository ppa:jonathonf/ffmpeg-3 -y
RUN apt-get update && apt-get install -y \
    libav-tools \
    libavdevice-dev \
    libx264-dev \
    libx265-dev \
    libnuma-dev \
    libvpx-dev \
    libfdk-aac-dev \
    libmp3lame-dev \
    libopus-dev \
    ffmpeg \
    && apt-get clean

RUN apt-get install -y \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-doc \
    gstreamer1.0-tools \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    && apt-get clean

ENV CPLUS_INCLUDE_PATH=/usr
ENV LD_LIBRARY_PATH=/usr

#install Google Cloud Storage and IoT Core Python Libraries
RUN pip install --upgrade google-cloud-storage
RUN pip install --user jwt
RUN pip install --user PyJWT
RUN pip install --user paho-mqtt

#set up environment for Google Cloud Storage
ENV SRC_DIR /googlesrc
ENV BIN_DIR /google

#copy gcstreamer directory to Docker
RUN mkdir -p $SRC_DIR
COPY *.md *.py roots.pem rsa_private.pem LICENSE *.json $SRC_DIR/
COPY client $SRC_DIR/client
COPY env $SRC_DIR/env

#copy python files to BIN_DIR directory
RUN mkdir -p $BIN_DIR
RUN mkdir -p $BIN_DIR/python
RUN cp $SRC_DIR/client/*.py $BIN_DIR/python
RUN cp $SRC_DIR/rsa_private.pem $BIN_DIR
RUN cp $SRC_DIR/roots.pem $BIN_DIR
RUN cp $SRC_DIR/*.json $BIN_DIR
RUN chmod +x $BIN_DIR/python/*.py

#clean up the build artifacts and source directory.
RUN cd $SRC_DIR  

#set work directory
WORKDIR $BIN_DIR

CMD ["/bin/bash"]