# User defination
source ./utilities/functions.profile
export JAVA_OPTS="-Xms512m -Xmx4096m"
export JAVA_TOOL_OPTIONS="-Xms512m -Xmx2048m -XX:+UseConcMarkSweepGC -XX:-UseGCOverheadLimit"
export MAVEN_OPTS="-Xms512m -Xmx2048m"
export FINDBUGS_HOME=/opt/findbugs-3.0.1
export PDSH_RCMD_TYPE=ssh
