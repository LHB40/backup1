import re
import urllib.request
import base64
import os

m=1

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html

def getImg(html):
    reg = r'qTcms_S_m_murl_e="(.+?)"'    #正则表达式，得到图片地址
    imgre = re.compile(reg)     #re.compile() 可以把正则表达式编译成一个正则表达式对象.
    imglist = re.findall(imgre,html)      #re.findall() 方法读取html 中包含 imgre（正则表达式）的    数据
    #把筛选的图片地址通过for循环遍历并保存到本地
    #核心是urllib.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名
    aa=base64.b64decode(imglist[0]).decode('utf-8') #漫画网站的实际图片地址经过base64加密，故需要先解密
    return aa
    print(imglist)


def geturl(aa):
    global m
    x=0
    reg = r'.com/(.+?\.JPG)'    #正则表达式，得到图片地址
    imgre = re.compile(reg)     #re.compile() 可以把正则表达式编译成一个正则表达式对象.
    imglist = re.findall(imgre,aa)
    if len(imglist)==0: #防止有时网站里jpg的大小写问题
        reg = r'.com/(.+?\.jpg)'
        imgre = re.compile(reg)
        imglist = re.findall(imgre,aa)
    os.mkdir(r'%s' % m ) #为每个页面创建一个文件夹
    for imgurl in imglist:
        imgurl=imgurl.replace('/','_') #替换地址里的/为_
        imgurl=r'http://www.gugu5.com/qTcms_Cache/Pic/'+imgurl #产生实际url
        print(imgurl)
        urllib.request.urlretrieve(imgurl,r'%s\%s.jpg' % (m,x) ) #下载图片
        x+=1
    m+=1

for x in range(757,818):
    url=r'http://www.gugu5.com/n/5247/249%s.html' % x
    try:   #防止目标页面有两种编码
        html = getHtml(url).decode('gbk')
    except:
        html = getHtml(url).decode('utf-8')
    geturl(getImg(html))
    
