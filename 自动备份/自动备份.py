import os

class backup():
    def __init__(self):
        self.path1=None
        self.path2=None
        self.lp1=0
        self.count=0
        self.paths=None
        self.state=1
        
    def allpath(self):
        try:
            with open('config.ini','r') as f:
                txt=f.read()
                self.paths=txt.split('\n')     
        except Exception as err:
            print(err)
        
    def getpath(self):
        while 1:
            try:
                if self.paths[0][0]!='#':   
                    self.path1=self.paths[0]
                    del(self.paths[0])
                    self.path2=self.paths[0]
                    self.lp1=len(self.path1)
                    del(self.paths[0])
                    break
            except:
                self.state=0
                break
            del(self.paths[0])
        
    def backup(self,md):
        if os.path.isfile(md):
            path2=self.path2+md[self.lp1:]
            if not os.path.exists(path2):
                cmd='copy "'+md+'" "'+path2+'"'
                res=os.popen(cmd,mode='w')
                print(cmd)
        elif os.listdir(md):
            if len(md)==self.lp1:
                path2=self.path2
            else:
                path2=self.path2 +md[self.lp1:]
            if not os.path.exists(path2):
                os.mkdir(path2)
            for i in os.listdir(md):
                self.backup(os.path.join(md,i))
                
    def start(self):
        while self.state:
            self.getpath()
            self.backup(self.path1)
   
if __name__=='__main__':
    a=backup()
    a.allpath()
    a.start()
    os.popen('pause')



