import os
os.system('title gao')
from urllib.request import urlopen
from urllib.request import Request
import re
import os



def html(url):
    header={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
    req=Request(url)
    return urlopen(req).read()

def png(data,i=0):
    with open('%d.png' % i,'wb') as txt:
        txt.write(data)
        
#url=r'https://wenku.baidu.com/view/7dd7dfbe8bd63186bcebbc8b.html'
url=input(r'输入要破解的文库地址：')

res=html(url).decode('gbk')

#print(res)
try:
    root=re.findall(r'wkbos.bdimg.com(.+?)0\.json\?response',res)[0]
    root=root.replace(r'\\\/',r'/')
    root=r'https://wkbos.bdimg.com'+root+r'0.png'
except:
    root=re.findall(r'wkbjbos.bdimg.com(.+?)0\.json\?response',res)[0]
    root=root.replace(r'\\\/',r'/')
    root=r'https://wkbjbos.bdimg.com'+root+r'0.png'

result=re.findall(r'0.png?(.+?)\\x22}',res)
result=[root+i for i in result]

for i in range(int(len(result)/2)):
    png(html(result[i]),i)
