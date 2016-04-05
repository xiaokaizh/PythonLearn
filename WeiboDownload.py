# -*-coding:utf8-*-

import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')
if len(sys.argv) == 2:
    user_id = (int)(sys.argv[1])
else:
    user_id = (int)(raw_input(u"请输入user_id: "))

cookie = {
    "Cookie": "_T_WM=d3e9b6943bccc56c0b5c86eaf8e0c46e; SUB=_2A2576mBBDeTxGeVM41cZ9CrMwjyIHXVZFQAJrDV6PUJbstAKLU_wkW1LHeszZ_QNqNnrrmdMsvFmBve2aC9Aag..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWEdlWHhs8IlOQQn3_qZmSH5JpX5o2p; SUHB=0N2l5hpCN_nuKk; SSOLoginState=1458442257; gsid_CTandWM=4uzeCpOz5qKroSYumKi9ZdMNu1s"}
url = 'http://weibo.cn/u/%d?filter=1&amp;page=1' % user_id

html = requests.get(url, cookies=cookie).content
selector = etree.HTML(html)
pageNum = 2

result = ""
urllist_set = set()
word_count = 1
image_count = 1

print u'爬虫准备就绪...'

for page in range(1, pageNum + 1):

    # 获取lxml页面
    url = 'http://weibo.cn/u/%d?filter=1&amp;page=%d' % (user_id, page)
    lxml = requests.get(url, cookies=cookie).content
    print u'获取xml页面%s' % (url)
    # 文字爬取
    selector = etree.HTML(lxml)
    content = selector.xpath('//span[@class="ctt"]')
    for each in content:
        text = each.xpath('string(.)')
        if word_count == 4:
            text = "%d :" % (word_count - 3) + text + "\n\n"
        else:
            text = text + "\n\n"
        result = result + text
        word_count += 1

    # 图片爬取
    soup = BeautifulSoup(lxml, "lxml")
    urllist = soup.find_all('a', href=re.compile(r'^http://weibo.cn/mblog/oripic', re.I))
    first = 0
    for imgurl in urllist:
        urllist_set.add(requests.get(imgurl['href'], cookies=cookie).url)
        image_count += 1

fo = open("%s.txt" % user_id, "ab")
fo.write(result)
word_path = os.getcwd() + '/%d' % user_id
print u'文字微博爬取完毕'

link = ""
fo2 = open("%s_imageurls.txt" % user_id, "ab")
for eachlink in urllist_set:
    link = link + eachlink + "\n"
fo2.write(link)
print u'图片链接爬取完毕'

if not urllist_set:
    print u'该页面中不存在图片'
else:
    # 下载图片,保存在当前目录的pythonimg文件夹下
    image_path = os.getcwd() + '/weibo_image'
    if os.path.exists(image_path) is False:
        os.mkdir(image_path)
    x = 1
    for imgurl in urllist_set:
        filename = "%s.jpg" % x
        dest_dir=os.path.join(image_path, filename)
        print u"下载地址%s" % image_path
        print u"文件名 %s"% filename
        print u'正在下载第%s张图片' % x
        try:
            urllib.urlretrieve(imgurl, dest_dir)
            urllib.urlcleanup()
            print u"该图片下载成功:%s" % imgurl
        except:
            print u"该图片下载失败:%s" % imgurl
        x += 1

print u'原创微博爬取完毕，共%d条，保存路径%s' % (word_count - 4, word_path)
print u'微博图片爬取完毕，共%d张，保存路径%s' % (image_count - 1, image_path)
