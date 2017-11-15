#!/bin/bash
#

#
# [function]
# ---------------------
# ssh_copy_id_auto()
#
# Description:
#   auto copy local '~/.ssh/id_rsa.pub' to destination node
#   thus can access it through ssh without password.
#
# Params:
#   user - remote node's username
#   ip - remote node's ip
#   pwd - remote node's password (here proclaimed in writing)
#
# Usage:
#   ssh_copy_id_auto ${user}@${ip} ${pwd}
#
ssh_copy_id_auto()
{
    expect -c "
    set timeout -1;
    spawn ssh-copy-id $1;
    expect {
        *(yes/no)* {send yes\r; exp_continue;}
        *password:* {send $2\r; exp_continue;}
        eof {exit 0;}
    }";
}

#
# [produce]
# ----------------------------
# Description:
#   generate local '~/.ssh/id_rsa.pub' and set its prority
#   and prepare for passphraseless setup.
#   also support to access localhost without password
#
# * ssh localhost without a passphrase
#   -- ssh localhost # checking
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

#
# [produce]
# ----------------------------
# Description:
#   configure remote nodes to accept local *.pub
#   for `ssh user@ip or pdsh` without password
#
# Params:
#   users - ${1}, a list of remote nodes and join with ','. sample as "u1@ip1,u2@ip2"
#   pwd - ${2}, remote nodes' password(s) that should been the same
#
# Usage:
#   ssh_copy_id_auto ${users} ${pwd}
#
OLD_IFS="$IFS"
IFS=","
nodes=(${1})
for node in ${nodes[@]}; do
    ssh_copy_id_auto ${node} ${2}
done
IFS="$OLD_IFS"

