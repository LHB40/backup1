

target=input("")
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
    
