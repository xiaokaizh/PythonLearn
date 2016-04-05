import random
import requests

__author__ = 'Administrator'
# coding:utf-8

import urllib
import urllib2

# 爬取sis001上的种子
success = 0
baseurl = "http://sis001.com/forum/attachment.php?aid="
i=2711000
def down():
    global i
    while(i < 2721010):
        if success > 20:
            break
        savetorrent(i)
        i += 1




def savetorrent(rdint):
    imgurl = baseurl + '%s' % rdint
    try:
        response = requests.get(url=imgurl)
        if response.content[0:3] == 'd13':
            fileName = '%s' % rdint + ".torrent"
            file = open(fileName, 'ab')
            file.write(response.content)
            file.close()
            print fileName + "  save pic OK"
            global success
            success += 1
        else:
            print "No Torrent:  " + imgurl
        # urllib.urlretrieve(imgurl, fileName)
        # urllib.urlcleanup()

    except :
        print "failed  " + imgurl
if __name__ == "__main__":
    down()