# -*- coding:utf-8 -*-
import time
from Mysql_Db import Mydb


def hostlog(sql_obj):
    """create table hostlog"""

    start_time = time.localtime()
    table_time = time.strftime('%Y-%m-%d', start_time)
    table_name = 'hostlog-' + table_time
    sql = '''CREATE TABLE `%s` (
                    `ip` char(15) NOT NULL DEFAULT '',
                    `drop` double NOT NULL DEFAULT '0',
                    `delay` double NOT NULL DEFAULT '0',
                    `ibps` double NOT NULL DEFAULT '0',
                    `obps` double NOT NULL DEFAULT '0',
                    `iUpps` double NOT NULL DEFAULT '0',
                    `oUpps` double NOT NULL DEFAULT '0',
                    `iMpps` double NOT NULL DEFAULT '0',
                    `oMpps` double NOT NULL DEFAULT '0',
                    `discards` double NOT NULL DEFAULT '0',
                    `odiscards` double NOT NULL DEFAULT '0',
                    `epps` double NOT NULL DEFAULT '0',
                    `oepps` double NOT NULL DEFAULT '0',
                    `state` int(11) NOT NULL DEFAULT '0',
                    `timestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
                    `sn` int(4) NOT NULL DEFAULT '0',
                    KEY `k1` (`ip`)
                    ) ENGINE=MyISAM DEFAULT CHARSET=utf8
            ''' % table_name
    sql_obj.create_table(sql)


def hosthour(sql_obj):
    """create table hosthour/hosthourx"""
    start_time = time.localtime()
    table_time = time.strftime('%Y-%m', start_time)
    table_names = ['hosthour-' + table_time, 'hosthourx-' + table_time]
    for table_name in table_names:
        sql = '''CREATE TABLE `%s` (
                        `ip` char(15) NOT NULL DEFAULT '',
                        `drop` double NOT NULL DEFAULT '0',
                        `delay` double NOT NULL DEFAULT '0',
                        `ibps` double NOT NULL DEFAULT '0',
                        `obps` double NOT NULL DEFAULT '0',
                        `iUpps` double NOT NULL DEFAULT '0',
                        `oUpps` double NOT NULL DEFAULT '0',
                        `iMpps` double NOT NULL DEFAULT '0',
                        `oMpps` double NOT NULL DEFAULT '0',
                        `discards` double NOT NULL DEFAULT '0',
                        `odiscards` double NOT NULL DEFAULT '0',
                        `epps` double NOT NULL DEFAULT '0',
                        `oepps` double NOT NULL DEFAULT '0',
                        `state` int(11) NOT NULL DEFAULT '0',
                        `timestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
                        KEY `k1` (`ip`)
                        ) ENGINE=MyISAM DEFAULT CHARSET=utf8
                ''' % table_name
        sql_obj.create_table(sql)


def hostday(sql_obj):
    """create table hostday/hostdayx"""
    start_time = time.localtime()
    table_time = time.strftime('%Y', start_time)
    table_names = ['hostday-' + table_time, 'hostdayx-' + table_time]
    for table_name in table_names:
        sql = '''CREATE TABLE `%s` (
                        `ip` char(15) NOT NULL DEFAULT '',
                        `drop` double NOT NULL DEFAULT '0',
                        `delay` double NOT NULL DEFAULT '0',
                        `ibps` double NOT NULL DEFAULT '0',
                        `obps` double NOT NULL DEFAULT '0',
                        `iUpps` double NOT NULL DEFAULT '0',
                        `oUpps` double NOT NULL DEFAULT '0',
                        `iMpps` double NOT NULL DEFAULT '0',
                        `oMpps` double NOT NULL DEFAULT '0',
                        `discards` double NOT NULL DEFAULT '0',
                        `odiscards` double NOT NULL DEFAULT '0',
                        `epps` double NOT NULL DEFAULT '0',
                        `oepps` double NOT NULL DEFAULT '0',
                        `state` int(11) NOT NULL DEFAULT '0',
                        `timestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
                        KEY `k1` (`ip`)
                        ) ENGINE=MyISAM DEFAULT CHARSET=utf8
                ''' % table_name
        sql_obj.create_table(sql)


def portday(sql_obj):
    """
        create table portday/portdayx
        sql 为Mydb 类对象
    """
    start_time = time.localtime()
    table_time = time.strftime('%Y', start_time)
    table_names = ['portday-' + table_time, 'portdayx-' + table_time]
    for table_name in table_names:
        sql = '''CREATE TABLE `%s`(
                    ip char(15) NOT NULL DEFAULT '',
                    port char(31) NOT NULL DEFAULT '',
                   `ibps` double NOT NULL DEFAULT '0',
                   `obps` double NOT NULL DEFAULT '0',
                   `iUpps` double NOT NULL DEFAULT '0',
                   `oUpps` double NOT NULL DEFAULT '0',
                   `iMpps` double NOT NULL DEFAULT '0',
                   `oMpps` double NOT NULL DEFAULT '0',
                   `discards` double NOT NULL DEFAULT '0',
                   `odiscards` double NOT NULL DEFAULT '0',
                   `epps` double NOT NULL DEFAULT '0',
                   `oepps` double NOT NULL DEFAULT '0',
                    timestamp datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
                    KEY k1 (ip,port, timestamp)
                    ) ENGINE=MyISAM DEFAULT CHARSET=utf8
        ''' % table_name
        sql_obj.create_table(sql)


def porthour(sql_obj):
    """
        create table pothour/porthourx
        sql 为Mydb 类对象
    """
    start_time = time.localtime()
    table_time = time.strftime('%Y-%m', start_time)
    table_names = ['porthour-' + table_time, 'porthourx-' + table_time]
    for table_name in table_names:
        sql = '''CREATE TABLE `%s`(
                    ip char(15) NOT NULL DEFAULT '',
                    port char(31) NOT NULL DEFAULT '',
                   `ibps` double NOT NULL DEFAULT '0',
                   `obps` double NOT NULL DEFAULT '0',
                   `iUpps` double NOT NULL DEFAULT '0',
                   `oUpps` double NOT NULL DEFAULT '0',
                   `iMpps` double NOT NULL DEFAULT '0',
                   `oMpps` double NOT NULL DEFAULT '0',
                   `discards` double NOT NULL DEFAULT '0',
                   `odiscards` double NOT NULL DEFAULT '0',
                   `epps` double NOT NULL DEFAULT '0',
                   `oepps` double NOT NULL DEFAULT '0',
                    timestamp datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
                    KEY k1 (ip,port, timestamp)
                    ) ENGINE=MyISAM DEFAULT CHARSET=utf8
        ''' % table_name
        sql_obj.create_table(sql)


def portlog(sql_obj):
    """
        create table portlog
        sql 为Mydb 类对象
    """
    start_time = time.localtime()
    table_time = time.strftime('%Y-%m-%d', start_time)
    table_name = 'portlog-' + table_time
    sql = '''CREATE TABLE `%s`(
                    ip char(15) NOT NULL DEFAULT '',
                    port char(31) NOT NULL DEFAULT '',
                   `ibps` double NOT NULL DEFAULT '0',
                   `obps` double NOT NULL DEFAULT '0',
                   `iUpps` double NOT NULL DEFAULT '0',
                   `oUpps` double NOT NULL DEFAULT '0',
                   `iMpps` double NOT NULL DEFAULT '0',
                   `oMpps` double NOT NULL DEFAULT '0',
                   `discards` double NOT NULL DEFAULT '0',
                   `odiscards` double NOT NULL DEFAULT '0',
                   `epps` double NOT NULL DEFAULT '0',
                   `oepps` double NOT NULL DEFAULT '0',
                   `timestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
                    sn int(4) NOT NULL DEFAULT '0',
                    KEY k1 (ip,port, timestamp)
                    ) ENGINE=MyISAM DEFAULT CHARSET=utf8
        ''' % table_name
    sql_obj.create_table(sql)


def portinfo(sql_obj):
    sql = """  CREATE TABLE `portinfo_temp` (
        `ip` char(15) NOT NULL DEFAULT '',
        `port` char(31) NOT NULL DEFAULT '',
        `desc` char(127) NOT NULL DEFAULT '',
        `speed` double NOT NULL DEFAULT '0',
        `state` int(11) NOT NULL DEFAULT '0',
        `ibps` double NOT NULL DEFAULT '0',
        `obps` double NOT NULL DEFAULT '0',
        `iUpps` double NOT NULL DEFAULT '0',
        `oUpps` double NOT NULL DEFAULT '0',
        `iMpps` double NOT NULL DEFAULT '0',
        `oMpps` double NOT NULL DEFAULT '0',
        `discards` double NOT NULL DEFAULT '0',
        `odiscards` double NOT NULL DEFAULT '0',
        `epps` double NOT NULL DEFAULT '0',
        `oepps` double NOT NULL DEFAULT '0',
        `timestamp` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
        `sn` int(4) NOT NULL DEFAULT '1',
         PRIMARY KEY (`ip`,`port`),
        KEY `ip` (`ip`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
            """
    sql_obj.create_table(sql)


def e_day(sql_obj):
    portlog(sql_obj)
    hostlog(sql_obj)

def e_month(sql_obj):
    porthour(sql_obj)
    hosthour(sql_obj)


def e_year(sql_obj):
    portday(sql_obj)
    hostday(sql_obj)


def main():
    sql_obj = Mydb(host='10.213.75.27', user='root', passwd='Northstar@2017', db='dg_server', port=3306, charset='utf8')
    while 1:
        cur_time = time.localtime()
        if cur_time.tm_hour == 0 and cur_time.tm_min == 0:
            portlog(sql_obj)
            hostlog(sql_obj)
        if cur_time.tm_mday == 1 and cur_time.tm_hour == 0 and cur_time.tm_min in range(5):
            e_month(sql_obj)
            e_month(sql_obj)


if __name__ == "__main__":
    pass



