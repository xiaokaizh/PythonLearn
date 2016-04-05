# coding:utf-8

# python 2.7.5
#
# 获取一些百度图片
# 1.指定标签
# 2.
# http://image.baidu.com/channel/listjson?pn=0&rn=1000&tag1=%E6%98%8E%E6%98%9F&tag2=%E5%BC%A0%E5%AD%A6%E5%8F%8B&ftags=&sorttype=0&ie=utf8&oe=utf-8&image_id=692147105
# 这是获取列表的方式
# pn 分页标识
# rn 页面内图片数量
# tag1 主标签
# tag2 分标签
# 其他字段暂时不管
#
# 3.返回的内容json 转字典
# 4.取download_url就可以了
# 5.下载
# 6.多线程加快点效率


from urllib import urlretrieve, urlcleanup
from urllib2 import *
import json
from hashlib import md5
import sys


class Baiduimage():
    """
    """

    def __init__(self, tag1, tag2, number=1, stored="."):
        self.tag1 = tag1
        self.tag2 = tag2
        self.number = str(number)
        self.url = self.make_url()
        self.stored = stored
        print "work start"

    def make_url(self):
        url = "http://image.baidu.com/channel/listjson?pn=0&rn=" + self.number + "&tag1=" + self.tag1 + "&tag2=" + self.tag2 + "&ftags=&sorttype=0&ie=utf8&oe=utf-8"
        return url

    def request_body(self):
        request = Request(self.url)
        # request.add_header();
        r = urlopen(request)
        return r.read()

    def parse_body(self):
        jsonstr = json.loads(self.request_body())
        urls = [i['download_url'] for i in jsonstr['data'] if i.has_key('download_url')]
        return (urls, urls.__len__())

    def image_name(self, url):
        return self.stored + "/" + md5(url).hexdigest() + "." + url.split(".")[-1]

    def dowload_image(self):
        (urls, urlnumber) = self.parse_body()

        def dowload(url):
            try:
                urlretrieve(url, self.image_name(url))
                urlcleanup()
            except:
                return False
            return True

        print "want " + self.number + " images, get images links " + str(urlnumber)
        if urlnumber == 0:
            print "Could not find a image link"
            pass
        else:
            print "Download start press Ctrl+Break to stop "
            count = 0
            for id, i in enumerate(urls):
                if dowload(i):
                    count += 1
                    sys.stdout.write("Dowdload[" + str(id + 1) + "] has download " + str(count) + chr(8) * 80)
                    sys.stdout.flush()

            print "\nwork end"

    def dowload_image_thread(self, threadnumber=2):
        """
        
        """
        (urls, urlnumber) = self.parse_body()

        print "Download start press Ctrl+Break to stop "

        def dowload(url):
            try:
                urlretrieve(url, self.image_name(url))
                urlcleanup()
            except:
                return False
            return True

        from Queue import Queue
        from threading import Thread
        from itertools import count
        def worker(count=count()):

            while True:
                (id, item) = q.get()

                if dowload(item):
                    sys.stdout.write("Dowdload[" + str(id + 1) + "] has download " + str(next(count) + 1) + chr(8) * 80)
                    sys.stdout.flush()

                q.task_done()

        q = Queue()
        for i in range(threadnumber):
            t = Thread(target=worker)
            t.daemon = True
            t.start()

        for id, item in enumerate(urls):
            q.put((id, item))
        q.join()  # block until all tasks are done
        print "work end"


if __name__ == "__main__":
    print "this is a test with thread "
    Baiduimage("明星", "刘德华", 100).dowload_image_thread()  # 自定义分类 关键词 图片个数 存放路径
