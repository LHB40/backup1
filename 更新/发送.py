import socket
import gzip

ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(('127.0.0.1',6000))
ss.listen(5)
while 1:
    conn,add=ss.accept()
    try:
        rec=conn.recv(1024)
        if rec==bytes([2]):
            txt=open('1.jpg','rb').read()
            txt=gzip.compress(txt)
            conn.send(txt)
    finally:
        conn.close()          
ss.close()
