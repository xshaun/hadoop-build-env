#!/bin/bash

set -e

# Add Maven Settings to {user home}/.m2/settings.xml
mkdir -p ~/.m2
cp ./1.1.switch.ali.maven.settings.xml ~/.m2/settings.xml

