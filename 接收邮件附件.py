import poplib
from email import parser

p=poplib.POP3('pop.163.com')    #设置pop3连接对象
p.user('@163.com')          #登陆id
p.pass_('')       #密码
lis=p.list()[1]         #获得邮件列表
lislen=len(lis)         #获得邮件数量
recs=[p.retr(i)[1] for i in range(1,lislen+1)]      #获得邮件，存于元组
recs=[b'\n'.join(rec) for rec in recs]              #将各个邮件的内容用'\n'连接
                                                    #由于邮件内容为二进制，故'\n'
                                                    #前加b
recs=[rec.decode('utf-8') for rec in recs]      #将邮件内容由二进制转为字符
msgs=[parser.Parser().parsestr(rec) for rec in recs]        #邮件内容转化为邮件对象
def msg(msgs):      
    for msg in msgs:        #遍历每个邮件对象
        for i in msg.walk():        #遍历单个邮件的每一行
            ff=i.get_filename()     #查询行内是否有文件名
            if ff:                  #如果有
                data=i.get_payload(decode=True)     #获得文件内容并存至data
                yield(ff,data)      #返回文件名和文件内容
ms=msg(msgs)
for i in ms:
    print(i[0])

#打印文件正文↓    
for i in msg.walk():
	contentType = i.get_content_type()
	if contentType == 'text/plain' or contentType == 'text/html':
		data = i.get_payload(decode=True)
		d=data.decode('gbk')
		print(d)
