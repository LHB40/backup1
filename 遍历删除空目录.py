import os

def aa(md):
    if os.path.isfile(md):
        pass
    else:
        if not os.listdir(md):
            print(md)
            #os.remove(md)
        else:
            for i in os.listdir(md):
                ff=os.path.join(md,i)
                aa(ff)


aa(r'C:\Users\gftv.DESKTOP-CH8PN4N\Desktop\新建文件夹')
    
