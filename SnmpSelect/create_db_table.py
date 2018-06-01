# -*- coding:utf-8 -*-
from datetime import datetime
from Mysql_Db import Mydb


def hostlog(sql_obj, table_name='hostlog'):
    """create table hostlog"""
    sql = '''CREATE TABLE `hostlog` (
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
                    partition by range(to_days(`timestamp`))(
                        partition p1 values less than (to_days('2017-11-29')),
                        partition p2 values less than (to_days('2017-11-30')),
                        partition p3 values less than (to_days('2017-12-01')),
                        partition p4 values less than (to_days('2017-12-02')),
                        partition p5 values less than (to_days('2017-12-03')),
                        partition p6 values less than (to_days('2017-12-04')),
                        partition p7 values less than (to_days('2017-12-05')),
                        partition p8 values less than (to_days('2017-12-06')),
                        partition p9 values less than (to_days('2017-12-07')),
                        partition p10 values less than (to_days('2017-12-08')),
                        partition p11 values less than (to_days('2017-12-09')),
                        partition p12 values less than (to_days('2017-12-10')),
                        partition p13 values less than (to_days('2017-12-11')),
                        partition p14 values less than (to_days('2017-12-12')),
                        partition p15 values less than (to_days('2017-12-13')),
                        partition p16 values less than (to_days('2017-12-14')),
                        partition p17 values less than (to_days('2017-12-15')),
                        partition p18 values less than (to_days('2017-12-16')),
                        partition p19 values less than (to_days('2017-12-17')),
                        partition p20 values less than (to_days('2017-12-18')),
                        partition p21 values less than (to_days('2017-12-19')),
                        partition p22 values less than (to_days('2017-12-20')),
                        partition p23 values less than (to_days('2017-12-21')),
                        partition p24 values less than (to_days('2017-12-22')),
                        partition p25 values less than (to_days('2017-12-23')),
                        partition p26 values less than (to_days('2017-12-24')),
                        partition p27 values less than (to_days('2017-12-25')),
                        partition p28 values less than (to_days('2017-12-26')),
                        partition p29 values less than (to_days('2017-12-27')),
                        partition p30 values less than (to_days('2017-12-28')),
                        partition p31 values less than (to_days('2017-12-29')),
                        partition p32 values less than (to_days('2017-12-30')),
                        partition p33 values less than (to_days('2017-12-31'))
                    );
            '''
    sql_obj.create_table(sql)


def hosthour(sql_obj, table_name='hostour'):
    """create table hosthour/hosthourx"""
    sql = '''CREATE TABLE `hosthourx` (
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
                        partition by range(to_days(timestamp))(
                            partition p1 values less than (to_days('2017-11-01')),
                            partition p2 values less than (to_days('2017-12-01')),
                            partition p3 values less than (to_days('2018-01-01')),
                            partition p4 values less than (to_days('2018-02-01')),
                            partition p5 values less than (to_days('2018-03-01')),
                            partition p6 values less than (to_days('2018-04-01'))
                        );
                '''
    sql_obj.create_table(sql)


def hostday(sql_obj, table_name='hostday'):
    """create table hostday/hostdayx"""
    sql = '''CREATE TABLE `hostdayx` (
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
                        partition by range(year(timestamp))(
                            partition p_2017 values less than (2017),
                            partition p_2018 values less than (2018),
                            partition p_2019 values less than (2019)
                        );
                '''
    sql_obj.create_table(sql)


def portday(sql_obj, table_name='portday'):
    """
        create table portday/portdayx
        sql 为Mydb 类对象
    """
    sql = '''CREATE TABLE `portday`(
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
                    partition by range(year(timestamp))(
                        partition p_2017 values less than (2017),
                        partition p_2018 values less than (2018),
                        partition p_2019 values less than (2019)
                    );
        '''
    sql_obj.create_table(sql)


def porthour(sql_obj, table_name='porthour'):
    """
        create table pothour/porthourx
        sql 为Mydb 类对象
    """
    sql = '''CREATE TABLE `porthour`(
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
                    partition by range(to_days(timestamp))(
                            partition p1 values less than (to_days('2017-11-01')),
                            partition p2 values less than (to_days('2017-12-01')),
                            partition p3 values less than (to_days('2018-01-01')),
                            partition p4 values less than (to_days('2018-02-01')),
                            partition p5 values less than (to_days('2018-03-01')),
                            partition p6 values less than (to_days('2018-04-01'))
                    );
        '''
    sql_obj.create_table(sql)


def portlog(sql_obj, table_name='portlog'):
    """
        create table portlog
        sql 为Mydb 类对象
    """
    sql = '''CREATE TABLE `portlog`(
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
                    partition by range(to_days(timestamp))(
                        partition p7 values less than (to_days('2017-12-05')),
                        partition p8 values less than (to_days('2017-12-06')),
                        partition p9 values less than (to_days('2017-12-07')),
                        partition p10 values less than (to_days('2017-12-08')),
                        partition p11 values less than (to_days('2017-12-09')),
                        partition p12 values less than (to_days('2017-12-10')),
                        partition p13 values less than (to_days('2017-12-11')),
                        partition p14 values less than (to_days('2017-12-12')),
                        partition p15 values less than (to_days('2017-12-13')),
                        partition p16 values less than (to_days('2017-12-14')),
                        partition p17 values less than (to_days('2017-12-15')),
                        partition p18 values less than (to_days('2017-12-16')),
                        partition p19 values less than (to_days('2017-12-17')),
                        partition p20 values less than (to_days('2017-12-18')),
                        partition p21 values less than (to_days('2017-12-19')),
                        partition p22 values less than (to_days('2017-12-20')),
                        partition p23 values less than (to_days('2017-12-21')),
                        partition p24 values less than (to_days('2017-12-22')),
                        partition p25 values less than (to_days('2017-12-23')),
                        partition p26 values less than (to_days('2017-12-24')),
                        partition p27 values less than (to_days('2017-12-25')),
                        partition p28 values less than (to_days('2017-12-26')),
                        partition p29 values less than (to_days('2017-12-27')),
                        partition p30 values less than (to_days('2017-12-28')),
                        partition p31 values less than (to_days('2017-12-29')),
                        partition p32 values less than (to_days('2017-12-30')),
                        partition p33 values less than (to_days('2017-12-31'))
                    );
        '''
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

if __name__ == "__main__":
    sql_obj = Mydb(host='10.213.75.27', user='root', passwd='Northstar@2017', db='dg_server', port=3306, charset='utf8')
