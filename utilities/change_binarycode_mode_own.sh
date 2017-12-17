#!/bin/bash

#paras are group, user, codepath
if [ $# -ne 3 ]
then 
    exit 1
fi

chown $2:$1 -R $3
chown root:$1 $3/etc
chown root:$1 $3/etc/hadoop
chown root:$1 $3/etc/hadoop/container-executor.cfg
#chown root:$1 $3
#chown root:$1 '$PWD/..'
chown root:$1 $3/bin/container-executor
chmod 6150 $3/bin/container-executor
