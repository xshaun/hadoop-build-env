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
grep "`cat ~/.ssh/id_rsa.pub`" ~/.ssh/authorized_keys > /dev/null
if [[ 0 != $? ]]; then
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
fi
chmod 700 ~/.ssh
chmod 644 ~/.ssh/authorized_keys

# * ssh from pc-dev to cluster without a passphrase
#
if [[ 'FULLY_DIS_MODE' == ${HADOOP_CLUSTER_MODE} ]]; then
    for item in ${HADOOP_FDM_NODES[list][@]}; do
        auto_ssh_copy_id ${HADOOP_FDM_NODES[pw]} ${item}
    done
fi


# -----------------------------
# Function:
#   auto_ssh_copy_id <password> <username>@<IP>
#
auto_ssh_copy_id() {
    expect -c "
    set timeout -1;
    spawn ssh-copy-id $2;
    expect {
        *(yes/no)* {send yes\r; exp_continue;}
        *password:* {send $1\r; exp_continue;}
        eof {exit 0;}
    }";
};
