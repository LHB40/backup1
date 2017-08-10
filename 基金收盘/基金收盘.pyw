from urllib.request import urlopen as ur
import socket
import re,time
import tkinter as tk
from threading import Thread as th

socket.setdefaulttimeout(4)

def gethtml(code,n):
    if n==0:
        url=r'https://www.howbuy.com/fund/ajax/gmfund/valuation/valuationnav.htm?jjdm=%s' % code
    else:
        url=r'http://fund.eastmoney.com/%s.html?spm=aladin' % code
    res=ur(url)
    html=res.read()
    try:
        html=html.decode('utf-8')
    except:
        try:
            html=html.decode('gbk')
        except:
            return 0
    return html

def getrate(html):
    reg=re.compile(r'<span class="con_ratio_red">(.+?)</span>')
    result=re.findall(reg,html)
    try:
        return result[0]
    except:
        return '未收盘'

def getname(html):
    reg=re.compile(r'<div style="float: left">(.+?)<span>')
    result=re.findall(reg,html)
    return result[0]

class win():
    def __init__(self):
        self.w=tk.Tk()
        self.li=tk.Listbox(self.w,width=25)
        self.li.pack()
    def loop(self):
        self.w.mainloop()
    def getvalue(self):
        for i in open(r'1.txt','r'):
            value=getname(gethtml(i.strip('\n'),1)) +' : '+getrate(gethtml(i.strip('\n'),0))
            try:
                self.li.insert(0,value)
            except:
                pass
    def getv(self):
        th(target=self.getvalue).start()

            
if __name__=='__main__':
    w=win()
    w.getv()
    w.loop()


