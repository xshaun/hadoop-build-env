#!/bin/bash
#
source 0.*

# ----------------------------
# Setup passphraseless ssh
#
# * ssh localhost without a passphrase
#   -- ssh localhost # check
if [[ ! -f ~/.ssh/id_rsa.pub ]]; then
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
fi
if [[ ! -f ~/.ssh/authorized_keys ]]; then
    touch ~/.ssh/authorized_keys
fi
grep "`cat ~/.ssh/id_rsa.pub`" ~/.ssh/authorized_keys
if [[ 0 != $? ]]; then
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
fi
chmod 700 ~/.ssh
chmod 644 ~/.ssh/authorized_keys

# * ssh configure
#    [pc-dev connects cluster nodes without a passphrase]
#
if [[ 'FULLY_DIS_MODE' == ${HADOOP_CLUSTER_MODE} ]]; then
    for item in ${HADOOP_FDM_NODES[list][@]}; do
        ssh_copy_id_auto ${HADOOP_FDM_NODES[pw]} ${item}
    done
fi

