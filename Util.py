import urllib2
import requests
import struct
__author__ = 'Administrator'

# 区分url 是网页还是下载地址

def IsHtml(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    HttpMessage = response.info()
    ContentType = HttpMessage.gettype()
    print ContentType

# 下载Torrent 文件有效
def downtorrent(url):
    response = requests.get(url=url)
    file = open('test.torrent', 'ab')
    file.write(response.content)
    file.close()

def filetype(filename):
    binfile = open(filename, 'rb') # 必需二制字读取
    tl = typeList()
    ftype = 'unknown'
    for hcode in tl.keys():
        numOfBytes = len(hcode) / 2 # 需要读多少字节
        binfile.seek(0) # 每次读取都要回到文件头，不然会一直往后读取
        hbytes = struct.unpack_from("B"*numOfBytes, binfile.read(numOfBytes)) # 一个 "B"表示一个字节
        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode:
            ftype = tl[hcode]
            break
    binfile.close()
    return ftype

def typeList():
    return {
        "52617221": EXT_RAR,
        "504B0304": EXT_ZIP}
class tt():
    def bytes2hex(bytes):
        num = len(bytes)
        hexstr = u""
        for i in range(num):
            t = u"%x" % bytes[i]
            if len(t) % 2:
                hexstr += u"0"
            hexstr += t
        return hexstr.upper()