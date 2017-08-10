from Stock import current
import threading,sys,time

def rash(code):
    a=current(code)
    a.getmacd()
    dif=[]
    mark=0
    gold_per=0.07
    dead_per=gold_per
    mix_per=0.02
    t1=0
    i1=0
    jl=len(a.js)
    if jl==0:
        sys.exit()
    for i in a.js[-120:]:
        if float(i[7])>9.8:
            t1+=1
        else:
            t1=0
        if t1==4:
            break
        i1+=1
    if jl<120:
        jl=jl-i1
    else:
        jl=120-i1
    if t1==4:
        for i in a.macd[-jl:]:
            dif.append(i[1])
        try:
            dif_max=max(dif)
        except:
            sys.exit()
        dif_min=min(dif)
        dif_range=dif_max-dif_min
        jc=0
        for i in a.macd[-jl:]:
            if i[1]>i[2]+gold_per*dif_range:
                if mark==0:
                    jc+=1
                mark=1
            elif i[1]+dead_per*dif_range<i[2]:
                mark=0
        if jc==2 and mark==1 and abs(a.macd[-1][1]-a.macd[-1][2])<mix_per*dif_range:
            print(code)
            while 1:
                try:
                    a.current_current()
                except:
                    pass
                try:
                    if a.current_DIF>a.current_DEA:
                        print(code)
                        break
                except:
                    break
def start_rash():
    for i in open(r'stock\list.dat','r'):
        i=i.strip('\n')
        t=threading.Thread(target=rash,args=(i,))
        t.setDaemon(True)
        try:
            t.start()
        except:
            pass
    while 1:
        time.sleep(3)

if __name__=='__main__':
    start_rash()
