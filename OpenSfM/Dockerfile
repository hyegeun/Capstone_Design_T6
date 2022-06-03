FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

# Install apt-getable dependencies
RUN apt-get update \
    && apt-get install -y \
        zip unzip \
        build-essential \
        cmake \
        git \
        libeigen3-dev \
        libgoogle-glog-dev \
        libopencv-dev \
        libsuitesparse-dev \
        python3-dev \
        python3-numpy \
        python3-opencv \
        python3-pip \
        python3-pyproj \
        python3-scipy \
        python3-yaml \
        curl \
    && apt-get clean \
    && pip install pandas \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# Install Ceres 2
RUN \
    mkdir -p /var/lib/docker/volumes/harbor/_data/OpenSfM && cd /var/lib/docker/volumes/harbor/_data/OpenSfM && \
    curl -L http://ceres-solver.org/ceres-solver-2.0.0.tar.gz | tar xz && \
    cd /var/lib/docker/volumes/harbor/_data/OpenSfM/ceres-solver-2.0.0 && \
    mkdir -p build && cd build && \
    cmake .. -DCMAKE_C_FLAGS=-fPIC -DCMAKE_CXX_FLAGS=-fPIC -DBUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF && \
    make -j4 install && \
    cd / && rm -rf /usr/src/Harbor/OpenSfM/ceres-solver-2.0.0


COPY ./ /var/lib/docker/volumes/harbor/_data/OpenSfM

WORKDIR /var/lib/docker/volumes/harbor/_data/OpenSfM

RUN pip3 install -r requirements.txt && \
    python3 setup.py build && \
    ./viewer/node_modules.sh
