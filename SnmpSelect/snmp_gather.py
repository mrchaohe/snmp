# -*- coding:utf-8 -*-
import time
import subprocess
from collections import defaultdict

import gevent
from gevent import monkey; monkey.patch_all()

MIB_LIST = {
    "port": "ifName",                   # 初始化使用
    "desc": "ifDescr",                  # 接口描述
    "speed": "ifSpeed",                 # 带宽
    "ibps": "ifInOctet",                # 收到字节
    "obps": "ifOutOctet",               # 发送字节
    "iUpps": "ifInUcastPkts",           # 收包数
    "oUpps": "ifOutUcastPkts",          # 发包数
    "iMpps": "ifHCInMulticastPkts",
    "oMpps": "ifHCoutMulticastPkts",
    "discards": "ifInDiscards",
    "odiscards": "ifOutDiscards",       # 发包丢包数
    "epps": "ifInErrors",               # 收包错误数
    "oepps": "ifOutErrors",             # 发包错误数
    # "state": "ifOperStatus",          # 接口状态
}


class SelectSnmp(object):
    """查询snmp信息,导入portinfo表"""
    def __init__(self, host, community, version=2):
        self.ip = host
        self.community = community
        self.version = version
        self.portinfo = defaultdict(dict)
        self.task = []

    def search_port(self, mib, timeout=150):
        """查询端口数据"""
        cmd = 'snmpwalk -v%sc -c %s %s %s' % (self.version, self.community, self.ip, mib)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        begin_time = time.time()

        while True:
            if proc.poll() is not None:
                break
            deadtime = time.time() - begin_time
            if deadtime > timeout:
                proc.terminate()
                print('cmd, timeout')
                break
            time.sleep(0.1)
        return proc.stdout.readlines()

    def parse_line(self, row):
        """数据处理"""
        before, after = row.split('=')
        if before:
            port_id = before.split('.')[-1].strip()
        if after:
            value = after.split(':')[-1].split('.')[0].strip()
        return port_id, value

    def search_state(self):
        """state"""
        try:
            res = self.search_port('ifOperStatus')
            if res:
                for row in res:
                    port_id, ori_value = self.parse_line(row)

                    value = ori_value[-2]  # 获取端口状态码
                    self.portinfo[port_id]['state'] = value
        except Exception as e:
            print(e, 'in state')

    def search_mib(self, total):
        """获取MID, 构建portinfo"""
        try:
            key = total[0]
            mid = total[1]
            rows = self.search_port(mid)
            if rows:
                for row in rows:
                    port_id, value = self.parse_line(row)
                    self.portinfo[port_id][key] = value
        except Exception as e:
            print(e, 'in search_mib')

    def gevent_row(self):
        """调用协程采集"""
        tasks = []
        for key, mid in MIB_LIST.items():
            tasks.append(gevent.spawn(self.search_mib, (key, mid)))
        tasks.append(gevent.spawn(self.search_state))
        gevent.joinall(tasks)

    def make_sql(self, sn):
        """构建sql_params"""
        self.gevent_row()   # 调用协程

        start_time = time.localtime()
        str_start_time = time.strftime('%Y-%m-%d %H:%M:%S', start_time)
        sql_params = []

        for port_id in self.portinfo.keys():
            try:
                values = [self.ip, self.portinfo[port_id]['port'],
                          self.portinfo[port_id]['desc'], self.portinfo[port_id]['speed'], self.portinfo[port_id]['state'],
                          self.portinfo[port_id]['ibps'],self.portinfo[port_id]['obps'], self.portinfo[port_id]['iUpps'],
                          self.portinfo[port_id]['oUpps'], self.portinfo[port_id]['iMpps'], self.portinfo[port_id]['oMpps'],
                          self.portinfo[port_id]['discards'], self.portinfo[port_id]['odiscards'], self.portinfo[port_id]['epps'],
                          self.portinfo[port_id]['oepps'], str_start_time, sn]
                sql_params.append(values)
            except Exception as e:
                print(e, 'in make_sql')
        return sql_params



