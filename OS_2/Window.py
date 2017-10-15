import tkinter as tk
import tkinter.messagebox
from OS_2 import *
# 弹窗

class MyDialog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('初始化信息')
        # 弹窗界面
        self.SetUi()

    def SetUi(self):
        # 第一行（两列）
        row1 = tk.Frame(self)
        row1.pack(fill = 'x') 
        tk.Label(row1, text='总内存大小：').pack(side=tk.LEFT)
        self.RamSize = tk.IntVar()
        self.RamSize.set(64)
        tk.Entry(row1, textvariable=self.RamSize, width= 10).pack(side=tk.LEFT)
        
        # 第二行
        row2 = tk.Frame(self)
        row2.pack(fill='x', ipadx=1, ipady=1)
        tk.Label(row2, text='块大小：').pack(side=tk.LEFT)
        self.ChunkSize = tk.IntVar()
        self.ChunkSize.set(4)
        tk.Entry(row2, textvariable=self.ChunkSize, width= 10).pack(side=tk.LEFT)
        # 第三行
        row3 = tk.Frame(self)
        row3.pack(fill='x', ipadx=1, ipady=1)
        tk.Label(row3, text='进程大小：').pack(side=tk.LEFT)
        self.ProgressSize = tk.IntVar()
        self.ProgressSize.set(5000)
        tk.Entry(row3, textvariable=self.ProgressSize, width= 10).pack(side=tk.LEFT)

        row4 = tk.Frame(self)
        row4.pack(fill='x', ipadx=1, ipady=1)
        tk.Label(row4, text='分配内存块：').pack(side=tk.LEFT)
        self.MemorySize = tk.IntVar()
        self.MemorySize.set(3)
        tk.Entry(row4, textvariable=self.MemorySize, width= 10).pack(side=tk.LEFT)

        self.radioframe = tk.Frame(self)
        self.radioframe.pack()
        self.algor = tk.StringVar()
        self.radioframe.choc = tk.Radiobutton(self.radioframe, text='FIFO',variable=self.algor, value='FIFO',anchor='e')
        self.radioframe.choc.pack(fill='x')

        self.radioframe.straw = tk.Radiobutton(self.radioframe, text='LRU',variable=self.algor, value='LRU',anchor='e')
        self.radioframe.straw.pack(fill='x')

        self.radioframe.lemon = tk.Radiobutton(self.radioframe, text='OPT',variable=self.algor, value='OPT',anchor='e')
        self.radioframe.lemon.pack(fill='x')

        
        row5 = tk.Frame(self)
        row5.pack(fill='x')
        tk.Button(row5, text='取消', command=self.cancel).pack(side=tk.RIGHT)
        tk.Button(row5, text='确定', command=self.ok).pack(side=tk.RIGHT)


    def ok(self):
        self.inits = [self.RamSize.get(), self.ChunkSize.get(),self.ProgressSize.get(),self.MemorySize.get(),self.algor.get()] # 设置数据
        self.destroy() # 销毁窗口
    def cancel(self):
        self.inits = None # 空！
        self.destroy()

class MyWindow(tk.Tk): # 主窗口
    def __init__(self):
        super().__init__()
        self.title('OS')
        self.RamSize = 0
        self.ChunkSize = 0
        self.ProgressSize = 0 
        self.MemorySize = 0
        self.algor = ''
        self.LogicAddress = '0000'
        self.StationView = ''
        self.ReplaceView = ''
        self.PageView = ''
        self.RAM = ''
        self.PhysicalAdd = ''
        self.FindNum = 0
        self.lackNum = 0
        self.lackPro = 0.0
        self.OptNum = 0
        self.SetUi()

    def SetUi(self):
        frame_Up = tk.Frame(self)
        frame_Up.pack(side = tk.TOP,fill = 'both')

        row1 = tk.Frame(frame_Up)
        tk.Button(row1,text = '初始化',command = self.setup_config).pack(side = tk.TOP)
        row1.pack(side = tk.LEFT)
        row2 = tk.Frame(frame_Up)
        tk.Label(row2, text='总内存大小：',justify = 'right',width = 10,anchor = 'e').pack(side=tk.TOP)
        self.l1 = tk.Label(row2, text=self.RamSize, width= 10)
        self.l1.pack(side=tk.TOP)
        row2.pack(side = tk.LEFT)
        row3 = tk.Frame(frame_Up)
        tk.Label(row3, text='块大小：',width = 10,justify = 'right',anchor = 'e').pack(side=tk.TOP)
        self.l2 = tk.Label(row3, text=self.ChunkSize, width= 10)
        self.l2.pack(side=tk.TOP)
        row3.pack(side = tk.LEFT)
        row4 = tk.Frame(frame_Up)
        tk.Label(row4, text='进程大小：',width = 10,justify = 'right',anchor = 'e').pack(side=tk.TOP)
        self.l3 = tk.Label(row4, text=self.ProgressSize, width= 10)
        self.l3.pack(side=tk.TOP)
        row4.pack(side = tk.LEFT)
        row5 = tk.Frame(frame_Up)
        tk.Label(row5, text='分配内存块：',width = 10,justify = 'right',anchor = 'e').pack(side=tk.TOP)
        self.l4 = tk.Label(row5, text=self.MemorySize, width= 10)
        self.l4.pack(side=tk.TOP)        
        row5.pack(side = tk.LEFT)
        row6 = tk.Frame(frame_Up)
        tk.Label(row6, text='置换算法:',width = 10,justify = 'right',anchor = 'e').pack(side=tk.TOP)
        self.l5 = tk.Label(row6, text=self.algor, width= 10)
        self.l5.pack(side=tk.TOP) 
        row6.pack(side = tk.LEFT)



        frame_Down = tk.Frame(self)
        frame_Down.pack(side = tk.BOTTOM,fill = 'both')

        row8 = tk.Frame(frame_Down)
        tk.Label(row8, text='内存空间位视图',width = 15).pack(side=tk.TOP)
        self.l6 = tk.Label(row8, text=self.StationView, width= 10)
        self.l6.pack(side=tk.TOP) 
        row8.pack(side = tk.LEFT,fill = 'both')

        row9 = tk.Frame(frame_Down)
        tk.Label(row9, text='置换空间位视图',width = 15).pack(side=tk.TOP)
        self.l7 = tk.Label(row9, text=self.StationView, width= 10)
        self.l7.pack(side=tk.TOP) 
        row9.pack(side = tk.LEFT,fill = 'both')

        row10 = tk.Frame(frame_Down)
        tk.Label(row10, text='页表',width = 10).pack(side=tk.TOP)
        self.l8 = tk.Label(row10, text=self.PageView, width= 10)
        self.l8.pack(side=tk.TOP) 
        row10.pack(side = tk.LEFT,fill = 'both')

        row11 = tk.Frame(frame_Down)
        tk.Label(row11, text='内存',width = 10).pack(side=tk.TOP)
        self.l9 = tk.Label(row11, text=self.RAM, width= 10)
        self.l9.pack(side=tk.TOP) 
        row11.pack(side = tk.LEFT,fill = 'both')

        row12 = tk.Frame(frame_Down)
        row12.pack(side = tk.TOP,fill = 'y')
        tk.Label(row12, text='逻辑地址:',width = 10).pack(side=tk.LEFT)
        self.l10 = tk.Label(row12, text=self.LogicAddress, width= 10)
        self.l10.pack(side=tk.RIGHT)

        row13 = tk.Frame(frame_Down)
        row13.pack(side = tk.TOP,fill = 'y')
        tk.Label(row13, text='物理地址:',width = 10).pack(side=tk.LEFT)
        self.l11 = tk.Label(row13, text=self.PhysicalAdd, width= 10)
        self.l11.pack(side=tk.RIGHT)

        row13 = tk.Frame(frame_Down)
        row13.pack(side = tk.TOP,fill = 'y')
        tk.Label(row13, text='访问次数:',width = 10).pack(side=tk.LEFT)
        self.l12 = tk.Label(row13, text=self.FindNum, width= 10)
        self.l12.pack(side=tk.RIGHT)

        row14 = tk.Frame(frame_Down)
        row14.pack(side = tk.TOP,fill = 'y')  
        tk.Label(row14, text='缺页次数:',width = 10).pack(side=tk.LEFT)
        self.l13 = tk.Label(row14, text=self.lackNum, width= 10)
        self.l13.pack(side=tk.RIGHT)

        row15 = tk.Frame(frame_Down)
        row15.pack(side = tk.TOP,fill = 'y')
        tk.Label(row15, text='缺页率:',width = 10).pack(side=tk.LEFT)
        self.l14 = tk.Label(row15, text=self.lackPro, width= 10)
        self.l14.pack(side=tk.RIGHT)
        

        row7 = tk.Frame(frame_Down)
        tk.Button(row7, text='OPT', command=self.OPT).pack(side=tk.RIGHT)
        tk.Label(row7, text='逻辑地址').pack(side=tk.LEFT)
        self.LogicAddress = tk.StringVar()
        tk.Entry(row7, textvariable=self.LogicAddress, width= 10).pack(side=tk.LEFT)
        tk.Button(row7, text='设置', command=self.cancel).pack(side=tk.LEFT)
        row7.pack(side = tk.BOTTOM)

        

    def setup_config(self): # 更新初始化信息
        global StationView,ReplaceView,Page,Memory,Replace,List,algor,Table,Memory_Size

        res = self.ask_init()
        if res is None:
            return
        self.RamSize, self.ChunkSize, self.ProgressSize ,self.MemorySize, self.algor= res
        self.l1.config(text = self.RamSize)  
        self.l2.config(text = self.ChunkSize)      
        self.l3.config(text = self.ProgressSize)
        self.l4.config(text = self.MemorySize)
        self.l5.config(text = self.algor)

        self.StationView = '';self.ReplaceView = '';self.PageView = '';self.RAM = ''
        StationView,ReplaceView = InstallStationView(self.RamSize,self.ChunkSize)   # 初始化位视图
        for index,i in enumerate(StationView.flat):
            self.StationView += str(i)
            temp = index+1
            if temp % 8 == 0:
                self.StationView += '\n'
        self.l6.config(text = self.StationView)

        for index,i in enumerate(ReplaceView.flat):
            self.ReplaceView += str(i)
            temp = index+1
            if temp % 8 == 0:
                self.ReplaceView += '\n'
        self.l7.config(text = self.ReplaceView)

        Ram = self.RamSize
        Chunk = self.ChunkSize
        progress = self.ProgressSize
        Memory_Size = self.MemorySize
        algor = self.algor
        Page = PageTable(math.ceil(progress/(Chunk*1024)))
        Memory = MEMORY(Memory_Size)  #初始化内存分配的块
        ApplyForStationView(Memory_Size,StationView,Memory)   # 初始化内存块
        List = [] # 置换使用的栈
        Replace = REPLACE(ReplaceView)
        Table = []
        for i in Page.PageNum:
            self.PageView += str(i) + ' '
            if Page.getPhysicalBlock(i) == -1:
                self.PageView += '_' + '  '
            else:
                self.PageView += str(Page.getPhysicalBlock(i))+ '  '
            if Page.getStateStation(i) == False:
                self.PageView += '_' + '\n'
            else:
                self.PageView += str(Page.getStateStation(i)) + '\n'
        self.l8.config(text = self.PageView)

        for index,i in enumerate(Memory.Page):
            self.RAM += str(index) + ' '
            if i == -1:
                self.RAM += '__'+'\n'
            else:
                self.RAM += str(i)+'\n'
            # self.RAM += str(Memory.getStation(index))+'\n'
        self.l9.config(text = self.RAM)

    def ask_init(self): # 调用子窗口
        initDialog = MyDialog()
        self.wait_window(initDialog)
        return initDialog.inits

    def OPT(self):
        global Table,Memory_Size
        Time = Opt(Table,Memory_Size)
        s = '缺页次数：'+ str(Time) + '\n' + '缺页率:' + str(Time/len(Table)) 
        tk.messagebox.showinfo("OPT",s) 

    def cancel(self): # 输入逻辑地址，进行更新
        global StationView,ReplaceView,Page,Memory,Replace,List,algor,Table

        self.FindNum += 1
        # if AddressConvert(self.lackNum,self.LogicAddress.get(),self.ChunkSize,
        #             Replace,Page,Memory,List,StationView,ReplaceView,algor) == False:
        #     return False
            
        self.lackNum,self.PhysicalAdd = AddressConvert(self.lackNum,self.LogicAddress.get(),
                                        self.ChunkSize,Replace,Page,Memory,List,StationView,ReplaceView,algor,Table)
        self.lackPro = round(self.lackNum/self.FindNum,2)

        self.StationView = '';self.ReplaceView = '';self.PageView = '';self.RAM = ''
        for index,i in enumerate(StationView.flat):
            self.StationView += str(i)
            temp = index+1
            if temp % 8 == 0:
                self.StationView += '\n'
        self.l6.config(text = self.StationView)
        for index,i in enumerate(ReplaceView.flat):
            self.ReplaceView += str(i)
            temp = index+1
            if temp % 8 == 0:
                self.ReplaceView += '\n'
        self.l7.config(text = self.ReplaceView)
        for i in Page.PageNum:
            self.PageView += str(i) + ' '
            if Page.getPhysicalBlock(i) == -1:
                self.PageView += '_' + '  '
            else:
                self.PageView += str(Page.getPhysicalBlock(i)) + ' '
            if Page.getStateStation(i) == False:
                self.PageView += '_' + '\n'
            else:
                self.PageView += 'T' + '\n'
        self.l8.config(text = self.PageView)
        for index,i in enumerate(Memory.Page):
            self.RAM += str(index) + ' '
            if i == -1:
                self.RAM += '__'+'\n'
            else:
                self.RAM += str(i)+'\n'
            # self.RAM += str(Memory.getStation(index))+'\n'
        self.l9.config(text = self.RAM)
        self.l7.config(text = self.ReplaceView)
        self.l10.config(text = self.LogicAddress.get())
        self.l11.config(text = self.PhysicalAdd)
        self.l12.config(text = self.FindNum)
        self.l13.config(text = self.lackNum)
        self.l14.config(text = self.lackPro)


def main():
    Wind = MyWindow()
    Wind.mainloop()

if __name__ == '__main__':
    main()
