#!/bin/bash

set -e

# APT='apt-get'

# ----------------------------
# Installing required packages
#
# * Oracle JDK 1.8 (preferred)
apt-get -y purge openjdk*
add-apt-repository -y ppa:webupd8team/java
apt-get -y update
echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
apt-get -y install oracle-java8-installer --allow-unauthenticated
apt-get -y install oracle-java8-set-default --allow-unauthenticated
apt-get -y install software-properties-common
# * Basic
apt-get -y install ssh pdsh curl
# * Maven
apt-get -y install maven
# * Native libraries
apt-get -y install build-essential autoconf automake libtool cmake zlib1g-dev pkg-config libssl-dev
# * ProtocolBuffer 2.5.0 (required)
apt-get -y install libprotobuf-dev protobuf-compiler

# ----------------------------
# Optional packages:
#
# * Snappy compression
apt-get -y install snappy libsnappy-dev
# * Bzip2
apt-get -y install bzip2 libbz2-dev
# * Jansson (C Library for JSON)
apt-get -y install libjansson-dev
# * Linux FUSE
apt-get -y install fuse libfuse-dev
