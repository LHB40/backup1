import urllib.request as ur
import re
from urllib.parse import unquote
from threading import Thread as th
import threading
import time
import os

st=1
if st==0:
    url1=r'http://www.gb688.cn/bzgk/gb/std_list_type?r=0.6317334363354967&page=%s&pageSize=50&p.p1=1&p.p5=PUBLISHED&p.p90=circulation_date&p.p91=desc'
else:
    url1=r'http://www.gb688.cn/bzgk/gb/std_list_type?r=0.2806449853929156&page=%s&pageSize=50&p.p1=2&p.p90=circulation_date&p.p91=desc'

url2=r'http://c.gb688.cn/bzgk/gb/showGb?type=online&hcno='
url=r'http://c.gb688.cn/bzgk/gb/viewGb?hcno='
url3=r'http://www.gb688.cn/bzgk/gb/newGbInfo?hcno='

count=10
lis=[]
mark=0
marks=[0 for i in range(count)]
lock=threading.Lock()
threads=[]

def html(url):
    request=ur.urlopen(url)
    request=request.read().decode('utf-8')
    return request

def getNext(html):
    results=re.findall('showInfo\(\'(.+?)</a>',html,re.M)
    return results

def download(code,name):
    name=name+r'.pdf'
    name=name.replace(r':','：')
    if not os.path.exists(name):
        #print(name)
        target=url+code
        try:
            request=ur.urlopen(target)
            content=request.read()
            txt=open(name,'wb')
            txt.write(content)
            txt.flush()
            txt.close()
        except:
            yulan=url3+code
            request=ur.urlopen(yulan)
            content=request.read().decode('utf-8')
            if len(re.findall('在线预览',content))!=0:
                target=url2+code
                target= '''[{000214A0-0000-0000-C000-000000000046}]
Prop3=19,2
[InternetShortcut]
IDList=
URL=%s''' % target
                name=name.replace(r'.pdf',r'.url')
                name=name.replace('/',' ')
                txt=open(name,'wb')
                txt.write(target.encode('utf-8'))
                txt.flush()
                txt.close()
                
def main():
    for j in range(42 if st==0 else 770):
        tar=url1 % str(j+1)
        tars=getNext(html(tar))
        lock.acquire()
        for i in range(0,len(tars),2):
            urlTmp=tars[i].split('\'')
            lis.append((urlTmp[0],urlTmp[1][4:]+' '+tars[i+1].split('\'')[1][4:]))
        lock.release()
    while 1:
        lock.acquire()
        if sum(marks)==0 and len(lis)==0:
            mark=1
            time.sleep(2)
            break
        lock.release()
        time.sleep(3)
        
def sub(i):
    while 1:
        if mark==1:
            break
        lock.acquire()
        if len(lis)!=0:
            code=lis[0][0]
            name=lis[0][1]
            marks[i]=1
            del(lis[0])
            lock.release()
            try:
                download(code,name) 
            except:
                pass
            finally:
                marks[i]=0
        else:
            lock.release()
        time.sleep(1)

for i in range(count):
    th1=th(target = sub, args =(i,))
    threads.append(th1)
for t in threads:
    t.start()
main()

