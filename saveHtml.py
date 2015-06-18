#!/usr/bin/python
#-*- coding:utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
from Logger import Logger
import os

class saveHtml(object):
    """
        获取网页的html并存储，以及获取相应的js，css和imgs
    """

    def __init__(self):
        self.url = None
        self.html = None
        self.doc_tree = None 
        self.css_root_url = None
        self.logger = Logger()       
        self.root_dir = None    #存放的位置目录 

    # TODO(oucmath@126.com) 初始化网页地址和要存放的目录
    def init(self, htmlUrl, root_dir):
        self.url = htmlUrl
        self.root_dir = root_dir
        self.create_images_dir(self.root_dir)
        self.create_css_dir(self.root_dir)
        self.create_js_dir(self.root_dir)
        
   
     # TODO(oucmath@126.com) 获取原始的网页
    def get_raw_html(self):
        if None == self.url:
            self.logger.error('网页地址错误')
            return False
        try:
            self.html = urllib2.urlopen(self.url)
            self.doc_tree = BeautifulSoup(self.html.read(), 
                            from_encoding='utf-8')
            return True
        except Exception as e:
            self.logger.error('网页无法获取')
            return False
    
    # TODO(oucmath@126.com) 获取css的根url地址
    def get_css_root_url(self):
        if None == self.doc_tree:
            return False
        link = self.doc_tree.head.find('link', {'type': 'text/css'})
        self.css_root_url = link['href']
        index = self.css_root_url.find('tags')
        self.css_root_url = self.css_root_url[0: index+5]
        return True
    
    # TODO(oucmath@126.com) 获取html的logo图片，存储到images目录中
    def get_html_logo(self):
        logo_url = 'http://m.sohu.com/images/logo-icon.png'
        try:
           logo = urllib2.urlopen(logo_url)
           os.chdir(r'%s/%s' % (self.root_dir, 'images'))
           logo_file = open('logo-icon.png', 'wb')
           logo_file.write(logo.read())
           logo_file.close()
           return True
        except Exception as e:
            print e
            self.logger.error('get logo picture:%s fail' % (logo_url, ))
            return False

    # TODO(oucmath@126.com) 创建images目录，如果目录不存在则创建
    def create_images_dir(self, root_dir):
        if not os.path.exists(root_dir):
            self.logger.info('create dir %s' % (root_dir, ))
            os.mkdir(root_dir)
        os.chdir(root_dir)
        images_dir = r'%s/%s' % (root_dir, 'images')
        if not os.path.exists(images_dir):
            self.logger.info('create dir %s' % (images_dir, ))
            os.mkdir(images_dir)
        return True

    # TODO(oucmath@126.com) 创建css目录，如果目录不存在则创建
    def create_css_dir(self, root_dir):
        if not os.path.exists(root_dir):
            self.logger.info('create dir %s' % (root_dir, ))
            os.mkdir(root_dir)
        os.chdir(root_dir)
        css_dir = r'%s/%s' % (root_dir, 'css')
        if not os.path.exists(css_dir):
            self.logger.info('create dir %s' % (css_dir, ))
            os.mkdir(css_dir)
        return True

    # TODO(oucmath@126.com) 创建js目录，如果目录不存在则创建
    def create_js_dir(self, root_dir):
        if not os.path.exists(root_dir):
            self.logger.info('create dir %s' % (root_dir, ))
            os.mkdir(root_dir)
        os.chdir(root_dir)
        js_dir = r'%s/%s' % (root_dir, 'js')
        if not os.path.exists(js_dir):
            self.logger.info('create dir %s' % (js_dir, ))
            os.mkdir(js_dir)
        return True
    
    # TODO(oucmath@126.com) 获取网页的css文件(网页只有一个css)
    def get_html_css(self):
        pass


if __name__ == '__main__':
    helper = saveHtml()
    helper.init('http://m.sohu.com', '/home/arthur/test')
    helper.get_html_logo()
    helper.get_raw_html()
    
