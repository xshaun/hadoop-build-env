#!/bin/bash

#para are group_name and user_name
if [ $# -ne 2 ]
then
    echo "wrong paras number"
    exit 1
fi

#create group if not exists  
egrep "^$1" /etc/group >& /dev/null  
if [ $? -ne 0 ]  
then  
    groupadd $group  
fi  
  
#create user if not exists  
egrep "^$2" /etc/passwd >& /dev/null  
if [ $? -ne 0 ]  
then  
	useradd $2
else
   	usermod -a -G $1 $2
fi  
