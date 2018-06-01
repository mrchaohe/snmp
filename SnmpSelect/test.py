# -*- coding:utf-8 -*-
from multiprocessing import Process
import time
from Queue import Queue
from threading import Timer


def abc(i):
    print (i)


def main():
    i = 1
    q = Queue()
    q.put(i)
    print(2)
    t1 = Process(target=abc, args=(1,))
    t1.start()
    time.sleep(2)
    print(3)
    #t2 = Process(target=abc, args=(q.get(),))
    #t1.start()



main()

