#!/bin/bash
#
source 0.*

# Recommend trusty (14.04LTS)

set -e

# APT='apt-get'

# ----------------------------
# Installing required packages
#
# * Basic
apt-get -y install ssh pdsh curl expect
# * Oracle JDK 1.8 (preferred)
apt-get -y purge openjdk*
add-apt-repository -y ppa:webupd8team/java
apt-get -y update
echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
apt-get -y install oracle-java8-installer --allow-unauthenticated
apt-get -y install oracle-java8-set-default --allow-unauthenticated
apt-get -y install software-properties-common
# * Maven
apt-get -y install maven
# * Native libraries
apt-get -y install build-essential autoconf automake libtool cmake zlib1g-dev pkg-config libssl-dev
# * ProtocolBuffer 2.5.0 (required)
if [[ ! `apt-get -y install libprotobuf-dev=2.5.0-9ubuntu1 protobuf-compiler=2.5.0-9ubuntu1` ]]; then
    curl -sSL 'https://github.com/google/protobuf/releases/download/v2.5.0/protobuf-2.5.0.tar.gz' | tar -C ~ -xzv

    cd ~/protobuf-2.5.0
    ./autogen.sh  &&  ./configure --prefix=/usr

    make  &&  make install
    # protoc --version

    cd ~/protobuf-2.5.0/java
    mvn install
fi

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
# * ZStandard compression
apt-get -y install zstd
# * Findbugs (if running findbugs)
curl -sSL 'https://jaist.dl.sourceforge.net/project/findbugs/findbugs/3.0.1/findbugs-noUpdateChecks-3.0.1.tar.gz' | tar -C '/opt' -xzv
export FINDBUGS_HOME=/opt/findbugs-3.0.1

# ----------------------------
# Fix issues / Reset
#
# * pdsh set rsh to connect default,
#       reset ssh and reconnect terminal
#   -- echo 'export PDSH_RCMD_TYPE=ssh' >>  ~/.profile # add
#   -- pdsh -w localhost -l root uptime # test
FILE=~/.profile
if [[ ! `grep 'export PDSH_RCMD_TYPE=' ${FILE} > /dev/null` ]]; then
    sed -i 's#.*export PDSH_RCMD_TYPE=.*#export PDSH_RCMD_TYPE=ssh#g' ${FILE}
else
    echo 'export PDSH_RCMD_TYPE=ssh' >> ${FILE}
fi
#
# * set findbugs home
FILE=~/.profile
if [[ ! `grep 'export FINDBUGS_HOME=' ${FILE} > /dev/null` ]]; then
    sed -i 's#.*export FINDBUGS_HOME=.*#export FINDBUGS_HOME=/opt/findbugs-3.0.1#g' ${FILE}
else
    echo 'export FINDBUGS_HOME=/opt/findbugs-3.0.1' >> ${FILE}
fi


# ----------------------------
# Clean and Upgrade libs:
apt-get -y upgrade
apt-get -y autoremove
apt-get -y autoclean

