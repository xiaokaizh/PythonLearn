import urllib2
import requests
import struct
__author__ = 'Administrator'

# ����url ����ҳ�������ص�ַ

def IsHtml(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    HttpMessage = response.info()
    ContentType = HttpMessage.gettype()
    print ContentType

# ����Torrent �ļ���Ч
def downtorrent(url):
    response = requests.get(url=url)
    file = open('test.torrent', 'ab')
    file.write(response.content)
    file.close()

def filetype(filename):
    binfile = open(filename, 'rb') # ��������ֶ�ȡ
    tl = typeList()
    ftype = 'unknown'
    for hcode in tl.keys():
        numOfBytes = len(hcode) / 2 # ��Ҫ�������ֽ�
        binfile.seek(0) # ÿ�ζ�ȡ��Ҫ�ص��ļ�ͷ����Ȼ��һֱ�����ȡ
        hbytes = struct.unpack_from("B"*numOfBytes, binfile.read(numOfBytes)) # һ�� "B"��ʾһ���ֽ�
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