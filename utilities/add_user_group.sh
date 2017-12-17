#!/bin/bash

#para are group_name and user_name
if [ $# -ne 3 ]
then
    echo "wrong paras num"
    exit 1
fi

is_group_exist=`cat /etc/group | grep -w $1 | awk -F ':' '{print $1}'`
if [ $1 -ne is_group_exist ]
then
   groupadd $1
fi

is_user_exist=`id $2`
if [ $is_user_exist -ne 0 ]
   useradd $2
else
   usermod -a -G $1 $2
