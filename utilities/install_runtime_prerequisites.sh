#!/bin/bash
#
# Recommend trusty (14.04LTS)

killall dpkg
killall apt-get
killall aptitude
dpkg --configure -a

# APT='apt-get'

# ----------------------------
# Installing required packages
#
# * Basic
apt-get -y install ssh pdsh curl expect libxml2-utils

# FOR UBUNTU
cat /etc/*release | grep ID=ubuntu
if [[ $? == 0 ]]; then
	# * Oracle JDK 1.8 (preferred)
	apt-get -y purge openjdk*
	add-apt-repository -y ppa:webupd8team/java
	apt-get -y update
	echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
	apt-get -y install oracle-java8-installer --allow-unauthenticated
	apt-get -y install oracle-java8-set-default --allow-unauthenticated
	apt-get -y install software-properties-common

	# * Open JDK 1.8
	if [[ '' == `which java` ]]; then 
	    apt-get -y install openjdk-8-jdk; 
	fi
fi

# FOR DEBIAN
cat /etc/*release | grep ID=debian
if [[ $? == 0 ]]; then
	apt-get -f install apt-transport-https
	echo deb http://http.debian.net/debian jessie-backports main >> /etc/apt/sources.list
	apt-get update
	apt-get -f install openjdk-8-jdk
	# update-alternatives --config java
fi

# ----------------------------
# Clean and Upgrade libs:
# apt-get -y upgrade
# apt-get -y autoremove
# apt-get -y autoclean
