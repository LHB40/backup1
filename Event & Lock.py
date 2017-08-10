import time,threading
from threading import Thread as tr

lock=threading.Lock()
event=threading.Event()

def aa():
    event.wait()
    for i in range(0,10):
        lock.acquire()
        print(i)
        lock.release()
        time.sleep(1)
def bb():
    event.wait()
    for i in range(10,20):
        lock.acquire()
        print(i)
        lock.release()
        time.sleep(1)
def cc():
    time.sleep(4)
    print(t2.name)
    event.set()
t=[]
t1=tr(target=aa,name='aa')
t2=tr(target=bb,name='bb')
t3=tr(target=cc)
t.append(t1)
t.append(t2)
t.append(t3)
for i in t:
    i.start()
        
