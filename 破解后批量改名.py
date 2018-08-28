import os

def pj(path):
    for i,j,k in os.walk(path):
        for n in j:
            aa=path+n+'\\'
            pj(aa)
            
        for m in k:
            try:
                print(path+"\\"+m,path+'\\'+'.'.join(m.split('.')[:-1]))
                os.rename(path+"\\"+m,path+'\\'+'.'.join(m.split('.')[:-1]))
            except:
                pass

path=input(r'输入文件夹路径：')
if path[-2:]==r'\\':
    pj(path)
elif path[-1]=='\\':
    pj(path)
else:
    path+=r'\\'
    pj(path)
