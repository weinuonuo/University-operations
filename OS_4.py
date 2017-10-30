import re
import random
import time
import math

def Init():     #初始化
    global MyFAT,root,NowFile
    bsize = input("请输入块大小")
    bnum = input("请输入块个数")
    MyFAT = FAT(int(bnum),int(bsize)) # FAT表初始化
    root = FileDirectory(None,"root")
    NowFile = root

class FileDirectory(object):    #目录
    def __init__(self,father,name):
        self.name = name
        self.father = father
        self.filelist = ['.','..'] # 目录表
        self.fcb = FCB(self.name,1,2) # 自动创建fcb
        

class File(object):
    def __init__(self,name,size):
        self.name = name
        self.size = size
        self.fcb = FCB(self.name,size,1)
        
    
class FAT(object):
    def __init__(self,num,bsize):
        self.bsize = bsize # 每块的大小
        # self.table = [0 for i in range(num)] # 0为空，-1为结束
        self.content = [] # 文件的具体内容
        self.StationView = [random.randint(0,1) for i in range(64)]# 初始化位视图
        self.table = self.__init_table()
        # print(self.table)

    def __init_table(self):
        temp = self.StationView.copy()
        # print(self.StationView)
        for index,i in enumerate(temp):
            if i == 1:
                temp[index] = -1
        return temp

    def _init_table_(self,size):
        if type(size) is int: #如果是文件
            for index,i in enumerate(self.table):
                if index == size:
                    self.table[index] = -1
                    # print(self.table)
                    return
            else:
                print("FAT已满")
        elif type(size) is list:
            if len(size) == 1:#如果一个块可以放下
                for index,i in enumerate(self.table):
                    if index == size[0]:
                        self.table[index] = -1
                        # print(self.table)
                        return
            else :
                for i in size[1:]:
                    for index,j in enumerate(self.table):
                        if j == 0:
                            self.table[index] = i
                            break
                for index,k in enumerate(self.table):
                        if k == 0:
                            self.table[index] = -1
                            break
class FCB(object): #文件控制快
    global MyFAT
    def __init__(self, name,fsize,ftype):
        self.name = name # 文件名
        self.fsize = fsize # 文件大小
        self.ftype = ftype # 1为文件，2为目录，0为已删除目录
        self.first_block = self.__init_block_()
        self.datatime = self.__init_time_() # 初始化创建时间

    def __init_block_(self):
        if self.ftype == 2:
            for index,i in enumerate(MyFAT.StationView):
                if i == 0:
                    MyFAT.StationView[index] = 1
                    MyFAT._init_table_(index)
                    return index
        elif self.ftype == 1:
            num = math.ceil(self.fsize/1024)
            size = []
            for index,i in enumerate(MyFAT.StationView):
                if num == 0:
                    MyFAT._init_table_(size)
                    return size[0]
                if i == 0:
                    size.append(index)
                    MyFAT.StationView[index] = 1
                    num -= 1

    def __init_time_(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
 
def MakeDir(name):
    global MyFAT,NowFile
    newfile = FileDirectory(NowFile,name[0]) # 初始化目录
    NowFile.filelist.append(newfile) # 在父目录中加入
    MyFAT.content.append(newfile) # 将目录放入FAT中
    
def ChangDir(command):
    global NowFile
    if command[0] == NowFile.filelist[0]:
        print("返回当前目录")
        return
    elif command[0] == NowFile.filelist[1]:
        print("返回上一层目录") 
        NowFile = NowFile.father  
        return     
    for file in NowFile.filelist[2:]:
        if command[0] == file.name:
            NowFile = file
            return
    else:
        print("当前目录下无此子目录")

def RemoveDir(command):
    global NowFile
    for file in NowFile.filelist:
        if type(file) is FileDirectory:
            if file.name == command[0]:
                if len(file.filelist) == 2: # 如果是空目录
                    MyFAT.StationView[file.fcb.first_block] = 0
                    MyFAT.table[file.fcb.first_block] = 0 #将FAT表还原
                    NowFile.filelist.remove(file) #从当前父目录下移除
                    return
                else:
                    print("当前目录不为空，无法删除")
                    return
    else:
        print("目录不存在")
        return

def Make(command):
    global NowFile
    newfile = File(command[0],int(command[1])) # 创建新的文件对象
    NowFile.filelist.append(newfile) # 在父目录中添加文件对象
    MyFAT.content.append(newfile) 


def Delete(command):
    global NowFile
    for file in NowFile.filelist:
        if type(file) == File:
            if file.name == command[0]:
                if file.size <= MyFAT.bsize:
                    NowFile.filelist.remove(file)
                    temp1 = MyFAT.table[file.fcb.first_block]
                    MyFAT.table[file.fcb.first_block] = 0
                    while temp1 != -1:
                        temp = temp1
                        temp1 = MyFAT.table[temp]
                        MyFAT.table[temp] = 0
                    MyFAT.StationView[file.fcb.first_block-1] = 0
                return
    else:
        print("当前目录下无该文件")
        return

def Dir():
    global NowFile
    for file in NowFile.filelist:
        if file == '.' or file == '..':
            print(file)
        else:
            print(file.fcb.datatime + "  " + file.name)

def PrintTree(root,level):
    # global root
    for file in root.filelist:
        if file == '.' or file == '..':
            continue
        else :
            if type(file) is File:
                indent = '| ' * 1 * level + '|____'
                print(indent + file.name+".file")
            if type(file) is FileDirectory:
                indent = '| ' * 1 * level + '|____'
                level += 1
                print(indent+file.name)
                PrintTree(file,level)
                level -= 1

def main():
    global NowFile,root,MyFAT
    for index,i in enumerate(MyFAT.StationView):
        if index % 8 == 0:
            print()
        print(i,end = "  ") 
    print()
    print("FAT")

    for index,i in enumerate(MyFAT.table):
        if index % 8 == 0:
            print()
        if i == 0:
            print(" "+ str(i),end = "  ")
        else:
            print(i,end = "  ")
            
    print()
    print(NowFile.name,end = '')
    command = input("$").split(" ")
    command_dic = {
        "md" : MakeDir
        ,"cd" : ChangDir
        ,"rd" : RemoveDir
        ,"mk" : Make
        ,"del": Delete
        ,"dir" : Dir
        ,"tree" : PrintTree
    }
    if command[0] in command_dic:
        if command[0] == "tree":
            command_dic[command[0]](root,1)
        elif command[1:]:
            command_dic[command[0]](command[1:])
        else:
            command_dic[command[0]]()
        
    else:
        print("该命令不存在，请重新输入")
        return
        

if __name__ == '__main__':
    Init()
    while True:
        main()
