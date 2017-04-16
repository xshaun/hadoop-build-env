
#!/bin/bash

# APT='apt-get'

# ----------------------------
# Installing required packages

# * Oracle JDK 1.8 (preferred)
apt-get -y purge openjdk*
apt-get -y install software-properties-common
add-apt-repository ppa:webupd8team/java
apt-get -y update
apt-get -y install oracle-java8-installer
# * Maven
apt-get -y install maven
# * Native libraries
apt-get -y install build-essential autoconf automake libtool cmake zlib1g-dev pkg-config libssl-dev
# * ProtocolBuffer 2.5.0 (required)
apt-get -y install libprotobuf-dev protobuf-compiler

# ----------------------------
# Optional packages:

# * Snappy compression
apt-get -y install snappy libsnappy-dev
# * Bzip2
apt-get -y install bzip2 libbz2-dev
# * Jansson (C Library for JSON)
apt-get -y install libjansson-dev
# * Linux FUSE
apt-get -y install fuse libfuse-dev
