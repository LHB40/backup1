import socket
from win32com.client import Dispatch
conn=Dispatch('ADODB.Connection')
rec=Dispatch('ADODB.Recordset')
conn.Open (r"Provider=Microsoft.Ace.OleDB.12.0;data Source=e:\工作管理.accdb;Jet OLEDB:Database Password=882921" )
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()
port=6000
s.bind((host,port))
s.listen(1)
while 1:
    netconn,addr=s.accept()
    print('accpet connection')
    try:
         while 1:
            aa=netconn.recv(1024)
            aa=aa.decode('utf-8')
            aa=r'select * from 量具管理'
            rec.Open(aa,conn)
            while rec.eof==0 :
                for x in rec.fields:
                    bb=str(x.value)
                    netconn.send(bb.encode('utf-8'))
                rec.movenext
            msg='发送完毕'
            print(msg)
            netconn.send(msg.encode('utf-8'))
    except:
        msg=r'发生错误'
        print(msg)
        netconn.send(msg.encode('utf-8'))
        
