import socket
import gzip

ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.connect(('127.0.0.1',6000))
ss.send(bytes([2]))
msg=ss.recv(10240)
while 1:
    rec=ss.recv(10240)
    if len(rec)==0:
        break
    msg+=rec
txt=open('2.jpg','wb')
msg=gzip.decompress(msg)
txt.write(msg)
txt.close()
ss.close()
 
