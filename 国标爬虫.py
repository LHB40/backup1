import urllib.request as ur
import re
from urllib.parse import unquote
from threading import Thread as th
import threading
import time

url1=r'http://www.gb688.cn/bzgk/gb/std_list_type?r=0.6317334363354967&page=%s&pageSize=50&p.p1=1&p.p5=PUBLISHED&p.p90=circulation_date&p.p91=desc'

url=r'http://c.gb688.cn/bzgk/gb/viewGb?hcno='

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
    #results=re.findall('showInfo\(\'(.+?)\'\)',html)
    results=re.findall('showInfo\(\'(.+?)</a>',html,re.M)
    return results

def download(code,name):
    target=url+code
    request=ur.urlopen(target)
    content=request.read()
    txt=open(name+r'.pdf','wb')
    txt.write(content)
    txt.flush()
    txt.close()

def main():
    for j in range(42):
        tar=url1 % str(j+1)
        tars=getNext(html(tar))
        lock.acquire()
        for i in range(0,len(tars),2):
            urlTmp=tars[i].split('\'')
            lis.append((urlTmp[0],urlTmp[1][4:]+' '+tars[i+1].split('\'')[1][4:]))
        lock.release()
    while 1:
        lock.acquire()
        print('threads count is'+str(len(threads))+'\n\n')
        if sum(marks)==0 and len(lis)==0:
            mark=1
            break
            print(1)
        sleep(3)
        lock.release()
        
def sub(i):
    while 1:
        if mark==1:
            print('thread',i,'exit')
            break
        lock.acquire()
        if len(lis)!=0:
            code=lis[0][0]
            name=lis[0][1]
            marks[i]=1
            del(lis[0])
            lock.release()
            try:
                print(name+'\n\n')
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

