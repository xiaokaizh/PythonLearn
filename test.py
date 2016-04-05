import requests
import os,sys
__author__ = 'Administrator'


import urllib2

# url = 'http://sis001.com/forum/attachment.php?aid=2716371'
# 2716371
url = 'http://sis001.com/forum/attachment.php?aid=2700001'
response = requests.get(url=url)
if response.content[0:3] == 'd13':
    print "Success"
else:
    print "No"

# num = len(bytes)
# hexstr = u""
# for i in range(num):
#     t = u"%x" % bytes[i]
#     if len(t) % 2:
#         hexstr += u"0"
#     hexstr += t
# print hexstr.upper()




# req = urllib2.Request(url)
# print req.type
# response = urllib2.urlopen(req)
# HttpMessage = response.info()
# ContentType = HttpMessage.gettype()
# print ContentType

# file = open('test.torrent', 'ab')
# file.write(response.content)
# file.close()