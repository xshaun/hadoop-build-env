#!/bin/bash
#
source 0.*

# ----------------------------
# Download $HADOOP_VERSION from one of the Apache Download Mirrors
#
# * binary
HADOOP_CODE_LOCATION
curl -sSL 'http://www-eu.apache.org/dist/hadoop/common/hadoop-'$HADOOP_VERSION'/hadoop-'$HADOOPVERSION'.tar.gz' | tar -C $HADOOP_CODE_LOCATION -xzv
