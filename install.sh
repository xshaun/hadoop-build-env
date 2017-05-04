#!/bin/bash

set -e

if [[ ${1} == 'src' ]]; then
    ./0.0.user.manual.settings.sh
    ./1.0.pre.src.requisites.sh
    ./1.1.switch.ali.maven.sh
    ./1.2.settup.passphraseless.sh

    ./3.0.src.download.code.sh
    ./3.1.src.compile.code.sh
    ./3.2.src.deploy.code.sh

    exit 0
fi

if [[ ${1} == 'run' ]]; then
    ./0.0.user.manual.settings.sh
    ./1.0.pre.run.requisites.sh
    ./1.1.switch.ali.maven.sh
    ./1.2.settup.passphraseless.sh

    ./2.0.run.download.code.sh
    ./2.1.run.conf.requisites.sh
    ./2.2.run.auxconf.default.xml.sh
    ./2.3.run.auxconf.mapred.xml.sh

    exit 0
fi

echo 'Usage: [ install.sh src ] | [ install.sh run ] '
