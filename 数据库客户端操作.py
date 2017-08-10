import socket
from win32com.client import Dispatch
#conn=Dispatch('ADODB.Connection')
#rec=Dispatch('ADODB.Recordset')
#conn.Open (r"Provider=Microsoft.Ace.OleDB.12.0;data Source=e:\工作管理.accdb;Jet OLEDB:Database Password=882921" )
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()
port=6000
#s.bind((host,port))
#s.listen(1)
s.connect((host,port))
while 1:
    #netconn,addr=s.accept()
    #print('accpet connection')
    #try:
    #    while 1:
    #        netinput=netconn.recv(1024).decode('utf-8')
    #        rec.Open(netinput,conn)
    #        for x in rec.fields:
    #            netconn.send(x.value.encode('utf-8'))
    #        msg=r'发送完毕'
    #        print(msg)
    #        netconn.send(msg.encode('utf-8'))
    #except:
    #    msg=r'发生错误'
    #    print(msg)
    #    netconn.send(msg.encode('utf-8'))
    msg=input(r'输入SQL操作')
    s.send(msg.encode('utf-8'))
    while 1:
        inmsg=s.recv(1024).decode('utf-8')
        print(inmsg)
        
