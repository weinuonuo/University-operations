# coidng = utf-8
import re
import glob
import os
import getpass
import csv

test_list = ['create table a(数学 int,英语 char,语文 int);',\
            'insert into 成绩 values(c,54,66,89);',\
            'delete from b where b = b;',\
            # 'updata b set f = 'u' where f = 'A';',\
            'select * from 成绩;',\
            'alter table 成绩 add 化学 int;',\
            'alter table 成绩 drop 化学;',\
            'drop table a;'\
            'grant insert on 成绩 to zhangsan;'\
            'create user zhangsan indentified by 123456;']

re_list = []
re_list.append(re.compile(r'create\s+table\s+(\w+)\s*\((.*?)\);$',re.I))
re_list.append(re.compile(r'insert\s+into\s+(\w+)\s*values\s*\((.*?)\);$',re.I))
re_list.append(re.compile(r'insert\s+from\s+(\w+)\s+where\s+(\w+)\s*(>|<|=|>=|<=)\s*([\w\']+);$',re.I))
re_list.append(re.compile(r'updata\s+(\w+)\s+set\s+(\w+)\s*=\s*\'*(\w+)\'*\s+where\s+(.*?);$',re.I))
re_list.append(re.compile(r'select\s+([\w\*]+)\s+from\s+(\w+);$',re.I))
re_list.append(re.compile(r'alter\s+table\s+(\w+)\s+add\s+(\w+)\s+(\w+);$',re.I))
re_list.append(re.compile(r'alter\s+table\s+(\w+)\s+drop\s+(\w+);$',re.I))
re_list.append(re.compile(r'drop\s+table\s+(\w+);$',re.I))
re_list.append(re.compile(r'grant\s+([\w\,]+)\s+on\s+(\w+)\s+to\s+(\w+);$',re.I))
re_list.append(re.compile(r'create\s+user\s+(.*?)\s+indentified\s+by\s+(.*?);$',re.I))
re_list.append(re.compile(r'q$',re.I))
FUNCTION_list = ['create','insert','insert','updata','select','alter','alter','drop','grant','create','q']
TABLENAME_list = []         #存放数据的结构体
USERNAME_list = []          #存放用户的结构体
un = []                     #当前用户名

class User(object):
    def __init__(self,name,password):
        self.name = name #用户名
        self.password = password #密码
        self.limit = {} #各表权限
        
class Table(object):
    """docstring for Table"""
    def __init__(self, name):
        super(Table, self).__init__()
        self.tab_name = name
        self.pro_name = []
        self.line_data = []
    
def CreatTable(table_name,para):
    para = para.split(',')
    name = Table(table_name)
    for temp in para:
        tem = temp.split(' ')
        name.pro_name.append([tem[0],tem[1]])
    TABLENAME_list.append(name)
    print('插入表成功')

def Insert(name,para):
    para = para.split(',')    #数据
    for table in TABLENAME_list:
        if table.tab_name == name: 
            table.line_data.append([])
            break
    else:
        print('表不存在，请重新输入')
        return False
    i = 0
    for temp2 in table.pro_name:
        if temp2[1] == 'int' and para[i].isdigit(): #判断类型是否正确
            table.line_data[-1].append(para[i]) #在第几行插入第几个数据
            i += 1
        elif temp2[1] == 'char' and para[i].isalpha():
            table.line_data[-1].append(para[i])
            i += 1
        elif i == len(para):           #属性大小大于数据大小
            print("输入数据缺少")
            table.line_data.pop(-1)
            return False
        else:                           #前两项未匹配成功，类型错误
            print("输入类型错误")
            table.line_data.pop(-1)
            return False
    print('插入数据成功')

def Delete(name,con1,con2,con3):
    print(con1+con2+con3)
    for table in TABLENAME_list:
        if table.tab_name == name:
            break
    else:
        print('表不存在')
        return False
    for num,tab in enumerate(table.pro_name):
        if tab[0] == con1:
            break
    else:
        print('输入列不存在')
        return False 
    for data in table.line_data:
        if table.pro_name[num][1] == 'char':
            if data[num] == con3:
                table.line_data.remove(data)
        elif table.pro_name[num][1] == 'int':
            if con2 == '=':
                if data[num] == con3:
                    table.line_data.remove(data)
            else:    
                s = data[num]+con2+con3
                if eval(s):
                    table.line_data.remove(data)
        
def UpDate(tab_name,pro_name,prm,condition):
    print(condition)
    condition = re.compile(r'(\w+)\s*=\s*\'*(\w+)\'*',re.I).match(condition)
    print(condition.group(2))
    for table in TABLENAME_list:
        if table.tab_name == tab_name:
            for index,pro in enumerate(table.pro_name):
                if pro[0] == pro_name:
                    break
            else:
                print("输入列有误，请重新输入")
                return False
            for data in table.line_data:
                if data[index] == condition.group(2):
                    data[index] = prm
                    break
            else:
                print("未查询到符合条件的记录，请重新输入")
                return False

            

def PrintTable(pro,tab):
    if pro == '*':
        for table in TABLENAME_list:
            if table.tab_name == tab:
                for pro in table.pro_name:
                    print(pro[0],end = '    ')
                print()
                print('-------------------------')
                for line in table.line_data:
                    for data in line:
                        print(data,end='    ')
                    print()

def AddProperty(tab_name,pro_name,prm):
    for table in TABLENAME_list:
        if table.tab_name == tab_name:
            table.pro_name.append([pro_name,prm])
            print("插入列成功")
            break
    else:
        print('表不存在，请重新输入')

def DropProperty(tab_name,pro_name):
    for table in TABLENAME_list:
        if table.tab_name == tab_name:
            for index,pro in enumerate(table.pro_name):
                if pro[0] == pro_name:
                    table.pro_name.remove(pro)
            for line in table.line_data:
                if index+1 >= len(line):
                    continue
                line.pop(index)
            return True
    else:
        print("输入有误，请重新输入")

def DropTable(tab_name):
    for table in TABLENAME_list:
        if table.tab_name == tab_name:
            filename = table.tab_name+'.txt'
            filename2 = table.tab_name+'_values.txt'
            if os.path.exists(filename):
                os.remove(filename)
            else:
                print("该表不存在")
                return false
            if os.path.exists(filename2):
                os.remove(filename2)
            TABLENAME_list.remove(table)
            
def Grant(limits,tab_name,user_name):
    limit  = limits.split(',')
    # print(limit)
    for user in USERNAME_list:
       if user.name == user_name:
            break
    else:
        print('该用户不存在')
    # print(USERNAME_list)
    if tab_name not in user.limit:
        user.limit[tab_name] = limit
        # print(user.limit)
    else:
        if len(limit) == 1:
            user.limit[tab_name].extend(limit)
        else:
            for i in limit:
                if i not in user.limit[tab_name]:
                    user.limit[tab_name].extend(i)

def CreatUser(user_name,user_pw):
    user = User(user_name,user_pw)
    USERNAME_list.append(user)
    print('创建用户成功')

def OpenFile():
    values_file = re.compile(r'(\w+)_values\.txt')
    for file in glob.glob(r'*.txt'):
        if file == 'pw.txt':
            continue
        elif values_file.match(file):#数据文件
            for table in TABLENAME_list:
                if table.tab_name == values_file.match(file).group(1):
                    break
            else:
                name = Table(values_file.match(file).group(1))#创建table对象
                TABLENAME_list.append(name)
            
        else:                   #数据字典文件
            table_name = re.compile(r'(\w+)\.txt').match(file).group(1)
            f = open(file,'r')
            pros = f.read().strip('|').split('|')
            for table in TABLENAME_list:
                if table.tab_name == table_name:
                    break
            else:
                table = Table(table_name)#创建table对象
                TABLENAME_list.append(table)
                for pro in pros:
                    pro = pro.split(' ')
                    table.pro_name.append([pro[0],pro[1]])
            f.close()
    for file in glob.glob(r'*.csv'):
        with open(file,'r') as f:
            limits = csv.reader(f)
            for limit in limits:
                for user in USERNAME_list:
                    if limit[0] == user.name:
                        user.limit[limit[1]] = limit[2:]

def OpenFileFirst():
    values_file = re.compile(r'(\w+)_values\.txt')
    for file in glob.glob(r'*.txt'):
        if file == 'pw.txt':
            continue
        elif values_file.match(file):#数据文件
            for table in TABLENAME_list:
                if table.tab_name == values_file.match(file).group(1):
                    f = open(file,'r')
                    line = f.readline().strip().strip('|')
                    while line:
                        if line == ' ':
                            break
                        line = line.split('|')
                        table.line_data.append(line)#读入数据
                        line = f.readline().strip().strip('|')
                    f.close()
                    break
            else:
                name = Table(values_file.match(file).group(1))#创建table对象
                TABLENAME_list.append(name)
            
        else:                   #数据字典文件
            table_name = re.compile(r'(\w+)\.txt').match(file).group(1)
            f = open(file,'r')
            pros = f.read().strip('|').split('|')
            for table in TABLENAME_list:
                if table.tab_name == table_name:
                    for pro in pros:
                        pro = pro.split(' ')
                        table.pro_name.append([pro[0],pro[1]])
                    break
            else:
                table = Table(table_name)#创建table对象
                TABLENAME_list.append(table)
                for pro in pros:
                    pro = pro.split(' ')
                    table.pro_name.append([pro[0],pro[1]])
            f.close()
    

def WriteFile():
    for table in TABLENAME_list:
        f1 = open(table.tab_name+'.txt','w')
        if table.line_data :
            f2 = open(table.tab_name+'_values.txt','w')
            s2 = ''
            for line in table.line_data:#写入数据文件
                for data in line:
                    s2 = s2 + data + '|'
                s2 = s2 + '\n'
            f2.write(s2)
            f2.close()
        s1 = ''
        for pro in table.pro_name:#写入数据字典文件
            s1 = s1 + pro[0] + ' ' + pro[1] + '|'
        f1.write(s1)
        f1.close()
    
    with open('limit.csv','w') as f:
        for user in USERNAME_list:
            w = csv.writer(f)
            for tl in user.limit:
                s = []
                s.append(user.name)
                s.append(tl)
                s.extend(user.limit[tl])
                # print(s)
                w.writerow(s)

    f = open('pw.txt','w')
    for user in USERNAME_list:
        s = user.name + ':' + user.password+'\n'
        f.write(s)

def Test():
    OpenFile()
    if un[0] != 'admin':
        LimitForUser()
    command = input(">>")
    for index,com in enumerate(re_list):
        if com.match(command):
            re_com = com.match(command);
            if un[0] != 'admin':
                if re_com.group(1) != '*' and re_com.group(1) not in un[1]:
                    print('对此表无权限')
                    break
                elif re_com.group(1) == '*' and re_com.group(2) not in un[1]:
                    print('对此表无权限')
                    break
                if re_com.group(1) != '*' and FUNCTION_list[index] not in un[1][re_com.group(1)]:
                    print('对此操作无权限')
                    break
                elif re_com.group(1) == '*' and FUNCTION_list[index] not in un[1][re_com.group(2)]:
                    print('对此操作无权限')
                    break
            if index == 0 :
                CreatTable(re_com.group(1),re_com.group(2))
            elif index == 1:
                Insert(re_com.group(1),re_com.group(2))
            elif index == 2:
                Delete(re_com.group(1),re_com.group(2),re_com.group(3),re_com.group(4))
            elif index == 3:
                UpDate(re_com.group(1),re_com.group(2),re_com.group(3),re_com.group(4))
            elif index == 4:
                PrintTable(re_com.group(1),re_com.group(2))
            elif index == 5:
                AddProperty(re_com.group(1),re_com.group(2),re_com.group(3))
            elif index == 6:
                DropProperty(re_com.group(1),re_com.group(2))
            elif index == 7:
                DropTable(re_com.group(1))
            elif index == 8:
                Grant(re_com.group(1),re_com.group(2),re_com.group(3))
            elif index == 9:
                CreatUser(re_com.group(1),re_com.group(2))
            elif index == 10:
                print('谢谢使用')
                return False
            break
    else:
        print('语法错误')
    WriteFile()

def login():
    f = open('pw.txt','r')
    lines = f.read().strip().strip('|').split('\n')
    if lines:
        for users in lines:
            u = users.split(':')
            user = User(u[0],u[1])  #初始化用户类型
            USERNAME_list.append(user) # 加入用户表
    print('欢迎使用，请输入用户名密码')
    username = input("用户名：")
    un.append(username) 
    password = getpass.getpass("密码：")
    if username == 'admin' and password == 'admin':
        print('登录成功，欢迎您，超级管理员')
        return True
    for user in USERNAME_list:
        if username == user.name and password == user.password:
            print('登录成功，欢迎您')
            return True
    print('登录失败')
    return False

def LimitForUser():
    for user in USERNAME_list:
        if user.name == un[0]:
            un.append(user.limit)
            break

if __name__ == '__main__':
    if login():
        OpenFileFirst()
        while True:
            if Test():
                break