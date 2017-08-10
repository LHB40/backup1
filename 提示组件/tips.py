import win32api,win32gui
import tkinter as tk
import time
import threading as th
import xlrd,sys

def getpos():
    return win32api.GetCursorPos()
        
def getwl():
    return (win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1))

class window():
    def __init__(self):
        self.w=tk.Tk()
        self.w.resizable(False,False)
        self.w.overrideredirect(True)
        self.w.title('提示')
        width,height=getwl()
        self.wwidth=300
        self.wheight=150
        self.w.geometry('%dx%d+%d+%d' % (self.wwidth,self.wheight,width-\
                                         self.wwidth,(height-self.wheight)/2))
        self.li=tk.Listbox(self.w)
        self.li.pack(fill=tk.BOTH)
        self.w1=tk.Tk()
        self.w1.resizable(False,False)
        self.w1.overrideredirect(True)
        self.w1.title('提示')
        width1,height1=getwl()
        self.wwidth1=5
        self.wheight1=150
        self.w1.geometry('%dx%d+%d+%d' % (self.wwidth1,self.wheight1,width1-\
                                         self.wwidth1,(height1-self.wheight1)/2))
    def show(self):
        self.w.update()
        self.w.deiconify()

    def hide(self):
        self.w.withdraw()

    def rd(self,name):       #获得xlsx内容
        xl=xlrd.open_workbook(name)
        xl=xl.sheets()[0]
        for i in range(2,xl.nrows):
            if (xl.cell(i,19).value=='N' or xl.cell(i,19).value=='n') and xl.cell(i,12).value!='':
                a=(xl.cell(i,0).value,xl.cell(i,12).value,xl.cell(i,2).value,xl.cell(i,3).value,xl.cell(i,5).value,xl.cell(i,11).value)
                yield a
                   
    def tm(self):       #获得当前时间
        return time.strftime('%Y%m%d',time.localtime())

    def th(self):
        lis=[]
        t=self.tm() #今日时间
        t1=str(t[:-2])   #本月时间
        t2=str(t[-2:])  #今日日期
        for i in self.rd('1.xlsx'):
            if str(int(i[1]))[:-2]==t1 and int(str(int(i[1]))[-2:])>=int(t2):
                lis.append(('%2d天到期' %(int(i[1])-int(t)),str(i[4])+' ： '+str(i[3])+' ： '+str(i[2])+' ： '+str(i[0])))
        lis.sort()
        for i in lis[::-1]:
            self.li.insert(0,i[0]+' ： '+i[1])
            
def ww(w):
    width,height=getwl()
    show=0
    try:
        while 1:
            if getpos()[0]>=width-10 and (getpos()[1]>=(height-w.wheight)/2 \
                                          and getpos()[1]<=(height+w.wheight)/2)and show==0:
                w.show()
                show=1
            elif (getpos()[0]<width-w.wwidth or\
                  (getpos()[1]<(height-w.wheight)/2 or getpos()[1]> (height+w.wheight)/2)) and show==1: 
                w.hide()
                show=0
            time.sleep(0.2)
    except:
        pass

if __name__=='__main__':
    w=window()
    t=th.Thread(target=ww,args=(w,))
    t.setDaemon(True)
    t.start()
    w.hide()
    w.th()
    w.w.mainloop()

    
