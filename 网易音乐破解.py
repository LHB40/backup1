import os

def crash(target):
    txt1=open(target,'rb')
    name=target.split('.')[:-1]
    name=".".join(name)
    name+='.mp3'
    txt2=open(name,'wb')
    key=163
    for i in txt1.read():
        i=bytes([i^key])
        txt2.write(i)
    txt1.close()
    txt2.flush()
    txt2.close()
    print('finish')

while 1:
    try:
        target=input("")
        if target!='1':  
            crash(target)
        else:
            cwd=os.getcwd()
            for i,j,k in os.walk(cwd):
                print(k)
                print(len(k))
                ta=k
            for i in ta:
                if i.split('.')=='uc':
                    crash(i)
        print('all finish')
    except Exception as err:
        print(err)
    
