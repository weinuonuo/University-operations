from prettytable import PrettyTable
ready = [] # 就绪队列
running = [] # 运行队列
block = [] # 阻塞队列
finished = [] # 完成队列
Jobs = []
class Job(object):
    '''class for job'''
    def __init__(self,name,arrival_time,runned_time):
        self.name = name
        self.arrival_time = int(arrival_time) # 到达时刻
        self.runned_time = int(runned_time) # 运行时长
        self.running_time = self.runned_time # 时间片轮转用于计时
        self.burst_time = -1 # 开始时间
        self.finished_time = -1 # 结束时刻
        self.turnaround_time = -1 # 周转时长
        self.w_turnaround_time = -1 # 带权周转时长
    
    def _Runned(self):
        '''运行结束时，计算用时'''
        self.turnaround_time = self.finished_time - self.arrival_time
        self.w_turnaround_time = round(self.turnaround_time/self.runned_time,2) 

    def _Joblist(self):
        '''生成列表'''
        job = [self.name,self.arrival_time,self.runned_time,self.burst_time
                ,self.finished_time,self.turnaround_time,self.w_turnaround_time]
        return job

def CreateJob(rawlist):
    '''创建进程'''
    newjob = Job(rawlist[0],rawlist[1],rawlist[2])
    Jobs.append(newjob)

def Calculate(Algor):
    '''根据算法选择函数'''
    fun_dic = {
        "f":FCFS
        ,"s":SJF
        ,"r":RR
    }
    fun = fun_dic.get(Algor.lower())
    if not fun:
        return
    fun()

def FCFS():
    '''先来先服务'''
    time = Jobs[0].arrival_time
    for index,job in enumerate(Jobs):
        if not running:
            running.append(job)
            PrintProcess()
            job.burst_time = time # 开始时间等于当前时间
            job.finished_time = time + job.runned_time
            job._Runned()
            finished.append(running.pop())
            time = job.finished_time
    PrintJob()
            

def SJF():
    '''短作业优先'''
    Jobs.sort(key = lambda x:(x.arrival_time,x.runned_time))
    time = Jobs[0].arrival_time
    ready.append(Jobs[0])
    while ready:
        if not running and ready:
            nowjob = ready.pop(0)
            running.append(nowjob)
            PrintProcess()
            nowjob.burst_time = time # 开始时间等于当前时间
            nowjob.finished_time = time + nowjob.runned_time
            for job2 in Jobs[Jobs.index(nowjob)+1:]:
                if job2.arrival_time <= nowjob.finished_time and job2 not in ready and job2 not in finished:
                    ready.append(job2)
            ready.sort(key = lambda x:x.runned_time)
            time = nowjob.finished_time
            nowjob._Runned()
            finished.append(running.pop(0))
        if not ready and len(finished) != len(Jobs):
            for j in Jobs:
                if j not in ready and j not in finished:
                    ready.append(j)
        # PrintList(ready)
    PrintJob()


def RR():
    '''时间片轮转'''
    global Time
    time = Jobs[0].arrival_time
    for job in Jobs:
        ready.append(job)
    while len(finished) != len(Jobs):
        if len(ready) > len(Jobs):
            print("---------------BUG---------------")
            break       
        if not running:
            now_job = ready.pop(0)
            running.append(now_job)
            PrintProcess()
            if now_job.burst_time == -1:
                now_job.burst_time = time
            # 如果一个时间片未用完已经完成程序
            if now_job.running_time - Time <= 0:
                now_job.finished_time = time + now_job.running_time
                time += now_job.running_time
                running.pop(0)
                now_job._Runned()
                finished.append(now_job)
                continue
            now_job.running_time -= Time
            time += Time
            print(time)
            ready.append(running.pop(0))
    PrintJob()

def PrintProcess():
    '''方便查看每个状态队列'''
    global Algor
    print("-----------------------------")
    print("就绪队列")
    for job in ready:
        print(str(job.name)+" ",end = " ")
    print("\n运行队列")
    for job in running:
        print(str(job.name)+" ",end = " ")
    print("\n阻塞队列")
    for job in block:
        print(str(job.name)+" ",end = " ")
    print("\n结束队列")
    for job in finished:
        print(str(job.name)+" ",end = " ")
    if Algor == "r":
        print("\n---------还需服务时间-----------")
        for job in Jobs:
            if job not in finished:
                print(str(job.name)+" "+str(job.running_time))
            

def PrintJob():
    '''打印进程状态'''
    head = ['进程名','到达时刻','运行时长','开始时刻','结束时刻','周转时间','带权周转时间']
    table = PrettyTable(head)
    avg_run,avg_wrun = 0,0
    for job in Jobs:
        avg_run += job.turnaround_time
        avg_wrun += job.w_turnaround_time
        table.add_row(job._Joblist())
    print(table)
    print("平均周转时间"+str(round(avg_run/len(Jobs),2)))
    print("平均带权周转时间"+str(round(avg_wrun/len(Jobs),2)))

def Parse(raw):
    raw = raw.split(" ")
    if raw[0].lower() == "c":
        CreateJob(raw[1:])
    else:
        return

def main():
    global Time,Algor
    Algor = input('请选择算法')
    if Algor.lower() == "r":
        Time = int(input("请输入轮转时间"))
    while True:
        raw = input(">")
        Parse(raw)
        if raw.lower() == 'q':
            Calculate(Algor)

if __name__ == '__main__':
    main()


'''
测试数据
c A 0 4
c B 1 3
c C 2 5
c D 3 2
c E 4 4

c j1 1 5
c j2 1 3
c j3 0 3
c j4 0 2

c j1 0 4
c j2 1 3
c j3 2 5
c j4 3 2
c j5 4 4

'''
