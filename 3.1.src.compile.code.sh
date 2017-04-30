#!/bin/bash
#
source 0.*

# ----------------------------------------------------------------------------------
# Maven main modules:
#
#   hadoop                            (Main Hadoop project)
#          - hadoop-project           (Parent POM for all Hadoop Maven modules.             )
#                                     (All plugins & dependencies versions are defined here.)
#          - hadoop-project-dist      (Parent POM for modules that generate distributions.)
#          - hadoop-annotations       (Generates the Hadoop doclet used to generated the Javadocs)
#          - hadoop-assemblies        (Maven assemblies used by the different modules)
#          - hadoop-common-project    (Hadoop Common)
#          - hadoop-hdfs-project      (Hadoop HDFS)
#          - hadoop-mapreduce-project (Hadoop MapReduce)
#          - hadoop-tools             (Hadoop tools like Streaming, Distcp, etc.)
#          - hadoop-dist              (Hadoop distribution assembler)
#
# ----------------------------------------------------------------------------------
# Where to run Maven from?
#
#   It can be run from any module. The only catch is that if not run from utrunk
#   all modules that are not part of the build run must be installed in the local
#   Maven cache or available in a Maven repository.
#
# ----------------------------------------------------------------------------------
# Maven build goals:
#
#  * Clean                     : mvn clean [-Preleasedocs]
#  * Compile                   : mvn compile [-Pnative]
#  * Run tests                 : mvn test [-Pnative] [-Pshelltest]
#  * Create JAR                : mvn package
#  * Run findbugs              : mvn compile findbugs:findbugs
#  * Run checkstyle            : mvn compile checkstyle:checkstyle
#  * Install JAR in M2 cache   : mvn install
#  * Deploy JAR to Maven repo  : mvn deploy
#  * Run clover                : mvn test -Pclover [-DcloverLicenseLocation=${user.name}/.clover.license]
#  * Run Rat                   : mvn apache-rat:check
#  * Build javadocs            : mvn javadoc:javadoc
#  * Build distribution        : mvn package [-Pdist][-Pdocs][-Psrc][-Pnative][-Dtar][-Preleasedocs][-Pyarn-ui]
#  * Change Hadoop version     : mvn versions:set -DnewVersion=NEWVERSION
#



# ----------------------------------------------------------------------------------
# Importing projects to eclipse/idea
#
# When you import the project to eclipse/idea, install hadoop-maven-plugins at first.
#
cd ${HADOOP_SRC_CODE_PATH}/hadoop-maven-plugins/ && mvn install
#
# Then, generate eclipse/idea project files.
#
#cd ${HADOOP_SRC_CODE_PATH}/ && mvn eclipse:eclipse -DskipTests
cd ${HADOOP_SRC_CODE_PATH}/ && mvn idea:idea -DskipTests
#
# At last, import to eclipse/idea by specifying the root directory of the project via
# [File] > [Import] > [Existing Projects into Workspace].
#
# ----------------------------------------------------------------------------------
# Building distributions:
#
cd ${HADOOP_SRC_CODE_PATH}
mvn dependency-check:aggregate
#
# Create binary distribution without native code and without documentation:
#
#   $ mvn package -Pdist -DskipTests -Dtar -Dmaven.javadoc.skip=true
#
# Create binary distribution with native code and with documentation:
#
#   $ mvn package -Pdist,native,docs -DskipTests -Dtar
#
# Create source distribution:
#
#   $ mvn package -Psrc -DskipTests
#
# Create source and binary distributions with native code and documentation:
#
#   $ mvn package -Pdist,native,docs,src -DskipTests -Dtar
#
# Create a local staging version of the website (in /tmp/hadoop-site)
#
#   $ mvn clean site -Preleasedocs; mvn site:stage -DstagingDirectory=/tmp/hadoop-site
#
mvn package -Pdist,native,docs,src -DskipTests -Dtar
#
# ----------------------------------------------------------------------------------
# Tests options:
#
# Use -DskipTests to skip tests when running the following Maven goals:
# 'package',  'install', 'deploy' or 'verify'
#
# * -Dtest=<TESTCLASSNAME>,<TESTCLASSNAME#METHODNAME>,....
# * -Dtest.exclude=<TESTCLASSNAME>
# * -Dtest.exclude.pattern=**/<TESTCLASSNAME1>.java,**/<TESTCLASSNAME2>.java
#
# To run all native unit tests
#
#   $ mvn test -Pnative -Dtest=allNative
#
# To run a specific native unit test
#
#   $ mvn test -Pnative -Dtest=<test>
#
# For example, to run test_bulk_crc32, you would use
#
#   $ mvn test -Pnative -Dtest=test_bulk_crc32
#
