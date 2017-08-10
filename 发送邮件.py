import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  

def mailMe(text):
    sender = 'fdrv@163.com'   #发送邮箱
    receiver = 'soar3033@163.com'  #接收邮箱
    subject = '邮件测试'  #邮件名称
    smtpserver = 'smtp.163.com'  #邮件服务器  
    username = 'fdrv'   #发送邮箱的账号
    password = '88292145369'  #发送邮箱的密码
    #MIMEText的第一项为发送内容
    msg = MIMEText(text,'plain','utf-8')#中文需参数‘utf-8'，单字节字符不需要  
    msg['Subject'] = Header(subject, 'utf-8')  
    msg['From'] = 'fdrv<fdrv@163.com>'    #发送方名称，必须满足格式！！！
                                          #fdrv可以随便改，后方邮件地址不可以
    msg['To'] = "soar3033"  #接受方名称，可以随便起
    smtp = smtplib.SMTP()  
    smtp.connect('smtp.163.com')  
    smtp.login(username, password)  
    smtp.sendmail(sender, receiver, msg.as_string())  
    smtp.quit()  

mailMe('aaa')
