#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command
import os


class Custom(Basis):

    def action(self):
        logger.info('--> common.configure_ganglia_monitor <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=5'

        host_list = self.getHosts()
        gmetad_list = self.getHosts(roles=['gmetad',])

        instructions = list()

        for host in host_list:
            ins = "ssh {0} {2}@{1} -tt 'sudo -S apt-get install ganglia-monitor ganglia-modules-linux ganglia-monitor-python'".format(
                ssh_option, host['ip'], host['usr'])
            instructions.append((ins, host['pwd']))

        for host in gmetad_list:
            ins = "ssh {0} {2}@{1} -tt 'sudo -S apt-get install gmetad ganglia-webfrontend rrdtool'".format(
                ssh_option, host['ip'], host['usr'])
            instructions.append((ins, host['pwd']))

        ret = Command.parallel(instructions)
        if not ret:
            return ret

        """
        服务器端

        修改/etc/ganglia/gmond.conf中
            cluster.name
            udp_send_channel 中的IP和端口
            udp_recv_channel 中的端口（用于接收其他gmond的数据）
            tcp_accept_channel 中的端口 （用于gmetad获取数据）

        在/etc/ganglia/gmetad.conf中增加
            data_source “?cluster.name?” ?ip?:8649 （此端口对应 tcp_accept_channel）

        sudo /etc/init.d/ganglia-monitor restart
        sudo /etc/init.d/gmetad restart

        sudo ln -s /usr/share/ganglia-webfrontend/ /var/www/html/ganglia
        sudo /etc/init.d/apache2 start

        sudo chown -R nobody /storage1/ganglia/
        sudo chown -R ganglia /storage1/ganglia/
        sudo chmod -R 777 /storage1/ganglia/

        客户端
        修改/etc/ganglia/gmond.conf中
            send_metadata_interval = 15
            cluster.name
            udp_send_channel 中的IP和端口 （此端口对应远程机的udp_recv_channel）

        sudo /etc/init.d/ganglia-monitor restart


        测试加压：`for j in {1..100}; do for i in {1..10000000}; do echo i>/dev/null; done; done;`&
        """

def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
