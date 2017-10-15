import numpy
import math
from Window import *

Table = [] # 页顺序
Page = ''
class PageTable(object):    #页表
    def __init__(self,PageNum):#页号
        self.PageNum = [i for i in range(0,PageNum)] #页号
        self.PhysicalBlock = [-1 for i in range(0,PageNum)] #物理块号初始化都为空
        self.StateStation = [False for i in range(0,PageNum)] #状态位初始化都为False

    def getStateStation(self,PageNum):
        return self.StateStation[PageNum]
    
    def getPhysicalBlock(self,PageNum):
        return self.PhysicalBlock[PageNum]

class MEMORY(object): # 内存
    def __init__(self,size):
        self.Station = [] # 物理块号
        self.Page = [-1 for i in range(0,size)] # 页号
    
    def getStation(self,Num):
        return self.Station[Num]
    
    def getPage(self,Num):
        return self.Page[Num]

class REPLACE(object): # 置换
    def __init__(self,ReplaceView):
        self.Block = []
        self.Page_Num = []
        self._initView_(ReplaceView)

    def _initView_(self,ReplaceView):
        for index,i in enumerate(ReplaceView.flat):
            if i == 0:
                self.Block.append(index)       
        
def InstallStationView(Ran_Size, Chunk_Size):   #初始化位视图
    size = int((Ran_Size/Chunk_Size)/8)
    StationView = numpy.random.randint(0,2,(size,8))
    ReplaceView = numpy.random.randint(0,2,(size*2,8))
    return StationView,ReplaceView

def ApplyForStationView(Memory_Size,StationView,Memory):  #申请位视图
    temp = 1
    for index,i in enumerate(StationView.flat):
        if temp > Memory_Size:
            break
        if i == 0:
            Memory.Station.append(index) #为进程申请内存块
            # StationView[int(index/8)][index%8] = 1;
            temp += 1
    else:
        print("内存不够")   

def EndProgress():  #终止进程，位视图反向为0
    for i in Memory.Station:
        StationView[int(i/8)][i%8] = 0

def FIFO(page,List,Page,Replace,ReplaceView): #FIFO置换
    oldPage = List.pop(0) #删除顶页
    List.append(page) #将新页加入
    Page.PhysicalBlock[page] = Page.getPhysicalBlock(oldPage) #更新页表
    Page.PhysicalBlock[oldPage] = 0
    Page.StateStation[page] = True
    Page.StateStation[oldPage] = False
    Replace.Page_Num.append(oldPage) # 将置换出的页加入置换空间
    num = Replace.Block[len(Replace.Page_Num)-1]
    ReplaceView[int(num/8)][num%8] = 1      #将置换空间的位视图置1

def PageSetUp(page,List):
    List.remove(page)
    List.append(page)
    
def AddressConvert(Time,LogicAddress,Chunk,Replace,Page,Memory,List,StationView,ReplaceView,algor,Table): # 地址转换
    page_num = int(LogicAddress,16)//(Chunk*1024) # 页号
    Table.append(page_num) # 记录页面访问顺序
    if page_num >= len(Page.PageNum): # 页号大于页表长度
        print('发生越界')
        return False
    if not Page.getStateStation(page_num): # 页不在内存
        Time += 1 # 缺页次数加1sss
        for index,page in enumerate(Replace.Page_Num):
            if page == page_num:
                num = Replace.Block[index]
                ReplaceView[int(num/8)][num%8] = 0
                Replace.Page_Num.remove(page)
        for index,i in enumerate(Memory.Page):
            if i == -1:
                PageExecutive(page_num,index,Memory,StationView,Page,List) #将进程调入内存
                break
        else:
            FIFO(page_num,List,Page,Replace,ReplaceView)
    else:
        print('命中')
        if algor == 'LRU':
            PageSetUp(page_num,List) #将命中页面置顶
    pagein_add = int(LogicAddress,16)%(Chunk*1024) # 页内地址
    PhysicalAdd = hex(Page.getPhysicalBlock(page_num)*(Chunk*1024)+pagein_add) #物理地址
    return Time,PhysicalAdd

def PageExecutive(page_num,index,Memory,StationView,Page,List):   # 进程调度
    PhyBlock = Memory.getStation(index)
    Memory.Page[index] = page_num
    StationView[int(PhyBlock/8)][PhyBlock%8] = 1
    Page.PhysicalBlock[page_num] = PhyBlock # 标注物理块号
    Page.StateStation[page_num] = True # 状态位置True
    List.append(page_num)

def Opt(Table,Memory_Size):
    List = []
    temp = 1;Max = -1;ind = 0;time = 0 #
    for i,page in enumerate(Table):
        print(List)
        if page in List:
            print('命中')
            continue
        else:
            if temp > Memory_Size:
                Max = -1
                for p in List:
                    
                    if p not in Table[i+1:]:
                        ind = p
                        List.remove(p)
                        List.append(page)
                        time += 1
                        break
                    if Table[i+1:].index(p) > Max:
                        Max = Table[i+1:].index(p)
                        ind = p
                else:
                    List.remove(ind)
                    List.append(page)
                    time += 1
                
            else:
                List.append(page)
                temp += 1;time += 1
    return time #返回缺页次数

    
# Ram = Wind.RamSize
# Chunk = Wind.ChunkSize
# progress = Wind.ProgressSize
# Memory_Size = Wind.MemorySize
# algor = Wind.algor
# Page = PageTable(math.ceil(progress/(Chunk*1024)))
# Memory = MEMORY(Memory_Size)  #初始化内存分配的块
# ApplyForStationView(Memory_Size)   # 初始化内存块

# def main():
#     l = [7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]
#     print(l)
#     Opt(l,3)

# if __name__ == '__main__':
#     main()
