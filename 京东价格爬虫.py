from urllib.request import urlopen
from urllib.request import Request
import re
from threading import Thread
import json
import sqlite3 as sq
import threading
import time

#lock=threading.Lock()

def Html(url):
    headers={'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWeb
             Kit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'''}
    request=Request(url=url,headers=headers)
    response=urlopen(request)
    return response.read()

def Decode(string):
    try:
        result=string.decode('utf-8')
    except:
        result=string.decode('gbk')
    return result

def Price(html):
    #print(html)
    result=re.findall('jdPrice":(.+?)}',html)[0]+'}'
    return result

def Code(url):
    code=re.findall(r'skuId=(.+?)&',url)[0]
    return code

def Analysis(code):
    url=r'https://c0.3.cn/stock?skuId=' + code + r'&cat=9987,653,655&venderId=1000000127&area=1_72_4137_0&buyNum=1&choseSuitSkuIds=&extraParam={%22originid%22:%221%22}&ch=1&fqsp=0&pduid=15415498144851377488111&pdpin=&callback=jQuery3970021'
    #code=Code(url)
    html=Html(url)
    html=Decode(html)
    price=Price(html)
    price=json.loads(price)
    
    return price['p']

def SavePrice(code,price,date):
    string='"'+code + '","'+price+'","'+date+'"'
    string=r'insert into record(code,price,date) values(%s);' % string
    try:
        con=sq.connect(r"1.db")
        cu=con.cursor()
        cu.execute(string)
    except Exception as err:
        print(err)
    cu.close()
    con.commit()
    con.close()
    

'''def AnaOne(code,cu,date,con):
    price=Analysis(code)
    SavePrice(code,price,cu,date,con)'''

def Date():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def Create():
    con=sq.connect(r"1.db")
    cu=con.cursor()
    cu.execute(r'create table record(id int primary key,code varchar(20),price varchar(20), date varchar(20));')
    con.commit()
    cu.close()
    con.close()
    
def Read(code=""):
    con=sq.connect(r"1.db")
    cu=con.cursor()
    if code=="":
        cu.execute(r'select * from record;')
    else:
        cu.execute('select * from record where code=%s;' % code)
    result=cu.fetchall()
    cu.close()
    con.close()
    return result
    
def StartOne(code,date,lock):
    count=0
    st=0
    while 1:
        count+=1
        if count==4:
            break
        try:       
            price=Analysis(code)
        except:
            continue
        lock.acquire()
        try:
            SavePrice(code,price,date)
            st=1
        except:
            pass
        finally:
            lock.release()
            if st==1:
                print(code+" done\n")
                break
        
def ReadCode(t,date,lock):
    with open(r'code.txt','r') as txt:
        txt=txt.read()
        txt=txt.split('\n')
        if len(txt)>0:
            for i in txt:
                t1=Thread(target=StartOne,args=(i,date,lock))
                t.append(t1)

def StartThreads(t):
    for i in t:
        i.start()

def Start(lock):
    while 1:
        t=[]
        ReadCode(t,Date(),lock)
        StartThreads(t)
        time.sleep(3600)

if __name__=='__main__':
    lock=threading.Lock()
    Start(lock)
