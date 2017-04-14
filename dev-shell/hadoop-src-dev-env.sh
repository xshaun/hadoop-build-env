#!/bin/bash

# --------------------------------------------------------------------------------
# Installing required packages for clean install of Ubuntu 14.04 LTS Desktop:

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

# Optional packages:

# * Snappy compression
apt-get -y install snappy libsnappy-dev
# * Bzip2
apt-get -y install bzip2 libbz2-dev
# * Jansson (C Library for JSON)
apt-get -y install libjansson-dev
# * Linux FUSE
apt-get -y install fuse libfuse-dev

# --------------------------------------------------------------------------------
# * Modidy maven mirrors in /etc/maven/settings.xml
# 
:<<COMMENT
<mirrors>
  <mirror>
    <id>alimaven</id>
    <name>aliyun maven</name>
    <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
    <mirrorOf>central</mirrorOf>
  </mirror>
  <!--
  <mirror>
    <id>CN</id>
    <name>OSChina Central</name>                               
    <url>http://maven.oschina.net/content/groups/public/</url>
    <mirrorOf>*</mirrorOf>
  </mirror>
  -->
</mirrors>
COMMENT
# 
# mirrorOf: 
# 1. *
# 2. repo3
# 3. repo1,repo2,*,!repo3
# 4. external:*
# 
mkdir -p ~/.m2
ln -s ./m2-settings.xml ~/.m2/settings.xml

# * curl
apt-get -y install curl

# * hadoop source code and dependencies
#curl -sSL http://www-eu.apache.org/dist/hadoop/common/hadoop-2.7.3/hadoop-2.7.3-src.tar.gz | tar -xzv
#curl -sSL http://www-eu.apache.org/dist/hadoop/common/hadoop-2.7.3/hadoop-2.7.3.tar.gz | tar -xzv
curl -sSL http://www-eu.apache.org/dist/hadoop/common/hadoop-3.0.0-alpha2/hadoop-3.0.0-alpha2-src.tar.gz | tar -xzv
#curl -sSL http://www-eu.apache.org/dist/hadoop/common/hadoop-3.0.0-alpha2/hadoop-3.0.0-alpha2.tar.gz | tar -xzv

#cd ./hadoop-2.7.3-src
#cd ./hadoop-2.7.3
cd ./hadoop-3.0.0-alpha2-src
#cd ./hadoop-3.0.0-alpha2

# Tips1： 网络下载超时，以下命令可能运行失败，可以嵌入循环中
# $? 2>/dev/null; while [[ $? -ne 0 ]]; do mvn clean; done
# $? 2>/dev/null; while [[ $? -ne 0 ]]; do mvn test; done
# $? 2>/dev/null; while [[ $? -ne 0 ]]; do mvn package; done
# $? 2>/dev/null; while [[ $? -ne 0 ]]; do mvn install -DskipTests; done
# $? 2>/dev/null; while [[ $? -ne 0 ]]; do mvn install; done
# $? 2>/dev/null; while [[ $? -ne 0 ]]; do mvn deploy; done
# 
# mvn dependency:list        查看当前项目的已解析依赖
# mvn dependency:tree        查看当前项目的依赖树
# mvn dependency:analyze     工具可以帮助分析当前项目的依赖
# 
# mvn compile                编译项目的主源代码
# mvn test-compile           编译项目的中测试代码
# mvn test                   使用单元测试框架运行测试，测试代码不会被打包或部署
# mvn package                接受编译好的代码，打包成可发布的格式
# mvn verify                 运行任何检查，验证包是否有效且达到质量标准。
# mvn install                将包安装到Maven本地仓库，供本地其他Maven项目使用
# mvn deploy                 将最终的包复制到远程仓库，供其他开发人员和Maven项目使用
# 
$? 2>/dev/null; while [[ $? -ne 0 ]]; do mvn clean install -DskipTests site ; done


