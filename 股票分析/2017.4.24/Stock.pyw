import urllib.request
import gzip
import json
import re
import socket
import time
import threading
import tkinter
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header
import winsound

socket.setdefaulttimeout(5)

class ur():   #网络连接类
    def __init__(self):
        pass
    def gethtml(self,url):
        html=urllib.request.urlopen(url)
        html=html.read()
        return html

    def gethtmll(self,url):
        html=self.gethtml(url)
        try:
            html=html.decode('utf-8')
        except:
            try:
                html=html.decode('gbk')
            except:
                try:
                    html=gzip.decompress(html).decode('utf-8')
                except:
                    html=gzip.decompress(html).decode('gbk')
        return html

class update(ur):   #更新股票代码类
    def __init__(self,n):
        self.url=r'http://vip.stock.finance.sina.com.cn/corp/go.php/vRPD_NewStockIssue/page/%d.phtml'
        self.n=int(n)
        self.code=set()
    def get(self):
        for i in range(self.n):
            i+=1
            code=self.url % i
            k=0
            while 1:
                k+=1
                if k==4:
                    break
                try: 
                    html=super().gethtmll(code)
                    break
                except:
                    continue
            reg=re.compile('<div align="center">(......)</div>')
            result=reg.findall(html)
            for i in result:
                try:
                    int(i)
                except:
                    continue
                i+='\n'
                self.code.add(i)
        try:
            for i in open('stock\\list.dat','r'):
                self.code.add(i)
        except:
            pass
        txt=open('stock\\list.dat','w')
        txt.close()
        txt=open('stock\\list.dat','a')
        for i in self.code:
            txt.write(i)
        txt.close()

class api(ur):   #获得个股的json数据类
    def __init__(self,code):
        self.code=str(code).strip('*')
        self.url=r"http://api.finance.ifeng.com/akdaily/?code=%s&type=last"
        self.js=None
    def get(self):
        if int(self.code)<600000:
            self.code='sz'+self.code
        else:
            self.code='sh'+self.code
        url=self.url % self.code
        while 1:
            try:
                html=super().gethtmll(url)
                break
            except:
                continue
        self.js=json.loads(html)
        self.js=self.js['record']

class api60(api): #继承api类功能，数据源改为60分钟线数据
    def __init__(self,code):
        self.code=str(code).strip('*')
        self.url=r'http://money.finance.sina.com.cn/quotes_service/api/jsonp_v2.php/a=/CN_MarketData.getKLineData?symbol=%s&scale=60&ma=no&datalen=1023'
    def get(self):
        self.js=None
        if self.code[0]!='s':
            if int(self.code)<600000:
                self.code='sz'+self.code
            else:
                self.code='sh'+self.code
        url=self.url % self.code
        while 1:
            try:
                html=super().gethtmll(url)
                break
            except:
                continue
        reg=re.compile('{(.*?)}')
        self.js=reg.findall(html)
        self.js=[i.split(',') for i in self.js]
        self.js=[i[4] for i in self.js]
        reg=re.compile('"(.*?)"')
        self.js=[reg.findall(i) for i in self.js]
        self.js=[float(i[0]) for i in self.js]
        
class macd(api):     #获得macd类
    def __init__(self,code):
        super().__init__(code)
        super().get()
        self.macd=[]   #macd元组
    def getmacd(self):
        if len(self.js)!=0:
            EMA1=float(self.js[0][3])
            EMA2=EMA1
            DIF=0
            DEA=0
            self.macd.append((0,DIF,DEA))
            k=0
            for i in self.js[1:]:
                k+=1
                EMA1=EMA1*11/13+float(i[3])*2/13
                EMA2=EMA2*25/27+float(i[3])*2/27
                DIF=round((EMA1-EMA2),3)
                DEA=round((DEA*8/10+DIF*2/10),3)
                self.macd.append((k,DIF,DEA,EMA1,EMA2))

class macd60(api60):  #获得60分钟macd
    def __init__(self,code):
        super().__init__(code)
    def getmacd(self):
        self.macd=[]
        super().get()
        EMA1=self.js[0]
        EMA2=EMA1
        DIF=0
        DEA=0
        self.macd.append((0,DIF,DEA))
        k=0
        for i in self.js[1:]:
            k+=1
            EMA1=EMA1*11/13+i*2/13
            EMA2=EMA2*25/27+i*2/27
            DIF=round((EMA1-EMA2),3)
            DEA=round((DEA*8/10+DIF*2/10),3)
            self.macd.append((k,DIF,DEA,EMA1,EMA2))
            
class getjc(macd):   #获得金叉
    def __init__(self,code):
        super().__init__(code)
        super().getmacd()
        self.jinc=[]  #存储金叉的元组,元素为金叉日的DIF
    def getjc_get(self,n,m):      #n代表搜索的天数，m代表几个涨停后开始判断
        if len(self.js)!=0:
            t1=0 #涨停板计数
            t2=0 #符合涨停天数的js位置
            i2=0 #0表示没有达到涨停计数，1表示达到
            if len(self.js)>int(n):
                i1=len(self.js)-int(n)   #js位置计数
                for i in self.js[len(self.js)-int(n):]:
                    if float(i[7])>9.8:
                        t1+=1
                    else:
                        t1=0
                    if t1==int(m):
                        t2=i1
                        i2=1
                    i1+=1
            else:
                i1=0 #js位置计数
                for i in self.js:
                    if float(i[7])>9.8:
                        t1+=1
                    else:
                        t1=0
                    if t1==int(m):
                        t2=i1
                        i2=1
                    i1+=1
            if i2==1:    
                k1=0 #金叉计数
                k2=0 #macd>0为0
                self.jinc.append(-999)
                for i in self.macd[t2:]:    #涨停第一天的dif将被作为jinc[0]
                    if i[1]>i[2] and k2==1:
                        k1+=1
                        k2=0
                        self.jinc.append(i[1])
                    elif i[1]>i[2]:
                        pass
                    else:
                        k2=1

class getjc60(macd60):
    def __init__(self,code):
        super().__init__(code)
        self.current_DIF=None
        self.current_DEA=None
    def current60(self):
        super().getmacd()
        h=time.localtime().tm_hour
        mi=time.localtime().tm_min
        if h<9 or (h==9 and mi<=30):
            return 0
        url=r'http://hq.sinajs.cn/list=%s' % self.code
        while 1:
            try:
                html=super().gethtmll(url)
                break
            except:
                continue
        html=html.split(',')
        cprice=float(html[3])
        EMA1=self.macd[-1][3]*11/13+cprice*2/13
        EMA2=self.macd[-1][4]*25/27+cprice*2/27
        self.current_DIF=round((EMA1-EMA2),3)
        self.current_DEA=round((self.macd[-1][2]*8/10+self.current_DIF*2/10),3)
    def Getjc60(self):
        self.current60()
        k=0
        c=0   #macdd列表计数
        self.d=0 #用于存储最后一个金叉在macdd列表中的位置
        macdd=self.macd
        macdd.append((999,self.current_DIF,self.current_DEA))
        self.cmacdd=len(macdd)
        self.jinc=[]
        for i in macdd:
            if i[1]>i[2] and k==1:
                k=0
                self.jinc.append(i[1])
                self.d=c
            elif i[1]>i[2]:
                pass
            else:
                k=1
            c+=1
    def comp60(self):
        self.Getjc60()
        return 1 if (self.jinc[-1]>self.jinc[-2])and(self.cmacdd-self.d<4) else 0
        #self.cmacdd-self.d<4 更改4可以控制对过时60分钟金叉的过滤

class current(getjc):   #获得当前数据并对比
    def __init__(self,code):
        super().__init__(code)
        self.current_cprice=None
        self.current_DIF=None
        self.current_DEA=None
    def current_current(self):   #计算当日指标,金叉返回1，否则0
        if len(self.macd)!=0:
            h=time.localtime().tm_hour
            mi=time.localtime().tm_min
            if h<9 or (h==9 and mi<=30):
                return 0
            url=r'http://hq.sinajs.cn/list=%s' % self.code
            while 1:
                try:
                    html=super().gethtmll(url)
                    break
                except:
                    continue
            html=html.split(',')
            self.current_cprice=float(html[3])
            EMA1=self.macd[-1][3]*11/13+self.current_cprice*2/13
            EMA2=self.macd[-1][4]*25/27+self.current_cprice*2/27
            self.current_DIF=round((EMA1-EMA2),3)
            self.current_DEA=round((self.macd[-1][2]*8/10+self.current_DIF*2/10),3)
            if self.current_DIF>self.current_DEA and self.current_DIF>self.jinc[-1] :
                return 1
            else:
                return 0
        else:
            return 0
    def DDE(self): #用于分析DDE
        gpapi=r'http://stockpage.10jqka.com.cn/spService/%s/Funds/realFunds' % self.code[2:]
        try:
            html=super().gethtmll(gpapi)
        except:
            return 0
        js=json.loads(html)
        ddlc=js['flash'][0]['sr']  #获取大单流出
        ddlr=js['flash'][5]['sr']  #获取大单流入
        jddlr=float(ddlr)-float(ddlc) 
        return 1 if jddlr>0 else 0

class comp(current):   #挑选合适的股票进行扫描
    def __init__(self,code,n=120,m=4):   #n/m见getjc_get()
        super().__init__(code)
        super().getjc_get(n,m)
        self.comp60=getjc60(code)
    def comp_comp(self,m,n):    #n为对比的金叉上限,m为金叉下限,即期望监视第m到n个金叉
        m-=1
        n-=1
        if len(self.jinc)-1<m or len(self.jinc)-1>n : return 0 #0表示不合格
        if n==0 or n==1 :return 1
        t1=0  #0表示金叉一直没有突破
        if len(self.jinc)-1>1:
            for i in range(1,len(self.jinc)-1):
                if self.jinc[i]<self.jinc[i+1]:
                    t1+=1
            return 1 if t1==0 else 0
        else:
            return 1
    def comp_compp(self,s,ss,lock,count,m=2,n=3):     #s为集合对象 #ss为显示金叉符合的集合
        result=self.comp_comp(m,n)
        if result==1 and self.macd[-1][1]<self.macd[-1][2]:
            lock.acquire()
            try:
                txt=open('stock\\list1.dat','a')
                txt.write(self.code[2:]+'\n')
                txt.close()
                ss.insert(1,self.code[2:])
                count.append(1)
            finally:
                lock.release()
            self.comp_comp2(s)
        else:
            m,n=1,1
            result=self.comp_comp(m,n)
            if result==1 and self.macd[-1][1]<self.macd[-1][2]:
                lock.acquire()
                try:
                    txt=open('stock\\list1.dat','a')
                    txt.write(self.code[2:]+'*\n')
                    txt.close()
                    ss.insert(1,self.code[2:]+'*')
                    count.append(1)
                finally:
                    lock.release()
                self.comp_comp3(s)
    def comp_comp2(self,s):    #开始循环监控当日指标
        mail_mark=0
        while 1:
            if super().current_current() and super().DDE() :
                    if mail_mark==0:
                        try:
                            mailMe(str(self.code))
                            mail_mark=1
                        except:
                            pass
                    try:
                        s.remove(self.code)
                    except:
                        s.add(self.code)
                        winsound.Beep(7000,800)
                    s.add(self.code)
            else:
                try:
                    s.remove(self.code)
                except:
                    pass
            time.sleep(10)
    def comp_comp3(self,s):
        mail_mark=0
        while 1:
            try:
                if  self.comp60.comp60()  :
                        if mail_mark==0:
                            try:
                                mailMe(str(self.code)+'*')
                                mail_mark=1
                            except:
                                pass
                        try:
                            s.remove(self.code+'*')
                        except:
                            s.add(self.code+'*')
                            winsound.Beep(7000,800)
                        s.add(self.code+'*')
                else:
                    try:
                        s.remove(self.code+'*')
                    except:
                        pass
            except:
                pass
            time.sleep(10)
            
class start(update):  #启动多线程
    def __init__(self,s,ss,lock,count,m=0,n=2):   #m=0则启动list内股票，m=1则启动listR内的股票
        super().__init__(n)             #n为更新天数
        self.start_m=m
        self.start_s=s    #s为集合 用于表述目前提示的股票
        self.start_ss=ss    #ss为tk.listbox对象 用于表述符合金叉的股票
        self.lock=lock
        self.count=count
    def __aa(self,a,b,c,d,e):    #启动完全扫描时调用
        a=comp(a)
        a.comp_compp(b,c,d,e)
    def __aaa(self,a,b,c,d):       #启动直接扫描时调用
        c.insert(1,a)
        d.append(1)
        aa=comp(a)
        if a[-1]!='*':
            aa.comp_comp2(b)
        else:
            aa.comp_comp3(b)
    def start_list(self):
        super().get()
        t=[]
        for i in open('stock\\list.dat','r'):
            i=i.strip()
            if i:
                t1=threading.Thread(target=self.__aa,args=(i,self.start_s,self.start_ss,self.lock,self.count))
                t.append(t1)
        for i in t:
            while threading.activeCount()>50 :
                time.sleep(1)
            try:
                i.setDaemon(True)
                i.start()
            except:
                continue
    def start_list1(self):
        t=[]
        for i in open('stock\\list1.dat','r'):
            i=i.strip()
            if i:
                t1=threading.Thread(target=self.__aaa,args=(i,self.start_s,self.start_ss,self.count))
                t.append(t1)
        for i in t:
            while threading.activeCount()>100 :
                time.sleep(1)
            try:
                i.setDaemon(True)
                i.start()
            except:
                continue
    def start(self):
        if self.start_m==0:
            txt=open('stock\\list1.dat','w')
            txt.close()
            self.start_list()
        else:
            self.start_list1()

def mailMe(text): #用于发送邮件
    sender = 'fdrv@163.com'   #发送邮箱
    receiver = 'soar3033@163.com'  #接收邮箱
    subject = '股票代码'  #邮件名称
    smtpserver = 'smtp.163.com'  #邮件服务器  
    username = 'fdrv'   #发送邮箱的账号
    password = '88292145369'  #发送邮箱的密码
    #MIMEText的第一项为发送内容
    msg = MIMEText(text,'plain','utf-8')#中文需参数‘utf-8'，单字节字符不需要  
    msg['Subject'] = Header(subject, 'utf-8')  
    msg['From'] = 'fdrv<fdrv@163.com>'    #发送方名称，必须满足格式！！！
    msg['To'] = "soar3033"  #接受方名称，可以随便起
    smtp = smtplib.SMTP()  
    smtp.connect('smtp.163.com')  
    smtp.login(username, password)  
    smtp.sendmail(sender, receiver, msg.as_string())  
    smtp.quit()



class inter():
    def __init__(self):
        self.lock=threading.Lock()   #线程锁
        self.count=[]   #扫描股票数计数
        self.s=set()   #存储目前合适的股票的集合
        self.alls=set()   #存储所有合适过的股票的集合
        self.w=tkinter.Tk()
        self.w.title('Stock')
        self.w.geometry('340x300')
        self.w.iconbitmap('stock\\1.ico')
        #Frame
        self.fr0=tkinter.Frame(self.w,width=10,height=25)
        self.fr1=tkinter.Frame(self.w,width=10,height=25)
        self.fr2=tkinter.Frame(self.w,width=10,height=25)
        #Listbox
        self.li11=tkinter.Listbox(self.fr1)
        self.li12=tkinter.Listbox(self.fr1)
        self.li21=tkinter.Listbox(self.fr2,height=30)
        #Button
        self.bu01=tkinter.Button(self.fr0,text='完整扫描',command=lambda :self.inter_start(0)).pack()
        self.bu02=tkinter.Button(self.fr0,text='直接扫描',command=lambda :self.inter_start(1)).pack()
        #pack
        self.fr0.pack(side=tkinter.LEFT)
        self.fr1.pack(side=tkinter.LEFT)
        self.fr2.pack(side=tkinter.LEFT)
        self.li11.pack()
        self.li12.pack()
        self.li21.pack(side=tkinter.TOP)
        #mainloop
        self.w.mainloop()
    def inter_thread(self,m):
        c_start=start(self.s,self.li12,self.lock,self.count,m)
        c_start.start()
    def inter_while(self):
        self.li11.insert(0,'符合的股票：')
        self.li12.insert(0,'0个股票扫描中：')
        self.li21.insert(0,'符合过的股票：')
        k=0
        while 1:
            self.alls.update(self.s)
            self.li21.delete(1,30)
            for i in self.alls:
                self.li21.insert(1,i)
            self.li11.delete(1,20)
            for i in self.s:
                self.li11.insert(1,i)
            self.lock.acquire()
            try:
                self.li12.delete(0)
                if k==0:
                    self.li12.insert(0,'%d个股票扫描中' % len(self.count))
                    k=1
                else:
                    self.li12.insert(0,'%d个股票扫描中*' % len(self.count))
                    k=0
            finally:
                self.lock.release()
            time.sleep(1)
    def inter_start(self,m):
        self.fr0.pack_forget()
        self.w.geometry('280x300')
        t=[]
        t2=threading.Thread(target=self.inter_while,)
        t.append(t2)        
        t1=threading.Thread(target=self.inter_thread,args=(m,))
        t.append(t1)
        for i in t:
            i.setDaemon(True)
            i.start()

if __name__=='__main__':
    a=inter()
    exit()

