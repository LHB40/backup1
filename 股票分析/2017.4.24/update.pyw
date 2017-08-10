import poplib
from email import parser

p=poplib.POP3('pop.163.com')    #设置pop3连接对象
p.user('soar3033@163.com')          #登陆id
ps='gf8829'+'2145'+'369'
p.pass_(ps)       #密码
lis=p.list()[1]         #获得邮件列表
lislen=len(lis)         #获得邮件数量
recs=[p.retr(i)[1] for i in range(1,lislen+1)]      #获得邮件，存于元组
recs=[b'\n'.join(rec) for rec in recs]              #将各个邮件的内容用'\n'连接
                                                    #由于邮件内容为二进制，故'\n'
                                                    #前加b
recs=[rec.decode('utf-8') for rec in recs]      #将邮件内容由二进制转为字符
msgs=[parser.Parser().parsestr(rec) for rec in recs]        #邮件内容转化为邮件对象
def msg(msgs,name):
    maillist=[]
    for msg in msgs:        #遍历每个邮件对象
        for i in msg.walk():        #遍历单个邮件的每一行
            ff=i.get_filename()     #查询行内是否有文件名
            if ff==name:                  #如果有
                data=i.get_payload(decode=True)     #获得文件内容并存至data
                maillist.append((ff,data))      #返回文件名和文件内容
    return maillist
def msg2(msgs):    #打印文件正文↓
    for msg in msgs:    
        for i in msg.walk():
                contentType = i.get_content_type()
                if contentType == 'text/plain' or contentType == 'text/html':
                        data = i.get_payload(decode=True)
                        d=data.decode('utf-8')
                        print(d)
def update(name):
    ms=msg(msgs,name)
    if len(ms)!=0:
        conten=ms[len(ms)-1][1]
        txt=open(name,'wb')
        txt.write(conten)
        txt.close()
    #msg2(msgs)
                        
if __name__=='__main__':
    update('Stock.pyw')
