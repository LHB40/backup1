from urllib.request import urlopen
import socket
import requests
import re

socket.setdefaulttimeout(4)

def geturl(url):  #获取api内容
    html=urlopen(url)
    html=html.read()
    html=html.decode('gbk')
    return html

def imglink(url):
    html=geturl(url)
    reg = r'<input src=(.+?\.jpg)'
    imgre = re.compile(reg)   
    imglist = re.findall(imgre,html)
    reg = r'<title>(.+?)草榴社區'
    imgre = re.compile(reg)
    ti = re.findall(imgre,html)
    ti='TT'+ti[0]+'\n'
    txt=open('1.txt','a')
    txt.write(ti)
    txt.close()
    for i in imglist:
        i=i[1:]+'\n'
        txt=open('1.txt','a')
        txt.write(i)
        print(i)
        txt.close()

def makeurl():
    html=open('1.html','r')
    html=html.read()
    reg = r'<a title="打開新窗口" href="(.+?)" target="_blank">'
    imgre = re.compile(reg)   
    imglist = re.findall(imgre,html)
    for i in imglist:
        try:
            i='http://t66y.com/'+i
            print(i)
            imglink(i)
        except Exception as err:
            print(err)
            continue
        finally:
            pass
        
makeurl()
