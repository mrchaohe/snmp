# -*- coding:utf-8 -*-
from threading import Thread


class MyThread(Thread):
    """多线程"""
    def __init__(self, func, args):
        # func 为 方法名
        Thread.__init__(self)
        self.args = args
        self.func = func
        self.data = []

    def run(self):
        if self.args:
            self.data = self.func(self.args)
        else:
            self.data = self.func()

    def get_result(self):
        return self.data

if __name__ == "__main__":
    pass
