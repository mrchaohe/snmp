# -*- coding:utf-8 -*-
import os
import time
from multiprocessing import Process
from threading import Timer
from collections import defaultdict

import gevent
from gevent import monkey; monkey.patch_all()

from snmp_gather import SelectSnmp
from mult_thread import MyThread
import Mysql_Db
import wrang_creat


def select(total):
    """调用SelectSnmp类，
       获取snmp数据，
       写入数据库
    """
    row = total[0]
    sn = total[1]
    community = row[1].split(';')[0]
    select_snmp = SelectSnmp(row[0], community)
    params = select_snmp.make_sql(sn)
    Mysql_Db.insert_portinfo(params)


def multi_thread(rows, sn):
    """
    :param row:
    :param sn:
    :return:
    """
    while 1:
        threads = []
        thread_num = 10
        for index in range(thread_num):
            try:
                row = rows.pop()
                thread = MyThread(select, (row, sn))
                threads.append(thread)
            except Exception as e:
                print(e, 'in get row')
                break
        try:
            for th in threads:
                th.start()
            for th in threads:
                th.join(timeout=150)

        except Exception as e:
            print e, 'in multithread'
        if not rows:
            break


def insert_portinfo(sn=[0]):
    """定时查询写入portinfo"""
    start_time = int(time.time())  # 定时执行时间戳
    try:
        sn[0] += 1  # sn 表示执行次数
        cur_time = time.localtime()
        if cur_time.tm_hour == 0 and cur_time.tm_min in range(5):
            sn[0] = 1

        rows = Mysql_Db.select_host()   # 需要查询的host

        # 构建进程列表, 将任务均分到各进程中
        process_num = 8
        row_groups = [[] for i in range(process_num)]
        for j in range(len(rows)):
            i = j % process_num
            row_groups[i].append(rows[j])
        
        # 创建多进程
        process = []
        for each_row in row_groups:
            each_process = Process(target=multi_thread, args=(each_row, sn[0]))
            process.append(each_process)

        for po in process:
            po.start()

        for po in process:
            po.join()

        # 同步更新到portlog和hostlog

        Mysql_Db.insert_portlog()
        Mysql_Db.insert_hostlog()
        wrang_creat.main()

    except Exception as e:
        print(e)

    # 每5分钟执行一次

    end_time = int(time.time())
    exec_time = 60*5-(end_time-start_time)
    t = Timer(exec_time, insert_portinfo)
    t.start()


def main():
    insert_portinfo()
    Mysql_Db.main()
    wrang_creat.main()

if __name__ == "__main__":
    main()


