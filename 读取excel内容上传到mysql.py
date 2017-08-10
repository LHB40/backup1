import xlrd
import pymysql

conn=pymysql.connect(host='127.0.0.1',user='root',password='88292145369',db='soar')
cu=conn.cursor()
xl=xlrd.open_workbook(r'f:\1.xlsx') #打开excel文件
sh=xl.sheets()[0]   #打开第一个表
tx=[]
for i in range(1,sh.nrows):   #按行遍历
    a=[]
    for j in range(1,10):    #按列遍历
        if j!=9:
            a.append('"'+str(sh.cell(i,j).value)+'"')
        else:
            a.append(int(sh.cell(i,j).value))
    tx.append(a)
for i in tx:   #遍历excel读出的内容
    i=[str(ii) for ii in i]   #为变量赋值，然后调用sql语句
    i=','.join(i)
    cu.execute('insert into t1(name,code,original_code,type,made_by,location,user,note,mouth) values(%s)' % i)
    conn.commit()    #提交修改
cu.close()
conn.close()
