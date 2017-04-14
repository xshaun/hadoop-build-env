#!/usr/bin/env python3
#-*-encoding:utf-8-*-
#

import os
from xml.dom import minidom, Node


HOME_PATH = r'/home/boy/'



m2_ali_mirror = \
    """
    <mirror>
        <id>alimaven</id>
        <name>aliyun maven</name>
        <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
        <mirrorOf>central</mirrorOf>
    </mirror>
    """

m2_filename = HOME_PATH + r'.m2/settings.xml'
if os.path.exists(m2_filename) :
    dom = minidom.parse(m2_filename)
    root = dom.documentElement
    eles = root.getElementsByTagName('mirrors')[0]
    print(eles.childNodes)
    print(eles.data)
else :
    m2_settings = \
 """
 <?xml version="1.0" encoding="UTF-8"?>
 <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0" 
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
           xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
   <mirrors>
 """ \
   + m2_ali_mirror + \
 """
   </mirrors>
 </settings>
 """
 
    print (m2_settings)


#update-alternatives --set java '/usr/lib/jvm/java-8-oracle/jre/bin/java'




