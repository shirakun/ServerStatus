# -*- coding: utf-8 -*-
# Update by: https://github.com/CokeMine/ServerStatus-Hotaru
# 依赖于psutil跨平台库：
# 支持Python版本：2.6 to 3.7
# 支持操作系统： Linux, Windows, OSX, Sun Solaris, FreeBSD, OpenBSD and NetBSD, both 32-bit and 64-bit architectures

import socket
import time
import string
import math
import os
import json
import collections
import psutil
import requests

SERVER = "http://status.localhost.lan/api.php"
USER = "user"
PASSWORD = "passwd"
INTERVAL = 1  # 更新间隔，单位：秒
UA = "ServerStatus"


def get_uptime():
    return int(time.time() - psutil.boot_time())


def get_memory():
    Mem = psutil.virtual_memory()
    try:
        MemUsed = Mem.total - (Mem.cached + Mem.free)
    except:
        MemUsed = Mem.total - Mem.free
    return int(Mem.total / 1024.0), int(MemUsed / 1024.0)


def get_swap():
    Mem = psutil.swap_memory()
    return int(Mem.total / 1024.0), int(Mem.used / 1024.0)


def get_hdd():
    valid_fs = ["ext4", "ext3", "ext2", "reiserfs", "jfs", "btrfs", "fuseblk", "zfs", "simfs", "ntfs", "fat32", "exfat",
                "xfs"]
    disks = dict()
    size = 0
    used = 0
    for disk in psutil.disk_partitions():
        if not disk.device in disks and disk.fstype.lower() in valid_fs:
            disks[disk.device] = disk.mountpoint
    for disk in disks.values():
        usage = psutil.disk_usage(disk)
        size += usage.total
        used += usage.used
    return int(size / 1024.0 / 1024.0), int(used / 1024.0 / 1024.0)


def get_load():
    try:
        return round(os.getloadavg()[0] * 2) / 2
    except:
        return -1.0


def get_cpu():
    return psutil.cpu_percent(interval=INTERVAL)


class Traffic:
    def __init__(self):
        self.rx = collections.deque(maxlen=10)
        self.tx = collections.deque(maxlen=10)

    def get(self):
        avgrx = 0
        avgtx = 0
        for name, stats in psutil.net_io_counters(pernic=True).items():
            if name == "lo" or name.find("tun") > -1:
                continue
            avgrx += stats.bytes_recv
            avgtx += stats.bytes_sent

        self.rx.append(avgrx)
        self.tx.append(avgtx)
        avgrx = 0
        avgtx = 0

        l = len(self.rx)
        for x in range(l - 1):
            avgrx += self.rx[x + 1] - self.rx[x]
            avgtx += self.tx[x + 1] - self.tx[x]

        avgrx = int(avgrx / l / INTERVAL)
        avgtx = int(avgtx / l / INTERVAL)

        return avgrx, avgtx


def liuliang():
    NET_IN = 0
    NET_OUT = 0
    net = psutil.net_io_counters(pernic=True)
    for k, v in net.items():
        if 'lo' in k or 'tun' in k:
            continue
        else:
            NET_IN += v[1]
            NET_OUT += v[0]
    return NET_IN, NET_OUT


def get_network(ip_version):
    if (ip_version == 4):
        HOST = "ipv4.google.com"
    elif (ip_version == 6):
        HOST = "ipv6.google.com"
    else:
        return False
    try:
        s = socket.create_connection((HOST, 80), 2).close()
        return True
    except:
        pass
    return False


def start_mon():
    traffic = Traffic()
    while True:
        CPU = get_cpu()
        NetRx, NetTx = traffic.get()
        NET_IN, NET_OUT = liuliang()
        Uptime = get_uptime()
        Load = get_load()
        MemoryTotal, MemoryUsed = get_memory()
        SwapTotal, SwapUsed = get_swap()
        HDDTotal, HDDUsed = get_hdd()
        array = {}

        array['uptime'] = Uptime
        array['load'] = Load
        array['memory_total'] = MemoryTotal
        array['memory_used'] = MemoryUsed
        array['swap_total'] = SwapTotal
        array['swap_used'] = SwapUsed
        array['hdd_total'] = HDDTotal
        array['hdd_used'] = HDDUsed
        array['cpu'] = CPU
        array['network_rx'] = NetRx
        array['network_tx'] = NetTx
        array['network_in'] = NET_IN
        array['network_out'] = NET_OUT
        array['user'] = USER
        array['passwd'] = PASSWORD
        array['online4'] = get_network(4)
        array['online6'] = get_network(6)
        print("update " + json.dumps(array) + '\n')

        try:
            headers = {'user-agent': UA}
            r = requests.post(SERVER,data=array,headers=headers)
            print(r.text)
            time.sleep(5)
        except Exception as e:
            print(e)
            time.sleep(5)
            start_mon()

if __name__ == '__main__':
    start_mon()