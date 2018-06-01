# -*- coding=utf-8 -*-

import MySQLdb
import time
from datetime import datetime
from mult_thread import MyThread
from copy import deepcopy


class Mydb(object):
    """数据库操作：select，insert/update"""
    def __init__(self, host, user, passwd, db, port=3306, charset='utf8'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.charset = charset

    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, port=self.port, db=self.db, user=self.user,
                                    passwd=self.passwd, charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def select(self, sql, params=()):
        rows = []
        try:
            self.connect()
            self.cursor.execute(sql, params)
            rows = list(self.cursor.fetchall())
        except Exception as e:
            print (e, 'in select sql', sql)
        finally:
            self.close()
            return rows

    def insert_many(self, sql, params=()):
        try:
            self.connect()
            self.cursor.executemany(sql, params)
            self.conn.commit()
        except Exception as e:
            print(e, 'in insert sql', sql)
            self.conn.rollback()
        finally:
            self.close()

    def insert_one(self, sql):
        try:
            self.connect()
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e, 'in insert sql', sql)
            self.conn.rollback()
        finally:
            self.close()


def sel_is_connect():
    """查询是否可达 ,state设为1"""
    # cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    sel_sql = '''select ip from ipinfo where is_connect=0'''
    rows = mydb.select(sel_sql)
    params = []
    for row in rows:
        param = [row[0], '0', 1, 2]
        params.append(param)
    # ins_sql = '''insert into ALARM_T(ip, port, `type`, alarm_level, checktime) values('%s',%s,  %s, %s, '%s')'''
    # mydb.insert_one(ins_sql, params)
    return params


def sel_cpu():
    """检查cpu告警， state设为2"""
    # cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    sel_sql = '''select i.ip, (100-free_cpu), a.LL, a.L,a.H, a.HH, a.level from ipinfo i, ALARM_Value a 
                 where i.ip=a.ip and i.free_cpu<> 0 and a.ziduan='cpu' '''
    rows = mydb.select(sel_sql)

    # 判断cpu利用率是否告警
    params = []
    for row in rows:
        if row[5] and row[1] > row[5]:
            alarm_statu = [row[0], '0', 2, 1]
            params.append(alarm_statu)
        elif row[4] and row[1] > row[4]:
            alarm_statu = [row[0], '0', 2, 2]
            params.append(alarm_statu)

    return params
    """
    if alarm_info:
        sql = '''insert into ALARM_T(ip,port, `type`, alarm_level, check_time) values(%s, %s,%s, %s,%s)'''
        mydb.insert_many(sql, alarm_info)
    """


def sel_ram():
    """查询内存告警，state设为3"""
    # cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    sel_sql = '''select i.ip, round((1-free_ram/total_ram),3)*100, a.LL, a.L,a.H, a.HH, a.LEVEL from ipinfo i, ALARM_Value a 
             where i.ip=a.ip and i.total_ram <> 0 and a.ziduan='arm' '''
    rows = mydb.select(sel_sql)

    # 判断ram利用率是否告警
    params = []
    for row in rows:
        if row[5] and row[1] > row[5]:
            alarm_statu = [row[0], '0', 3, 1]
            params.append(alarm_statu)
        elif row[4] and row[1] > row[4]:
            alarm_statu = [row[0],'0',  3, 2]
            params.append(alarm_statu)
    return params
    """
    if params:
        sql = '''insert into ALARM_T(ip, `type`, alarm_level, check_time) values(%s, %s,%s, %s,%s)'''
        mydb.insert_many(sql, params)
    """


def sel_port():
    """查询端口报警， state设为4"""
    # cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    sel_sql = '''select ip,port from portinfo where state=2 '''
    rows = mydb.select(sel_sql)

    params = []
    if rows:
        for row in rows:
            alarm_statu = [row[0], row[1], 4, 2]
            params.append(alarm_statu)
    return params
    """
    if params:
        sel = '''insert into ALARM_T(ip, `port`, `type`, alarm_level, check_time) values(%s,%s,%s,%s,%s)'''
        mydb.insert_many(sel, params)
    """


def sel_speed():
    """带宽占用告警， state设为5"""
    # cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    sel_sql = '''select p.ip, p.port, round((p.ibps/(p.speed*1000000))*100, 4), a.LL, a.L,a.H, a.HH, a.level from portinfo p, ALARM_Value a 
                     where p.ip=a.ip and p.port=a.port and p.speed <> 0 and a.ziduan='speed' '''
    rows = mydb.select(sel_sql)

    params = []
    for row in rows:
        if row[6] and row[2] > row[6]:
            alarm_statu = [row[0], row[1], 5, 1]
            params.append(alarm_statu)
        elif row[5] and row[2] > row[5]:
            alarm_statu = [row[0], row[1], 5, 2]
            params.append(alarm_statu)

    return params
    """
    if params:
        sql = '''insert into ALARM_T(ip, port,`type`, alarm_level, check_time) values(%s, %s,%s, %s,%s)'''
        mydb.insert_many(sql, params)
    """


def sel_epps():
    """错包告警, state=6"""
    # cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    sel_sql = '''select p.ip, p.port, round((p.epps/p.iUpps*100),2), round((p.oepps/p.iUpps*100),2), a.LL, a.L,a.H, a.HH, a.level 
                 from portinfo p, ALARM_Value a where p.ip=a.ip and p.port=a.port and p.iUpps<>0 and (a.ziduan='epps' or a.ziduan='oepps') '''
    rows = mydb.select(sel_sql)

    # 判断错包率是否告警
    params = []
    for row in rows:
        if row[7] and (row[2] > row[7] or row[3] > row[7]):
            alarm_statu = [row[0], row[1], 6, 1]
            params.append(alarm_statu)
        elif row[6] and (row[2] > row[6] or row[3] > row[6]):
            alarm_statu = [row[0], row[1], 6, 2]
            params.append(alarm_statu)
    return params
    """
    if params:
        sql = '''insert into ALARM_T(ip, port,`type`, alarm_level, check_time) values(%s, %s,%s, %s,%s)'''
        mydb.insert_many(sql, params)
    """


def sel_discards():
    """丢包告警, state=7"""
    # cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    sel_sql = '''select p.ip,p.port, round(ifnull((discards/iUpps*100),0),2), round(ifnull((odiscards/iUpps*100),0),2), a.LL, a.L,a.H, a.HH, a.level 
                 from portinfo p, ALARM_Value a where p.ip=a.ip and p.port=a.port and (a.ziduan='discards' or a.ziduan='odiscards') '''
    rows = mydb.select(sel_sql)

    # 判断丢包率是否告警
    params = []
    for row in rows:
        if row[7] and (row[2] > row[7] or row[3] > row[7]):
            alarm_statu = [row[0], row[1], 7, 1]
            params.append(alarm_statu)
        elif row[6] and (row[2] > row[6] or row[3] > row[6]):
            alarm_statu = [row[0], row[1], 7, 2]
            params.append(alarm_statu)
    return params
    """
    if params:
        sql = '''insert into ALARM_T(ip, port,`type`, alarm_level, check_time) values(%s, %s,%s, %s,%s)'''
        mydb.insert_many(sql, params)
    """


def getRelieveList():
    '''
        #获取已经解除的告警
        #返回 使用元组为单位组成的list
    '''
    cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    sel_sql = '''SELECT ip, port, state, alarm_level FROM ALARM_Relieve 
                 WHERE (starttime < '%s' AND endtime > '%s') or bz='0' ''' % (cur_time, cur_time)
    rows = mydb.select(sel_sql)
    params = []
    for row in rows:
        params.append(list(row))
    return params


def main():
    # 多线程获取告警数据
    t = [i for i in range(7)]
    cur_info = []
    t[0] = MyThread(sel_is_connect, '')
    t[1] = MyThread(sel_cpu, '')
    t[2] = MyThread(sel_ram, '')
    t[3] = MyThread(sel_port, '')
    t[4] = MyThread(sel_discards, '')
    t[5] = MyThread(sel_epps, '')
    t[6] = MyThread(sel_speed, '')

    for th in t:
        th.start()
    for th in t:
        th.join()
        cur_info.extend(th.get_result())

    relieve_list = getRelieveList()    # 解除数据

    # 排除解除报警
    if relieve_list:
        cur_info = [wran for wran in cur_info if wran not in relieve_list]

    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    sel_sql = '''select ip, port, state, alarm_level from ALARM_T'''
    ori_info = mydb.select(sel_sql)
    pre_info = []
    for pre in ori_info:
        pre_info.append(list(pre))
    new_wang = deepcopy([wran for wran in cur_info if wran not in pre_info])    # 新产生报警

    reco_wang = deepcopy([wran for wran in pre_info if wran not in cur_info])   # 已恢复报警
    # reco_wang = deepcopy([wran for wran in pre_info])  # 测试使用

    cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    host_info = mydb.select('select ip, type, sysname from hostinfo')

    # 新告警存入ALARM_S_new表
    t_sql = '''insert into ALARM_S_new(ip, port, state, alarm_level, starttime, `type`, sysname, alarm_status ) values(%s ,%s, %s,%s, %s,%s, %s, %s)'''
    t_info = []

    if new_wang:
        for wang in new_wang:
            wang.append(cur_time)
            for j in host_info:
                if j[0] == wang[0]:
                    # s_type = j[1]
                    wang.append(j[1])
                    wang.append(j[2])
                    wang.append(2)
                    break
            t_info.append(wang)
        mydb.insert_many(t_sql, t_info)

    # 恢复告警更新ALARM_S_new表
    s_sql = '''update ALARM_S_new set endtime=%s, alarm_status=%s where ip=%s and port=%s and state=%s and alarm_level=%s and (endtime like '0000-00-00 00:00:00' or alarm_status = '2')'''
    s_info = []
    if reco_wang:
        for wang in reco_wang:
            list_wang = list(wang)
            list_wang.insert(0, cur_time)
            list_wang.insert(1, 1)
            s_info.append(list_wang)

        mydb.insert_many(s_sql, s_info)

    # 更新ALARM_T表
    dele_sql = '''truncate table ALARM_T'''
    ins_sql = '''insert into ALARM_T(ip, port, state, alarm_level) values(%s, %s, %s, %s)'''

    mydb.insert_one(dele_sql)
    mydb.insert_many(ins_sql, cur_info)

if __name__ == "__main__":
    main()
