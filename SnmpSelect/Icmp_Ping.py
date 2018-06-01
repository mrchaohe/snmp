#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Moming
# 2016-04-07
# ping

import os
import sys
import socket
import struct
import select
import time
import ctypes
from mult_thread import MyThread
from collections import defaultdict
from datetime import datetime
from snmp_gather import SelectSnmp


ICMP_ECHO_REQUEST = 8


def receive_ping(my_socket, ID, timeout):
    """
    receive the ping from the socket
    """
    start_time = timeout
    while True:
        start_select = time.clock()
        # select.select(rlist, wlist, xlist[, timeout])
        # wait until ready for read / write / exceptional condition
        # The return value is a triple of lists
        what_ready = select.select([my_socket], [], [], start_time)
        how_long = (time.clock() - start_select)
        if what_ready[0] == []: #timeout
            return

        time_received = time.clock()
        # socket.recvfrom(bufsize[, flags])
        # The return value is a pair (string, address)
        rec_packet, addr = my_socket.recvfrom(1024)
        icmp_header = rec_packet[20 : 28]
        ip_type, code, checksum, packet_ID, sequence = struct.unpack("bbHHh", icmp_header)
        if ip_type != 8 and packet_ID == ID: # ip_type should be 0
            byte_in_double = struct.calcsize("d")
            time_sent = struct.unpack("d", rec_packet[28 : 28 + byte_in_double])[0]
            return time_received - time_sent

        start_time = start_time - how_long
        if start_time <= 0:
            return


def get_checksum(source):
    """
    return the checksum of source
    the sum of 16-bit binary one's complement
    """
    checksum = 0
    count = (len(source) / 2) * 2
    i = 0
    while i < count:
        temp = ord(source[i + 1]) * 256 + ord(source[i]) # 256 = 2^8
        checksum = checksum + temp
        checksum = checksum & 0xffffffff # 4,294,967,296 (2^32)
        i = i + 2

    if i < len(source):
        checksum = checksum + ord(source[len(source) - 1])
        checksum = checksum & 0xffffffff

    # 32-bit to 16-bit
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = checksum + (checksum >> 16)
    answer = ~checksum
    answer = answer & 0xffff

    # why? ans[9:16 1:8]
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def send_ping(my_socket, ip_addr, ID):
    """
    send ping to the given ip address
    """
    ip = socket.gethostbyname(ip_addr)

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    my_checksum = 0

    # Make a dummy heder with a 0 checksum
    # struct.pack(fmt, v1, v2, ...)
    # Return a string containing the values v1, v2, ... packed
    # according to the given format.
    # b:signed char, h:short 2, H:unsigned short 2
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    # struct.calcsize(fmt)
    # Return the size of the struct corresponding to the given format.
    byte_in_double = struct.calcsize("d") # C type: double
    data = (192 - byte_in_double) * "P" # any char is OK, any length is OK
    data = struct.pack("d", time.clock()) + data

    # Calculate the checksum on the data and the dummy header.
    my_checksum = get_checksum(header + data)

    # It's just easier to make up a new header than to stuff it into the dummy.
    # socket.htons(x)
    # Convert 16-bit positive integers from host to network byte order.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1)
    packet = header + data
    # my_socket.sendto(packet, (ip, 1)) # getsockaddrarg() takes exactly 2 arguments
    my_socket.sendto(packet, (ip, 80)) # it seems that 0~65535 is OK (port?)


def ping_once(ip_addr, timeout):
    """
    return either delay (in second) or none on timeout.
    """
    # Translate an Internet protocol name to a constant suitable for
    # passing as the (optional) third argument to the socket() function.
    # This is usually only needed for sockets opened in “raw” mode.
    icmp = socket.getprotobyname('icmp')
    try:
        # socket.socket([family[, type[, proto]]])
        # Create a new socket using the given address family(default: AF_INET),
        # socket type(SOCK_STREAM) and protocol number(zero or may be omitted).
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error:
        raise

    # Return the current process id.
    # int: 0xFFFF = -1, unsigned int: 65535
    my_ID = os.getpid() & 0xFFFF

    send_ping(my_socket, ip_addr, my_ID)
    delay = receive_ping(my_socket, my_ID, timeout)

    my_socket.close()
    return delay


def icmp_ping(ip_addr, timeout=0.5, count=4):
    """
    send ping to ip_addr for count times with the given timeout
    """
    is_connect = 1

    for i in range(count):
        try:
            delay = ping_once(ip_addr, timeout)
        except socket.gaierror, e:
            print "failed. (socket error: '%s')" % e[1]
        if delay == None:
            print 'failed. (timeout within %s second.)' % timeout
            is_connect = 0
        else:
            pass
    result = [ip_addr, round(delay, 4), is_connect]
    return result


def select_ipinfo(row):
    """查询CPU利用率，内存利用率,是否可达"""
    cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dely_resu = icmp_ping(row[0])

    search_list = ["memTotalReal", "memAvailReal",  "ssCpuIdle"]

    if dely_resu[2] == 0:
        ipinfo = [row[0], 0, 0, 0, 0, cur_time]
    else:
        try:
            community = row[1].split(';')[0]
            ipinfo = [dely_resu[0], dely_resu[2]]

            ipsnmp = SelectSnmp(row[0], community)
            for value in search_list:
                result = ipsnmp.search_port(value)
                if not result:
                    ipinfo.append(0)
                    continue
                id, value = ipsnmp.parse_line(result[0])

                if value.startswith('No'):
                    ipinfo.append(0)
                else:
                    val = value.split(' ')[0].strip()
                    ipinfo.append(val)
            ipinfo.append(cur_time)
        except Exception as e:
            print(e)
    return [dely_resu, ipinfo]


def select_ping(rows):
    """返回ping结果"""
    res = []
    while 1:
        threads = []
        thread_num = 10
        for i in range(thread_num):
            try:
                row = rows.pop()
                thread = MyThread(select_ipinfo, list(row))
                threads.append(thread)
            except Exception as e:
                print(e, 'in ping row')
        try:
            for th in threads:
                th.start()
            for th in threads:
                th.join(timeout=20)
                result = th.get_result()
                res.append(result)

        except Exception as e:
            print (e, 'in multithread')
        if not rows:
            break
    return res


if __name__ == '__main__':
    rows = [['localhost', 'public']],

    res = select_ping(rows)
    print res


