# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
from threading import Timer
import MySQLdb
from Icmp_Ping import select_ping
import time
import copy


class Mydb(object):
    """数据库操作：select，insert/update， create table"""
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
            print (e, 'in select sql')
        finally:
            self.close()
            return rows

    def insert_many(self, sql, params=()):
        try:
            self.connect()
            self.cursor.executemany(sql, params)
            self.conn.commit()
        except Exception as e:
            print(e, 'in insert sql %s', sql)
            self.conn.rollback()
        finally:
            self.close()



    def insert_one(self, sql):
        try:
            self.connect()
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e, 'in insert sql')
            self.conn.rollback()
        finally:
            self.close()

    def create_table(self, sql):
        try:
            self.connect()
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e, 'in create table')
        finally:
            self.close()


def select_host():
    """return ip, community"""
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    sql = "select ip, community from hostinfo"
    rows = mydb.select(sql)
    return rows


# ----------------------------------------------------------------------------------------------------------------------
# 创建host表
def insert_hostlog(sn=[0]):
    """ insert data to hostlog
        res 为delay数据
    """
    sn[0] += 1
    rows = select_host()
    res = select_ping(rows)

    # 插入ipinfo 表
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    values = []
    for i in res:
        value = i[1]
        value.append(sn[0])
        values.append(value)
    ins_sql = '''replace into ipinfo(ip, `is_connect`, `total_ram`, `free_ram`, `free_cpu`, `timestamp`, sn) 
                  values(%s, %s, %s, %s, %s, %s,%s)'''
    mydb.insert_many(ins_sql, values)

    select_sql = '''select ip , convert(ifnull(sum(discards)/(sum(discards)+sum(ibps)),0), DECIMAL(3,2)),sum(ibps), sum(obps), sum(iUpps), sum(oUpps),
                    sum(iMpps), sum(oMpps),sum(discards), sum(odiscards), sum(epps),sum(oepps), sn from portinfo group by ip, sn'''
    insert_sql = '''insert into hostlog(ip,`drop`,ibps, obps, iUpps, oUpps, iMpps, oMpps, discards, odiscards, epps,oepps, sn, delay, `timestamp`)
                    values(%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s, %s, %s,%s, %s)'''
    params = mydb.select(select_sql)
    para = []
    for i in params:
        n = list(i)
        for j in res:
            if n[0] == j[0][0]:
                n.append(j[0][1])
                n.append(timestamp)
                para.append(n)
    mydb.insert_many(insert_sql, para)


def insert_hosthour():
    """insert data to hosthour"""
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_time = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    select_sql = '''select ip , convert(avg(`drop`), DECIMAL(15,2)),convert(avg(delay), DECIMAL(15,4)), convert(avg(ibps), DECIMAL(15,2)),
                    convert(avg(obps), DECIMAL(15,2)), convert(avg(iUpps), DECIMAL(15,2)), convert(avg(oUpps), DECIMAL(15,2)),
                    convert(avg(iMpps), DECIMAL(15,2)), convert(avg(oMpps), DECIMAL(15,2)), convert(avg(discards), DECIMAL(15,2)), 
                    convert(avg(odiscards), DECIMAL(15,2)),convert(avg(epps), DECIMAL(15,2)),convert(avg(oepps), DECIMAL(15,2)) from hostlog 
                    where `timestamp` between '%s' and '%s' group by ip''' % (start_time, end_time)
    insert_sql = '''insert into hosthour(ip,`drop`, delay,ibps, obps, iUpps, oUpps, iMpps, oMpps, discards, odiscards, epps, oepps, `timestamp`)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s)'''
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    paras = mydb.select(select_sql)

    params = []  # 添加timestamp
    for para in paras:
        list_para = list(para)
        list_para.append(end_time)
        params.append(list_para)
    mydb.insert_many(insert_sql, params)


def insert_hosthourx():
    """insert data to hosthourx"""
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_time = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    select_sql = '''select ip , max(`drop`), max(delay), max(ibps), max(obps), max(iUpps), max(oUpps),max(iMpps), max(oMpps),max(discards), max(odiscards),
                    max(epps), max(oepps) from hostlog where `timestamp` between '%s' and '%s' group by ip''' % (start_time, end_time)
    insert_sql = '''insert into hosthourx(ip,`drop`, delay, ibps, obps, iUpps, oUpps, iMpps, oMpps, discards, odiscards, epps,oepps, `timestamp`)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s)'''

    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    paras = mydb.select(select_sql)

    params = []  # 添加timestamp

    for para in paras:
        list_para = list(para)
        list_para.append(end_time)
        params.append(list_para)
    mydb.insert_many(insert_sql, params)


def insert_hostday():
    """insert data to hosthour"""
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    select_sql = '''select ip , convert(avg(`drop`), DECIMAL(15,2)),convert(avg(delay), DECIMAL(15,4)), convert(avg(ibps), DECIMAL(15,2)),
                    convert(avg(obps), DECIMAL(15,2)), convert(avg(iUpps), DECIMAL(15,2)), convert(avg(oUpps), DECIMAL(15,2)),
                    convert(avg(iMpps), DECIMAL(15,2)), convert(avg(oMpps), DECIMAL(15,2)), convert(avg(discards), DECIMAL(15,2)), 
                    convert(avg(odiscards), DECIMAL(15,2)),convert(avg(epps), DECIMAL(15,2)),convert(avg(oepps), DECIMAL(15,2)) from hosthour 
                    where `timestamp` between '%s' and '%s' group by ip''' % (start_time, end_time)
    insert_sql = '''insert into hostday(ip,`drop`,delay, ibps, obps, iUpps, oUpps, iMpps, oMpps, discards,odiscards, epps,oepps, `timestamp`)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s, %s)'''
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    paras = mydb.select(select_sql)

    params = []  # 添加timestamp

    for para in paras:
        list_para = list(para)
        list_para.append(end_time)
        params.append(list_para)
    mydb.insert_many(insert_sql, params)


def insert_hostdayx():
    """insert data to hosthour"""
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    select_sql = '''select ip , max(`drop`), max(delay), max(ibps), max(obps), max(iUpps), max(oUpps),max(iMpps), max(oMpps),max(discards),max(odiscards),
                    max(epps), max(oepps) from hosthourx where `timestamp` between '%s' and '%s' group by ip''' % (start_time, end_time)
    insert_sql = '''insert into hostdayx(ip,`drop`,delay, ibps, obps, iUpps, oUpps, iMpps, oMpps, discards,odiscards, epps, oepps, `timestamp`)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s)'''
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    paras = mydb.select(select_sql)

    params = []  # 添加timestampa

    for para in paras:
        list_para = list(para)
        list_para.append(end_time)
        params.append(list_para)
    mydb.insert_many(insert_sql, params)

# ----------------------------------------------------------------------------------------------------------------------
# 创建port表

def insert_portinfo(params=[]):
    """"insert data to portinfo"""
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    replace_temp_sql = '''replace into portinfo_temp(`ip`, `port`, `desc`, `speed`, `state`,`ibps`, `obps`, `iUpps`, `oUpps`, `iMpps`,
                                        `oMpps`, `discards`, `odiscards`, `epps`, `oepps`, `timestamp`, sn) values(%s, %s, %s, %s/1000000, %s, %s,
                                         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    replace_sql = '''replace into portinfo(`ip`, `port`, `desc`, `speed`, `state`, `ibps`, `obps`, `iUpps`, `oUpps`, `iMpps`,
                    `oMpps`, `discards`, `odiscards`, `epps`, `oepps`, `timestamp`, sn) values(%s, %s, %s, %s/1000000, %s, %s,
                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    select_sql = '''select * from portinfo_temp'''
    pre_params = mydb.select(select_sql)     # 上一次采集原始数据
    next_params = copy.deepcopy(params)      # 本次将存入数据

    try:
        # 若临时表为空，则本次作为第一次采集，存放到临时表中
        if not pre_params:
            mydb.insert_many(replace_temp_sql, next_params)
            return
        else:
            cur_time = int(time.time())
            for pre in pre_params:

                # 若采集时间间隔超过10分钟，则将本次采集存放临时表
                pre_time = int(time.mktime(time.strptime(str(pre[15]), '%Y-%m-%d %H:%M:%S')))  # 转换为时间戳
                if cur_time - pre_time >= 10*60:
                    mydb.insert_many(replace_temp_sql, next_params)
                    return

                #  将本次采集与上次采集流量相减，取5分钟平均值，数据存入portinfo
                for param in params:
                    if pre[0] == param[0] and pre[1] == param[1]:
                        for i in range(5, 15):
                            param[i] = round((float(param[i]) - float(pre[i]))/300, 2)  # 结果保留2位小数
                            param[i] = param[i] if param[i] > 0 else 0
        mydb.insert_many(replace_sql, params)
        mydb.insert_many(replace_temp_sql, next_params)
    except Exception as e:
        print(e)


def insert_portlog():
    """insert data to portlog"""

    select_sql = '''select `ip`, `port`, `ibps`, `obps`, `iUpps`, `oUpps`, `iMpps`,`oMpps`, `discards`, `odiscards`, 
                    `epps`, `oepps`, cast(`timestamp` AS CHAR) AS `timestamp`, sn from portinfo
                    where ibps>0 or obps>0 or iUpps>0 or oUpps>0 or iMpps>0 or oMpps>0 or `discards` >0 or `odiscards`  '''
    insert_sql = '''insert into `portlog`(`ip`,`port`, `ibps`, `obps`, `iUpps`, `oUpps`, `iMpps`, `oMpps`, `discards`,`odiscards`,
                    `epps`, `oepps`,`timestamp`, sn) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'''
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    params = mydb.select(select_sql)
    mydb.insert_many(insert_sql, params)
    """
    for i in params:
        sql = insert_sql % i[0:12]
        mydb.insert_one(insert_sql, sql)
    """


def insert_porthour():
    """insert data to porthour"""
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_time = (datetime.now()-timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    select_sql = '''select ip, port, convert(avg(ibps), decimal(15,2)), convert(avg(obps), decimal(15,2)),convert(avg(iUpps), decimal(15,2)),
                    convert(avg(oUpps), decimal(15,2)), convert(avg(iMpps), decimal(15,2)),convert(avg(oMpps), decimal(15,2)),
                    convert(avg(discards), decimal(15,2)),convert(avg(odiscards), decimal(15,2)),convert(avg(epps), decimal(15,2)),
                    convert(avg(oepps), decimal(15,2)) from portlog where `timestamp` between '%s' and '%s' group by ip, port''' % (start_time, end_time)

    insert_sql = ''' insert into porthour(ip, port, ibps, obps, iUpps, oUpps, iMpps, oMpps, discards, odiscards, epps, oepps, `timestamp`)
                     values(%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s) '''
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    paras = mydb.select(select_sql)

    params = []  # 添加timestamp

    for para in paras:
        list_para = list(para)
        list_para.append(end_time)
        params.append(list_para)
    mydb.insert_many(insert_sql, params)


def insert_porthourx():
    """insert data to porthourx"""
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_time = (datetime.now()-timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    select_sql = '''select ip, port, max(ibps), max(obps), max(iUpps), max(oUpps), max(iMpps), max(oMpps),max(discards), max(odiscards),
                    max(epps), max(oepps) from portlog
                    where `timestamp` between '%s' and '%s' group by ip, port''' % (start_time, end_time)
    insert_sql = ''' insert into porthourx(ip, port, ibps, obps, iUpps, oUpps, iMpps, oMpps, discards, odiscards, epps, oepps,  `timestamp`)
                     values(%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s) '''

    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    paras = mydb.select(select_sql)

    params = []  # 添加timestamp

    for para in paras:
        list_para = list(para)
        list_para.append(end_time)
        params.append(list_para)
    mydb.insert_many(insert_sql, params)


def insert_portday():
    """insert data to portday"""
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_time = (datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    select_sql = '''select ip, port, convert(avg(ibps), decimal(15,2)), convert(avg(obps), decimal(15,2)),convert(avg(iUpps), decimal(15,2)),
                    convert(avg(oUpps), decimal(15,2)), convert(avg(iMpps), decimal(15,2)),convert(avg(oMpps), decimal(15,2)),
                    convert(avg(discards), decimal(15,2)),convert(avg(odiscards), decimal(15,2)),convert(avg(epps), decimal(15,2)),
                    convert(avg(oepps), decimal(15,2)) from porthour where `timestamp` between '%s' and '%s' group by ip, port''' % (start_time, end_time)

    insert_sql = ''' insert into portday(ip, port, ibps, obps, iUpps, oUpps, iMpps, oMpps, discards, odiscards, epps, oepps,  `timestamp`)
                     values(%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s) '''
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    paras = mydb.select(select_sql)

    params = []  # 添加timestamp

    for para in paras:
        list_para = list(para)
        list_para.append(end_time)
        params.append(list_para)
    mydb.insert_many(insert_sql, params)


def insert_portdayx():
    """insert data to portdayx"""
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_time = (datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    select_sql = '''select ip, port, max(ibps), max(obps), max(iUpps), max(oUpps), max(iMpps),max(oMpps),max(discards),max(odiscards),
                    max(epps), max(oepps) from porthourx where `timestamp` between '%s' and '%s' group by ip, port''' % (start_time, end_time)

    insert_sql = ''' insert into portdayx(ip, port, ibps, obps, iUpps, oUpps, iMpps, oMpps, discards, odiscards, epps, oepps,  `timestamp`)
                     values(%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s) '''
    mydb = Mydb(host='localhost', user='root', passwd='123456', db='test')
    paras = mydb.select(select_sql)

    params = []  # 添加timestamp

    for para in paras:
        list_para = list(para)
        list_para.append(end_time)
        params.append(list_para)
    mydb.insert_many(insert_sql, params)



def hour_execute():
    """每小时执行一次"""
    start_time = int(time.time())  # 定时执行时间戳

    insert_porthour()
    insert_porthourx()
    insert_hosthour()
    insert_hosthourx()

    # 定时执行

    end_time = int(time.time())
    exec_time = (60*60-(end_time-start_time))
    t1 = Timer(exec_time, hour_execute)
    t1.start()


def day_execute():
    """每天执行一次"""
    start_time = int(time.time())

    insert_portday()
    insert_portdayx()
    insert_hostday()
    insert_hostdayx()

    end_time = int(time.time())
    exec_time = (60*60*24 - (end_time - start_time))

    t2 = Timer(exec_time, day_execute)
    t2.start()


def main():
    hour_execute()
    day_execute()


if __name__ == '__main__':
    # main()
    hour_execute()

    #insert_portlog()



























