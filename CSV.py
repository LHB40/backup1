import urllib.request
import json
import time
import socket
import os

socket.setdefaulttimeout(6) #设置超时

def getHtml(url):  #用于读取连接内容
    page = urllib.request.urlopen(url)
    html = page.read()
    return html

def CSV(gupiaoapi):
    sPrice=[]
    sd=[]
    gpapi=r"http://ichart.yahoo.com/table.csv?s="+ str(gupiaoapi) +r".SZ&a=01&b=01&c=2000&d=01&e=31&f=2017&g=d"
    html=getHtml(gpapi)
    try:
        html=html.decode("utf-8")
    except:
        html=gzip.decompress(html).decode('utf-8')
    fname=r'PriceList\ ' + str(gupiaoapi) +'.dat'
    doc=open(fname,'w')
    doc.write(html)
    doc.close()
    doc=open(fname,'r')
    txtln=doc.readline()
    while 1:
        txtln=doc.readline()
        if not txtln:
            break
        txtln=txtln.split(',')
        sPrice.append(txtln[4])
        sd.append(txtln[0])
    doc.close()
    #return sPrice

    lenp=len(sPrice)
    DIF=DEA=0
    EMA1=EMA2=21.8
    for j in range(0,lenp):
        fPrice=float(sPrice[lenp-j-1])
        EMA1=EMA1*11/13+fPrice*2/13
        EMA2=EMA2*25/27+fPrice*2/27
        EMA1=round(EMA1,2)
        EMA2=round(EMA2,2)
        DIF=round((EMA1-EMA2),2)
        DEA=round((DEA*8/10+DIF*2/10),2)


        print(sd[lenp-j-1]+str(DIF)+'   '+str(DEA)+'\n')
  

CSV(300308)
