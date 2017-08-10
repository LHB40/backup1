import socket
import urllib.request as ur
import os
import re
import threading
import time

socket.setdefaulttimeout(8)

def getimg(_url,name):
    while 1:
        if os.path.exists(name):
            break
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
            req = ur.Request(url=_url, headers=headers) 
            html=ur.urlopen(req)
            html=html.read()
            txt=open(name,'wb')
            txt.write(html)
            txt.close()
            c2=threading.activeCount()
            c3=c1-c2+2
            print(str(c3)+ '/' + str(c1) +'*'*4 + name)
            break
        except:
            continue
    
t=[]
txt=open('1.txt','r')
if not os.path.exists('1'):
    os.mkdir('1')
while 1:
    txtlin=txt.readline()
    if not txtlin:
        break
    if (txtlin[0:2]=='TT'):
        name=txtlin[2:-2]
        i=0
        name = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "",name)
    else:
        try:
            i+=1
            name1=r'1\%s' % name
            if not os.path.exists(name1):
                os.mkdir(name1)
            name1=r'1\%s\%s.jpg' % (name,i)
            t1=threading.Thread(target=getimg,args=(txtlin,name1))
            t.append(t1)
        except Exception as err:
            print(err)

c1=len(t)

for i in t:
    try:
        i.start()
    except:
        continue
while 1:
    if threading.activeCount()==1:
        a=input('finished!input any key to exit')
        break
    else:
        time.sleep(3)
        continue
