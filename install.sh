#!/bin/bash

set -e

# Usage:
#   cmdlog <command>
#
cmdlog()
{
    mkdir -p ./tmp/
    stdout=./tmp/stdout.log
    stderr=./tmp/stderr.log
    progress=./tmp/progress.log

    if [[ -f ${progress} ]]; then
        # previous script file id
        pre=$(cat ${progress})

        # current script file id
        cur=$(echo ${1} | cut -d '.' -f 1,2)

        # skip executed script
        if [[ ${pre} > ${cur} ]]; then
            echo "$(date +%Y-%m-%d:%H:%M:%S) Skip : ${1}" | tee -a ${stdout} ${stderr}
            return 0
        fi
    fi

    echo ${1} | cut -d '.' -f 1,2 > ${progress}

    echo "$(date +%Y-%m-%d:%H:%M:%S) Executing : ${1}" | tee -a ${stdout} ${stderr}
    /bin/bash ./${1} 1>>${stdout} 2>>${stderr}
    echo "$(date +%Y-%m-%d:%H:%M:%S) Executed : ${1}" | tee -a ${stdout} ${stderr}

    # Successful Completion
    if [[ ${2} == 'final' ]]; then
        rm -f ${progress}
        echo "$(date +%Y-%m-%d:%H:%M:%S) SUCCESSFUL COMPLETION"
    fi
}

# Run:
#
if [[ ${1} == 'run' ]]; then

    cmdlog 0.0.user.manual.settings.sh
    cmdlog 1.0.pre.run.requisites.sh
    cmdlog 1.1.switch.ali.maven.sh
    cmdlog 1.2.settup.passphraseless.sh

    cmdlog 2.0.run.download.code.sh
    cmdlog 2.1.run.conf.requisites.sh
    cmdlog 2.2.run.auxconf.default.xml.sh
    cmdlog 2.3.run.auxconf.mapred.xml.sh 'final'

    exit 0
fi

# Src:
#
if [[ ${1} == 'src' ]]; then
    cmdlog 0.0.user.manual.settings.sh
    cmdlog 1.0.pre.src.requisites.sh
    cmdlog 1.1.switch.ali.maven.sh
    cmdlog 1.2.settup.passphraseless.sh

    cmdlog 3.0.src.download.code.sh
    cmdlog 3.1.src.compile.code.sh
    cmdlog 3.2.src.deploy.code.sh 'final'

    exit 0
fi

if [[ ${1} == 'all' ]]; then
    cmdlog 0.0.user.manual.settings.sh
    cmdlog 1.0.pre.src.requisites.sh
    cmdlog 1.1.switch.ali.maven.sh
    cmdlog 1.2.settup.passphraseless.sh

    cmdlog 2.0.run.download.code.sh
    cmdlog 2.1.run.conf.requisites.sh
    cmdlog 2.2.run.auxconf.default.xml.sh
    cmdlog 2.3.run.auxconf.mapred.xml.sh

    cmdlog 3.0.src.download.code.sh
    cmdlog 3.1.src.compile.code.sh
    cmdlog 3.2.src.deploy.code.sh 'final'

    exit 0
fi

echo 'Usage: [ install.sh src ] | [ install.sh run ] | [ install.sh all] '

