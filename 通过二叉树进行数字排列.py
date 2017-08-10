import random

class aa():                       #二叉树类
    def __init__(self,code):
        self.value=code
        self.left=None
        self.right=None
    def addLeft(self,code):      #为二叉树添加左侧子项
        self.left=aa(code)
    def addRight(self,code):     #为二叉树添加右侧子项
        self.right=aa(code)

def comp(value,code):      #将数字在二叉树中进行排列
    if code>value.value:
        if value.right==None:
            value.addRight(code)
        else:
            comp(value.right,code)
    else:
        if value.left==None:
            value.addLeft(code)
        else:
            comp(value.left,code)      

def pr(root):               #将二叉树里排列好的数字读出
    if root.left!=None:
        pr(root.left)
    print(root.value)
    if root.right!=None:
        pr(root.right)

lis=set()       #随机产生数字添加到集合中
for i in range(100):
    lis.add(int(random.randint(0,100)))

li=[]           #将集合转化为列表
for i in lis:
    li.append(i)

root=aa(li[0])  #调用comp方法将数字在二叉树中进行排列
for i in li[1:]:
    comp(root,i)
    
pr(root)        #调用pr方法将二叉树内的数字读出
print('root len is %d' % len(li))   #输出集合的长度
