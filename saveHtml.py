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
        link['href'] = '%s' % ('/css/home.css')
        return True
    
    # TODO(oucmath@126.com) 获取html的logo图片，存储到images目录中
    def get_html_logo(self):
        logo_url = 'http://m.sohu.com/images/logo-icon.png'
        try:
           logo = urllib2.urlopen(logo_url)
           if self.enter_or_create_images_dir(self.root_dir):
               logo_file = open('logo-icon.png', 'wb')
               logo_file.write(logo.read())
               logo_file.close()
               return True
           else:
               return False
        except Exception as e:
            self.logger.error('get logo picture:%s fail' % (logo_url, ))
            return False

    # TODO(oucmath@126.com) 创建images目录，如果目录不存在则创建
    def enter_or_create_images_dir(self, root_dir):
        if not os.path.exists(root_dir):
            self.logger.info('create dir %s' % (root_dir, ))
            os.mkdir(root_dir)
        os.chdir(root_dir)
        images_dir = r'%s/%s' % (root_dir, 'images')
        if not os.path.exists(images_dir):
            self.logger.info('create dir %s' % (images_dir, ))
            os.mkdir(images_dir)
        os.chdir(images_dir)
        return True

    # TODO(oucmath@126.com) 创建css目录，如果目录不存在则创建
    def enter_or_create_css_dir(self, root_dir):
        if not os.path.exists(root_dir):
            self.logger.info('create dir %s' % (root_dir, ))
            os.mkdir(root_dir)
        os.chdir(root_dir)
        css_dir = r'%s/%s' % (root_dir, 'css')
        if not os.path.exists(css_dir):
            self.logger.info('create dir %s' % (css_dir, ))
            os.mkdir(css_dir)
        os.chdir(css_dir)
        return True

    # TODO(oucmath@126.com) 创建js目录，如果目录不存在则创建
    def enter_or_create_js_dir(self, root_dir):
        if not os.path.exists(root_dir):
            self.logger.info('create dir %s' % (root_dir, ))
            os.mkdir(root_dir)
        os.chdir(root_dir)
        js_dir = r'%s/%s' % (root_dir, 'js')
        if not os.path.exists(js_dir):
            self.logger.info('create dir %s' % (js_dir, ))
            os.mkdir(js_dir)
        os.chdir(js_dir)
        return True
    
    # TODO(oucmath@126.com) 获取网页的css文件(网页只有一个css)
    def get_html_css(self):
        if None == self.doc_tree:
            return False
        link = self.doc_tree.find('link', {'type': 'text/css'})
        css_url = link['href']
        try:
            css = urllib2.urlopen(css_url)
            if self.enter_or_create_css_dir(self.root_dir):
                css_file = open('home.css', 'wb')
                css_file.write(css.read())
                css_file.close()
                return True
            else:
                return False
        except:
            self.logger.error('get home.css fail')
            return False

    # TODO(oucmath@126.com)
    def handle_css(self):
        """
        处理home.css,获取home.css中用到的图片，并将图片的远程地址替换为本地地址
        """
        if self.enter_or_create_css_dir(self.root_dir):
            try:
                css_file_in = open('home.css', 'r')
                css_file_out = open('home_back.css', 'w')
                line = css_file_in.readline()
                css_file_out.write(line)
                line = css_file_in.readline()
                modified_line = self.modify_css(line)
                css_file_out.write(modified_line)
                css_file_in.close()
                css_file_out.close()
                if self.enter_or_create_css_dir(self.root_dir):
                    os.remove('home.css')
                    os.rename('home_back.css', 'home.css')
                return True
            except Exception as e:
                print e
                self.logger.error('open home.css error')
                return False
        else:
            return False

    # TODO(oucmath@126.com) 修改css文件
    def modify_css(self, css):
        self.get_css_root_url()
        modified_line = ''
        last_pos = 0
        next_pos = css.find('url(', last_pos)
        while next_pos > 0:
            modified_line = '%s%s' % (modified_line, 
                                    css[last_pos: next_pos + 3])     
            last_pos = next_pos + 3
            next_pos = css.find(')', last_pos)
            pic_url = css[last_pos + 1: next_pos]
            local_pic_url = self.pic_download(pic_url)
            modified_line = '%s(%s' % (modified_line, local_pic_url)
            last_pos = next_pos
            next_pos = css.find('url(', last_pos)
        modified_line = '%s%s' % (modified_line, 
                                  css[last_pos:]) 
        return modified_line

    # TODO(oucmath@126.com) 根据pic的url获取pic并存档
    def pic_download(self, pic_url):
        if self.enter_or_create_images_dir(self.root_dir):
            try:
                pic_dir = ''
                last_slash = pic_url.rfind('/')
                pic_name = pic_url[last_slash + 1:]
                if 'http' in pic_url:
                    pic = urllib2.urlopen(pic_url)
                    upper_slash = pic_url.rfind('/', 0, last_slash)
                    pic_dir = pic_url[upper_slash + 1: last_slash]
                else:
                    pic_dir = pic_url[6: last_slash]
                    pic_url = '%s%s/%s' %  (self.css_root_url, 
                                            pic_dir, pic_name)
                    pic = urllib2.urlopen(pic_url)
                if not os.path.exists(os.path.join(os.getcwd(), pic_dir)):
                    os.mkdir(os.path.join(os.getcwd(), pic_dir))
                os.chdir(os.path.join(os.getcwd(), pic_dir))
                pic_file = open(pic_name, 'wb')
                pic_file.write(pic.read())
                pic_file.close()
                return '%s/%s/%s' % ('images', pic_dir, pic_name)
            except Exception as e:
                print e
                self.logger.error('download pic:%s fail' % (pic_url, ))
                return None
        else:
            return None  
    
    # TODO(oucmath@126.com) 获取js并存储到js目录中
    def get_html_js(self):
        if None == self.doc_tree:
            return False
        scripts = self.doc_tree.find_all('script', {'src': True})
        if None != scripts:
            for script in scripts:
                try:
                    js_url = script['src']
                    js = urllib2.urlopen(js_url)
                    if self.enter_or_create_js_dir(self.root_dir):
                        js_name = js_url[js_url.rfind('/') + 1:]
                        js_file = open(js_name, 'wb')
                        js_file.write(js.read())
                        js_file.close()
                        script['src'] = '%s%s' % ('/js/', js_name)
                except:
                    self.logger.error('open %s fail' % (script['src'],) )
        return True

    # TODO(oucmath@126.com) 更新a标签，全部替换为完全地址
    def update_a_tags(self):
        if None == self.doc_tree:
            return False
        a_tags = self.doc_tree.find_all('a', {'href': True})
        if None != a_tags:
            for a_tag in a_tags:
                a_href = a_tag['href']
                if a_href.startswith('/'):
                    a_tag['href'] = '%s%s' % (self.url, a_href)
        print self.doc_tree
        return True

if __name__ == '__main__':
    helper = saveHtml()
    helper.init('http://m.sohu.com', '/home/arthur/test')
    helper.get_html_logo()
    helper.get_raw_html()
    helper.get_html_css()
    helper.handle_css() 
    helper.get_html_js()
    helper.update_a_tags()
