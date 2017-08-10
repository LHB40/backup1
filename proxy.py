import socket
import threading
import urllib.parse
import sys
import time



def proxy(conn):
    try:
        conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket.setdefaulttimeout(2)
        rec=conn.recv(4096)
        if rec==b'':
            conn.close()
            sys.exit()
        recc=rec.split()[1] 
        url=urllib.parse.urlparse(recc)[1]
        if url==b'':
            url=urllib.parse.urlparse(recc)[2]
        f=url.find(b':')
        if f>0:
            host=url[:f]
            port=url[f+1:]
        else:
            host=url
            port=80
        port=int(port)
        print(host.decode('ascii'),port)
        url=socket.gethostbyname(host)
        sss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            sss.connect((url,port))
        except:
            print(host.decode('ascii'),'error\r\n')
            sys.exit()
        sss.send(rec)
        while 1:
            try:
                rec1=sss.recv(10240)
            except:
                break
            conn.send(rec1)
            if rec1==b'':
                break
        conn.close()
        sss.close()
        sys.exit()
    except Exception as e:
        print(e)
        sys.exit()
        
def count():
    while 1:
        print(threading.active_count())
        time.sleep(2)
        
#threading.Thread(target=count,).start()
ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ss.bind(('127.0.0.1',6000))
ss.listen(100)
print('listening 127.0.0.1:6000')
while 1:
    conn,add=ss.accept()
    threading.Thread(target=proxy,args=(conn,)).start()

