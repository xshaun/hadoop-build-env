# * Oracle JDK 1.8 (preferred)
apt-get -y purge openjdk*
apt-get -y install software-properties-common
add-apt-repository ppa:webupd8team/java
apt-get -y update
apt-get -y install oracle-java8-installer

# Installing Software
apt-get install ssh
apt-get install pdsh
# ----------------------------------------
# fix bugs: 
#   pdsh set rsh to connect default, reset ssh and reconnect terminal
#   -- vim ~/.profile
#   -- pdsh -w localhost -l root uptime # test
#----------------------
export PDSH_RCMD_TYPE=ssh
#----------------------

# Download a recent stable release from one of the Apache Download Mirrors
curl -sSL http://www-eu.apache.org/dist/hadoop/common/hadoop-3.0.0-alpha2/hadoop-3.0.0-alpha2.tar.gz | tar -xzv

# Edit the file vim etc/hadoop/hadoop-env.sh to define some parameters as follows:
#
# set to the root of your Java installation
export JAVA_HOME=/usr/lib/jvm/java-8-oracle

# this will display the usage documentation for the hadoop script.
bin/hadoop

# Pseudo-Distributed Operation
# ---------------------------------
# vim etc/hadoop/core-site.xml
# 
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
# ---------------------------------
# vim etc/hadoop/hdfs-site.xml
# 
cd ~
mkdir -p mydata/hdfs/namenode
mkdir -p mydata/hdfs/datanode

<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:/root/mydata/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:/root/mydata/hdfs/datanode</value>
    </property>
</configuration>

# Setup passphraseless ssh
# Now check that you can ssh to the localhost without a passphrase:
ssh localhost
# ---------------------------------
# If you cannot ssh to localhost without a passphrase, execute the following commands:
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys

# YARN on a Single Node
# 
# Format the filesystem:
bin/hdfs namenode -format
#
# Start NameNode daemon and DataNode daemon:
# 
# ----------------------------------------
# fix bugs: 
#   add below lines to [start|stop]-dfs.sh
#    -- vim sbin/start-dfs.sh
#    -- vim sbin/stop-dfs.sh
#----------------------
HDFS_DATANODE_USER=root
HADOOP_SECURE_DN_USER=hdfs
HDFS_NAMENODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root
#-----------------------
# ----------------------------------------
# 
# The hadoop daemon log output is written to the $HADOOP_LOG_DIR directory (defaults to $HADOOP_HOME/logs).
sbin/start-dfs.sh
# 
# Browse the web interface for the NameNode; by default it is available at:
NameNode - http://localhost:9870/
#
# # Make the HDFS directories required to execute MapReduce jobs:
# bin/hdfs dfs -mkdir /user
# bin/hdfs dfs -mkdir /user/root

# Configure parameters as follows:
# 
# ----------------------------------------
# cp etc/hadoop/mapred-site.xml.template etc/hadoop/mapred-site.xml 
# vim etc/hadoop/mapred-site.xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
# ----------------------------------------
# vim etc/hadoop/yarn-site.xml
#
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
    </property>
</configuration>

# Start ResourceManager daemon and NodeManager daemon:
# 
# ----------------------------------------
# fix bugs: 
#   add below lines to [start|stop]-dfs.sh
#    -- vim sbin/start-yarn.sh
#    -- vim sbin/stop-yarn.sh
#----------------------
YARN_NODEMANAGER_USER=root
YARN_RESOURCEMANAGER_USER=root
#-----------------------
# ----------------------------------------

# Start ResourceManager daemon and NodeManager daemon:
sbin/start-yarn.sh

# Browse the web interface for the ResourceManager; by default it is available at:
ResourceManager - http://localhost:8088/

# Run a MapReduce job.
./bin/hadoop jar ./share/hadoop/mapreduce/hadoop-mapreduce-examples-3.0.0-alpha2.jar  pi 2 5

# When you’re done, stop the daemons with:
sbin/stop-yarn.sh
sbin/stop-dfs.sh

#-----------------------------------------------------------------------------------------------------------------------------------
# Enabling Opportunistic Containers
# 
# vim etc/hadoop/yarn-site.xml
    <property>
        <name>yarn.resourcemanager.opportunistic-container-allocation.enabled</name>
        <value>true</value>
    </property>
    <property>
        <name>yarn.nodemanager.opportunistic-containers-max-queue-length</name>
        <value>20</value>
    </property>

./bin/hadoop jar ./share/hadoop/mapreduce/hadoop-mapreduce-examples-3.0.0-alpha2.jar  pi -Dmapreduce.job.num-opportunistic-maps-percent="40" 50 100

# Distributed scheduling
# 
# vim etc/hadoop/yarn-site.xml
    <property>
        <name>yarn.nodemanager.distributed-scheduling.enabled</name>
        <value>true</value>
    </property>
    <property>
        <name>yarn.nodemanager.amrmproxy.enabled</name>
        <value>true</value>
    </property>

./bin/hadoop jar ./share/hadoop/mapreduce/hadoop-mapreduce-examples-3.0.0-alpha2.jar  pi -Dmapreduce.job.num-opportunistic-maps-percent="40" 50 100
