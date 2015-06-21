#!/usr/bin/python
#-*-coding:utf-8-*-

from datetime import datetime, timedelta
from saveHtml import saveHtml
from Logger import Logger
import thread
import sys
import os

# TODO(oucmath@126.com) 网页存储的工具方法
def work(url, root_dir):
    if not os.path.exists(root_dir): 
        os.mkdir(root_dir)
    html = saveHtml()
    html.init(url, root_dir)
    html.save()
    #thread.exit_thread()

# TODO(oucmath@126.com) 以线程的方式运行工具方法
def task(url, root_dir):
    thread.start_new_thread(work, (url, root_dir))
    

def main():
    if sys.argv.__len__() < 6:
        print 'Invalid params'
        return False
    url = ''
    time = 0
    root_dir = ''
    index = 1
    while index < 7:
        flag = sys.argv[index]
        if '-d' == flag:
            time = sys.argv[index + 1]
        if '-u' == flag:
            url = sys.argv[index + 1]
        if '-o' == flag:
            root_dir = sys.argv[index + 1]
        index = index + 2
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    now = datetime.now()
    strnow = now.strftime('%Y%m%d%H%M')
    root_dir_ = '%s/%s' % (root_dir, strnow)
    #task(url, root_dir_)
    work(url, root_dir_)
    period = timedelta(seconds=int(time))
    next_time = now + period
    while True:
        iter_now = datetime.now()
        iter_now_str = iter_now.strftime('%Y%m%d%H%M%S')
        next_time_str = next_time.strftime('%Y%m%d%H%M%S')
        if iter_now_str == next_time_str:
            iter_now_str = iter_now.strftime('%Y%m%d%H%M')
            root_dir_ = '%s/%s' % (root_dir, iter_now_str)
            #task(url, root_dir_)
            work(url, root_dir_)
            next_time = next_time + period
            continue

if __name__ == '__main__':
    main()
    
