#coding = utf-8

import queue

#就绪态
Ready = queue.Queue()
#阻塞态
crimp = queue.Queue()
#运行态,判断是否为空 
run = []
#内存类，包含起始位置，空间大小，进程数量，进程所占空间大小，方法包含增加，删除
class RAM():
	"""docstring for RAM"""
	def __init__(self,OsSize,RamSize): #内存总大小，操作系统所占空间
		super(RAM, self).__init__()
		self.ProNum = 0
		self.Size = [['',OsSize,RamSize]] #进程名 开始地址 终止地址
 
	def Install(self,Process):
		name = Process.name
		for pro in self.Size:
			if pro[0] == name:
				pro[0] = ''
		self.Size.sort(key = lambda x:x[1])
		#上空下空，上空下占，上占下空，上占下占都可以归类成，如果下一个是空的就合并，直到循环一遍没有合并为止
		while True:
			for index,pro in enumerate(self.Size):
				if not pro[0]:
					if index == len(self.Size)-1:
						continue
					pro_down = self.Size[index+1]
					if not pro_down[0]:
						self.Size.append(['',pro[1],pro_down[2]])
						self.Size.remove(pro)
						self.Size.remove(pro_down)
						self.Size.sort(key = lambda x:x[1])
						break
			else:
				break
	

#进程类，包含起始位置，空间大小，运行状态
class Process():
	"""docstring for Process"""
	def __init__(self,name,Pro_Inital,Pro_Size):
		super(Process, self).__init__()
		self.name = name
		self.Pro_Inital = Pro_Inital
		self.Pro_Size = Pro_Size

def CreateProcess(name,size):	#创建进程
	for pro in Ram.Size:
		if not pro[0]:
			if pro[2] - pro[1] > size:
				if pro[2] -pro[1] -size <= 2:
					name = Process(name,pro[1],pro[2] -pro[1])
					Ram.Size.append([name.name,pro[1],pro[2]])
					Ram.Size.remove(pro)
				else:
					name = Process(name,pro[1],size)
					Ram.Size.append([name.name,pro[1],pro[1]+size])
					Ram.Size.append(['',pro[1]+size,pro[2]])
					Ram.Size.remove(pro)
				Ready.put(name)
				if not run:
					run.append(Ready.get())
				print("创建进程成功")
				break
	else:
		print("内存已满，无法创建")

def EndProcess():#结束进程
	if not run :
		print("当前无进程正在运行")
		return 0
	else:
		Ram.Install(run.pop())
		print("结束成功")
		if Ready.empty():
			return 0
		else:
			pro = Ready.get()
			run.append(pro)
			return 0

def CrimpProcess():#阻塞进程
	if not run :
		print("当前无进程正在运行")
	else:
		pro_r = run.pop()
		crimp.put(pro_r)
		print("阻塞成功")
		if Ready.empty():
			return 0
		else:
			pro = Ready.get()
			run.append(pro)

def ActiveProcess():#激活进程
	if crimp.empty():
		print("当前无进程被阻塞")
	else:
		Ready.put(crimp.get())
		if not run:
			run.append(Ready.get())
		print("激活成功")

def PrintProcess():#打印当前状态
	print("就绪态：",end = '')
	if not Ready.empty():
		for i in range(0,Ready.qsize()):
			pro = Ready.get()
			print(pro.name+"<"+str(pro.Pro_Inital)+","+str(pro.Pro_Size)+">",end = '')
			Ready.put(pro)
	print()
	
	print("执行态：",end = '')
	if run:
		pro = run.pop()
		print(pro.name+"<"+str(pro.Pro_Inital)+","+str(pro.Pro_Size)+">")
		run.append(pro)
	else:
		print()

	print("阻塞态：",end = '')
	if not crimp.empty():
		for i in range(0,crimp.qsize()):
			pro = crimp.get()
			print(pro.name+"<"+str(pro.Pro_Inital)+","+str(pro.Pro_Size)+">",end = '')
			crimp.put(pro)
	print()

def PrintRam():
	print("已占用空间：",end = '')
	for pro in Ram.Size:
		if pro[0]:
			print(pro[0]+"<"+str(pro[1])+","+str(pro[2])+"> ",end = '')
	print()

	print("未占用空间：",end = '')
	for pro in Ram.Size:
		if not pro[0]:
			print("<"+str(pro[1])+","+str(pro[2])+"> ",end = '')
	print()

def Round(): #时间片轮转
	if not run :
		print("当前无进程正在运行")
	else:
		Ready.put(run.pop())
		run.append(Ready.get())
		print("轮转完成")

def Help():	#帮助文档
	print('''命令的使用：
			1.创建进程: C/c + 空格 +进程名
			2.终止进程: E/e
			3.阻塞进程: T/t
			4.激活进程: A/a
			5.时间片到: R/r
			6.查看进程状态: s1
			7.查看内存状态: s2
			8.退出: Q/q
			9.帮助文档: H/h
		''')

if __name__ == '__main__':
	command = input("创建内存,请输入内存起始位置和大小\n>>").split(' ')
	Ram = RAM(int(command[0]),int(command[1]))
	print("内存创建成功")
	while True:
		command = input(">>").split(" ")
		command[0].lower()
		if(command[0] == 'c'):
			CreateProcess(command[1],int(command[2]))
		elif command[0] == 'e':
			EndProcess()
		elif command[0] == 't':
			CrimpProcess()
		elif command[0] == 'a':
			ActiveProcess()
		elif command[0] == 'r':
			Round()
		elif command[0] == 's1':
			PrintProcess()
		elif command[0] == 's2':
			PrintRam()
		elif command[0] == 'q':
			break
		elif command[0] == 'h':
			Help()
		else:
			print("非法指令")
	print("感谢本次使用")
