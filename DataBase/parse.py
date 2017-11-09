import xml.etree.ElementTree as ET
import itertools
import collections
from lxml import etree
from prettytable import PrettyTable
import os
import sys
import re
import getpass


def GetMatched(statement, user='root'):
    '''
    给一个语句，返回一个参数列表
    retlist = ['selectwhere1','colums','tablename','parse']
    '''
    statement = re.sub(',\s+',',',statement)
    command_dict = {
    'create':'''\s*create\s+table\s+(\w+)\s*\(\s*(.*)\s*\)\s*;'''
    ,'insert':'''\s*insert\s+into\s+(\w+)\s*values\s*\(\s*(.*?)\s*\)\s*;'''
    ,'delete':'''\s*delete\s+from\s+(\w+)\s+where\s+(.*)\s*;'''
    ,'update':'''\s*update\s+(\w+)\s+set\s+(\w+)\s*=\s*([\w\']+)\s+where\s*(.*)\s*;'''
    ,'selectwhere1':'''\s*select\s+(.+)\s+from\s+(\w+)\s+where\s+(.*)\s*;$'''
    ,'selectwhere2':'''\s*select\s+(.+)\s+from\s+(.+)\s+where\s+(.*)\s*;$'''
    ,'select1':'''\s*select\s+(.+)\s+from\s+(\w+)\s*;'''
    ,'alteradd':'''\s*alter\s+table\s+(\w+)\s+add\s+(\w+)\s+(\w+)\s*;$'''
    ,'alterdrop':'''\s*alter\s+table\s+(\w+)\s+drop\s+(\w+)\s*;$'''
    ,'drop':'''\s*drop\s+table\s+(\w+);$'''
    ,'dropindex':'''\s*drop\s+index\s+(\w+);$'''
    ,'createindex':'''\s*create\s+index\s+(\w+)\s+on\s+(\w+)\s*\((\w+)\)\s*;$'''
    ,'grant':'''\s*grant\s+(.+)\s+on\s+(\w+)\s+to\s+(\w+);'''
    ,'createuser':'''\s*create\s+user\s+(\w+)\s+identified\s+by\s+(\w+);$'''
    ,'dict':'''\s*dict\s*;'''
    ,'what':'''\s*what\s*can\s*(\w+)\s*do\s*;'''
    ,'who':'''\s*who\s*am\s*I\s*;'''
    }
    retlist = []
    for key in command_dict:
        matchobject = re.compile(command_dict[key] ,re.I).match(statement)
        if matchobject:
            if key == 'who':
                print(user)
                return
            if key == 'what':
                retlist.append(key)
                retlist.append(user)
                retlist.extend(matchobject.groups())
            if user != 'root' and not HavePrivillage(user, key):
                print('no privillage')
                return
            retlist.append(key)
            retlist.extend(matchobject.groups())
            return retlist
            #return matchobject.groups()
    print('Invalid statement')
    return

def What(rawlist):
    '''给一个用户名，输出用户可以做什么'''
    user = rawlist[0]
    who = rawlist[1]
    if who.lower() == 'i':
        guys = user
    else:
        guys = who
    if guys == 'root':
        if who is 'i':
            print('You can do anything!')
        else:
            print('(S)He can do anything!')
        return
    if who is 'i':
        s = 'select * from user;'
        s = s.replace('user', guys)
        Parse(GetMatched(s))
        return
    if not FindTable(who):
        print('ummmm, I don\'t know this guy named ',who)
        return

def Parse(rawlist):
    '''给一个列表，进入操作函数'''
    if not rawlist:
        return
    function_list= {
        'create' : CreateHandle
        ,'select1' : SelectAllHandle
        ,'update' : UpdateHandle
        ,'what': What
        ,'select2' : SelectAllHandle
        ,'selectwhere1': SelectAllHandle
        ,'drop' : DropTableHandle
        ,'dropindex' : DropTableHandle
        ,'alterdrop' : AlterDropHandle
        ,'createindex': CreateIndexHandle
        ,'selectwhere2': SelectAllHandle
        ,'insert' : InsertHandle
        ,'dict' : ShowDataDict
        ,'delete' : DeleteHandle
        ,'grant' : GrantHandle 
        ,'alteradd' : AlterAddHandle
        ,'createuser' : CreateUserHandle
    }
    fun = function_list.get(rawlist[0].lower())
    if not fun:
        return
    fun(rawlist[1:])

def GetTypeDict():
    '''类型的全局变量'''
    typedict = {
        'int' : '''\d+'''
        ,'char' : '''\'\w+\''''
        ,'float' : '''\d+\.\d+'''
    }
    return typedict

def CreateIndexHandle(rawlist):
    '''建立索引，前置函数'''
    indexname = rawlist[0]
    tablename = rawlist[1]
    if not FindTable(tablename):
        print('not such table')
        return
    columnname = rawlist[2]
    CreateIndex(indexname, tablename, columnname)
def CreateIndex(indexname, tablename, columnname):
    '''创建索引'''
    d = GetTable(tablename)
    l = d[columnname]
    num = range(len(l))
    r= list(zip(num,l))
    r.sort(key = lambda x:x[1])
    res = list(zip(num, r))
    dic = collections.OrderedDict()
    dic['index'] = []
    dic['addr'] = []
    dic['column'] = []
    for i in res:
        dic['index'].append(i[0])
        dic['addr'].append(i[1][0])
        dic['column'].append(i[1][1])
    if not FindTable(indexname):
        Parse(GetMatched('create table '+indexname+'(index int, addr int, column char);'))
    for i in res:
        s = 'insert into ' + indexname + 'values(' \
                +str(i[0])+','+str(i[1][0])+',\''+str(i[1][1]) +'\');'
        Parse(GetMatched(s))
    root = GetRoot()
    PrintPrettyTable(dic)
    
def PrintPrettyTable(tabledict, sorted = '', reverse = False):
    head = [i for i in tabledict]
    coldatas = [tabledict[i] for i in tabledict]
    rawrows = list(zip(*coldatas))
    rows = []
    for i in rawrows:
        if i not in rows:
            rows.append(i)
    
    table = PrettyTable(head)
    if not rows:
        print(table)
        return
    for i in rows:
        table.add_row(list(i))
    if sorted:
        table.sort_key(sorted)
        table.reversesort = reverse
    print(table)

def CreateUserHandle(rawlist):
    '''创建用户'''
    user = rawlist[0]
    password = rawlist[1]
    s = "insert into psw values('"+str(user)+"','" + \
            str(password) + "');"
    Parse(GetMatched(s))

def GrantHandle(rawlist):
    '''为用户授权'''
    operation = rawlist[0]
    oplist = operation.split(',')
    db = rawlist[1]
    if db != 'DATABASE':
        print('no such database')
        return 
    user = rawlist[2]
    if not FindTable(user):
        s = 'create table user(db char, privillage char primary key);'
        s = s.replace('user', user)
        Parse(GetMatched(s))
    root = GetRoot()
    s = "insert into user values('db', 'privillage');"
    s = s.replace('user', user)
    s = s.replace('db', db)
    for i in oplist:
        s = s.replace('privillage', i.strip())
        Parse(GetMatched(s))

def HavePrivillage(user, operation):
    # 判断用户是否拥有对此表操作的权利
    if not FindTable(user):
        return
    dic = GetTable(user)
    opdict = {
        'create' : 'create'
        ,'select1' : 'select'
        ,'update' : 'update'
        ,'select2' : 'select'
        ,'selectwhere1':'select'
        ,'drop' : 'drop'
        ,'alterdrop' : 'alter'
        ,'createindex': 'createindex'
        ,'selectwhere2': 'select'
        ,'insert' : 'insert'
        ,'dict' : 'dict'
        ,'delete' : 'delete'
        ,'grant' :  'grant'
        ,'alteradd' : 'alter'
        ,'all' : 'all'
        ,'what':'what'

    }
    if operation == 'what':
        return True
    if opdict[operation] in dic['privillage']:
        return True
    print('no privillage')
    return

def CheckType(data, type, len = 65536):
    ''' 检测用户输入是否合法 '''
    type = type.lower()
    typedict = GetTypeDict()
    if type not in typedict:
        print('DEBUG : Table type error')
        return
    regex = re.compile(typedict[type], re.I)
    return regex.match(data)

def DataDict():
    '''建立数据字典'''
    def __getTableDataDict(table):
        ''' get each table's table dict'''
        datadict = collections.OrderedDict()
        datadict['columnname'] = []
        datadict['datatype'] = []
        datadict['isprimary'] = []
        cols = table.findall('col')
        for col in cols:
            datadict['columnname'].append(col.attrib['name'])
            datadict['datatype'].append(col.attrib['type'])
            datadict['isprimary'].append(col.attrib['primary'])
        return datadict

def ShowDataDict():
    '''打印表格'''
    DataDict()
    root = GetRoot("DataDict.xml")
    for i in root.findall('table'):
        d = GetTable(i.attrib['name'], "DataDict.xml")
        print(i.attrib['name'])
        PrintPrettyTable(d)


'''
def WritePrettyXML(root, filename = 'DATABASE.xml'):
    # 初始化树后将其写入文件保存 
    tree = ET.ElementTree(root)
    try:
        os.remove(filename) # 将已有文件删除
    except:
        pass
    tree.write(filename)
    
'''
def WritePrettyXML(root, filename = 'DATABASE.xml'):
    #初始化树后将其写入文件保存
    xmlstring = ET.tostring(root)
    newroot = etree.fromstring(xmlstring)
    tree = etree.ElementTree(newroot)
    try:
        os.remove(filename) # 将已有文件删除
    except:
        pass
    tree.write(filename, pretty_print=True)

def GetTable(tablename,filename='DATABASE.xml'):
    '''
    give the name of table, return dict of table, such as:
    d = {"column1_name" : ['data1', 'data2', 'data3'],
         "column2_name" : ['data1', 'data2', 'data3'],...
    }
    if no such table, return None
    '''
    root = GetRoot(filename)
    if not FindTable(tablename, filename):
        print("no no no such table")
        return
    # get column elementtree object
    colobj = root.findall(".//table[@name='" + tablename + "']/col")
    # finnal dictionary list
    columndict = collections.OrderedDict()
    for col in colobj:
        columnname = col.attrib['name']
        if col.text:
            columndict[columnname] = col.text.split('|')
        else:
            columndict[columnname] = []
    return columndict

def UpdateHandle(rawlist):
    tablename = rawlist[0]
    columnname = rawlist[1]
    newvalue = rawlist[2]
    expression = rawlist[3]
    if not FindTable(tablename):
        print('no such table')
        return 
    d = GetTable(tablename)
    if columnname not in d:
        print('no such column')
        return
    Update(tablename, columnname,newvalue ,expression)

def Update(tablename, columnname, newvalue, expression):
    root = GetRoot()
    table = root.find(".//table[@name='" + tablename + "']")
    if not table:
        print('No such table named', tablename)
        return
    tabledict = GetTable(tablename)
    # convert column table to row table 
    heads, rawrows = DictToRow(tabledict)
    dicttobedel = ExpressionHandle(tabledict, expression)
    heads, rowstobeupdate = DictToRow(dicttobedel)
    heads = [i for i in tabledict]
    ind = heads.index(columnname)
    newrows = []
    for i in rawrows:
        if i in rowstobeupdate:
            new = list(i)
            new[ind] = newvalue.strip('\'')
            newrows.append(new)
        else:
            newrows.append(i)
    newdict = collections.OrderedDict(zip(heads, list(zip(*newrows))))
    for i in newdict:
        table.find(".//col[@name='"+i+"']").text = '|'.join(newdict[i])
    WritePrettyXML(root)

def DropTableHandle(rawlist):
    tablename = rawlist[0]
    if not FindTable(tablename):
        print('drop error: no such table')
        return 
    DropTable(tablename)

def DropTable(tablename):
    root = GetRoot()
    table = root.find(".//table[@name='" + tablename + "']")
    root.remove(table)
    WritePrettyXML(root)

def AlterAddHandle(rawlist):
    tablename = rawlist[0]
    columnname = rawlist[1]
    datatype = rawlist[2]
    tabledict = GetTable(tablename)
    if not FindTable(tablename):
        print('no such table')
        return 
    if columnname in tabledict:
        print('column exists')
        return
    AlterAdd(tablename, columnname, datatype)

def AlterAdd(tablename, columnname, datatype):
    root = GetRoot()
    tabledict = GetTable(tablename)
    table = root.find(".//table[@name='" + tablename + "']")
    newcol = ET.SubElement(table, 'col')
    newcol.attrib['name'] = columnname
    newcol.attrib['type'] = datatype
    if tabledict.values():
        leng = len(list(tabledict.values())[0])
    newcol.text = '|'.join(['' for i in range(leng)])
    WritePrettyXML(root)

def AlterDropHandle(rawlist):
    tablename = rawlist[0]
    columnname = rawlist[1]
    if not FindTable(tablename):
        print('no such table')
        return 
    if columnname not in GetTable(tablename):
        print('column not exists')
        return
    AlterDrop(tablename, columnname)

def AlterDrop(tablename, columnname):
    root = GetRoot()
    tabledict = GetTable(tablename)
    table = root.find(".//table[@name='" + tablename + "']")
    col = table.find(".//col[@name='" + columnname + "']")
    table.remove(col)
    WritePrettyXML(root)

def ExpressionHandle(tabledict, expression):
    '''
    Giving table table dict and the expression, 
    return the list of rows which satisfy the expression.
    '''
    def __typeof(s):
        '''return the type of string, return None if error'''
        if re.compile("\s*'[^'\s]+'\s*").match(s):
            return 'str'
        if s in tabledict.keys():
            return 'column'
        if re.compile("\s*\d+\s*").match(s):
            return 'int'
        if re.compile("!=|>=|<=|>|<|=").match(s):
            return 'operation'
        if s.strip().lower() == 'and':
            return 'and'
        if s.strip().lower() == 'or':
            return 'or'
        print(s+' is not valid( Error in Expression Handle)')
        return
    
    def __eval(tablelist, expressionlist):
        rowlist = []
        expr = ''
        expressionlist.append('and')
        for row in tablelist:
            expr = ''
            final = ''
            for ele in expressionlist:
                if not __typeof(ele):
                    return
                if ele.strip() == 'and' or ele.strip() == 'or':
                    try:
                        final += str(eval(expr))
                    except:
                        print('Debug: eval error!!')
                        return
                    expr = ''
                    final += ' ' + ele + ' '
                elif __typeof(ele) == 'column':
                    if ele not in tabledict.keys():
                        print("No such column")
                        return 
                    if row[ele].isdigit():
                        expr += row[ele]
                    else:
                        expr += "'" + row[ele] + "'" 
                elif ele == '=':
                    expr += " == "
                else:
                    expr += " " + ele + " " 
            if not final:
                final += expr
            final = final.strip().strip('and').strip('or')
            try:
                res = eval(final)
            except:
                print("Debug: eval error(ExpressionHandle)")
                return
            if res:
                rowlist.append(row)
        return rowlist

    rawexprlist = re.split(r'(and|or|!=|>=|<=|>|<|=)', expression)
    expressionlist = [i.strip() for i in rawexprlist] 
    tablelen = len(list(tabledict.values())[0]) # 获得行的大小
    tablelist = []
    for i in range(tablelen):
        rowdict = collections.OrderedDict() # 有序字典
        for eachkey in list(tabledict.keys()):
            rowdict[eachkey] = tabledict[eachkey][i]
        tablelist.append(rowdict)
    rowlist = __eval(tablelist, expressionlist)
    rows = []
    heads = tabledict.keys()
    if rowlist:
        for i in rowlist:
            rows.append(list(i.values()))
    rowlist = collections.OrderedDict(zip(heads, list(zip(*rows))))
    return rowlist

def InTable(valueslist, tablename):
    tabledict = GetTable(tablename)
    l = tabledict.values()
    rows = zip(*l)
    if valueslist in rows:
        return index(valueslist)
    return

def InsertHandle(rawlist):
    tablename = rawlist[0]
    values = list(map(lambda x:x.strip(), rawlist[1].split(',')))
    regex = re.compile('''(\w+)\s+('\w+'|\w+)\s*''')
    # if no such table
    if not FindTable(tablename):
        print('no such table named ',tablename)
        return
    root = GetRoot()
    table = root.find(".//table[@name='" + tablename + "']")
    columnlist = table.findall('col')
    tabledict = GetTable(tablename)
    if len(values) != len(columnlist):
        print('value number not matched')
        return 
    if InTable(values, tablename):
        return 
    for i in range(len(values)):
        if not CheckType(values[i], columnlist[i].attrib['type']):
            print('type error : \'', values[i], '\' is not ', columnlist[i].attrib['type'])
            return
        if columnlist[i].attrib['primary'] == 'True' and columnlist[i].text:
            if values[i].strip('\'') in columnlist[i].text:
                print("primary key should be identified")
                return
        if columnlist[i].text:
            columnlist[i].text += '|' + values[i].strip("'")
        else:
            columnlist[i].text = values[i].strip("'")
    WritePrettyXML(root)

def ReadTable(tablename):
    tableobj = FindTable(tablename)
    # if no such table
    if not tableobj:
        print('no such table named '+ tablename)
        return
    # table founded
    root = GetRoot()
    cols = root.findall(".//*[@name='" + tablename + "']/col")
    head = []
    coldatas = []
    tabledict = collections.OrderedDict()
    for col in cols:
        colname = col.attrib['name']
        if col.text:
            coldata = col.text.split('|')
            tabledict[colname] = coldata
        else:
            tabledict[colname] = []
    return tabledict

def CartesianProduct(tablenamelist):
    '''笛卡尔积'''
    def __cartesian(rowlist1, rowlist2):
        if not rowlist1:
            return rowlist2
        l = []
        res = []
        for row1 in rowlist1:
            for row2 in rowlist2:
                l.append(row1 + row2)
        for i in l:
            if i not in res:
                res.append(i)
        return res

    curlist = []
    heads = []
    for tablename in tablenamelist:
        tabledict = GetTable(tablename)
        if not tabledict:
            print("table '",tablename ,"' not exist ")
        heads.extend([tablename+'.'+i for i in tabledict])
        curlist = __cartesian(curlist, list(zip(*tabledict.values())))
    return collections.OrderedDict(list(zip(heads, zip(*curlist))))

def SelectAllHandle(rawlist):
    ''' rawlist such as: ['*', 'tablename'] 
    or ['col1, col2', 'tablename']
    or ['col1, col2', 'tablename', 'a = 1 and b = 2']'''
    tablename = rawlist[1]
    if ',' in tablename:
        tablenamelist = [i.strip() for i in tablename.split(',')]
        tabledict = CartesianProduct(tablenamelist)
        if not tabledict:
            print("table error")
            return
    else:
        tablename = rawlist[1]
        tabledict = ReadTable(tablename)
    TableWillPrint = collections.OrderedDict()
    if not tabledict:
        return 
    if rawlist[0] == '*':
        columns = tabledict.keys()
    else:
        columns = rawlist[0].split(',')
    # select where
    if len(rawlist) == 3:
        expression = rawlist[2]
        tabledict = ExpressionHandle(tabledict, expression)
    for i in columns:
        if i.strip() not in tabledict:
            print(tabledict)
            print('The column \'', i, '\' is not valid.(select)')
            return
        TableWillPrint[i.strip()] = tabledict[i.strip()]
    PrintPrettyTable(TableWillPrint)

def DictToRow(tabledict):
    head = [i for i in tabledict]
    coldatas = [tabledict[i] for i in tabledict]
    rawrows = list(zip(*coldatas))
    return head, rawrows

def DeleteHandle(rawlist):
    tablename = rawlist[0]
    root = GetRoot()
    table = root.find(".//table[@name='" + tablename + "']")
    if not table:
        print('No such table named', tablename)
        return
    expression = rawlist[1]
    tabledict = GetTable(tablename)
    # convert column table to row table 
    heads, rawrows = DictToRow(tabledict)
    dicttobedel = ExpressionHandle(tabledict, expression)
    heads, rowstobedel = DictToRow(dicttobedel)
    heads = [i for i in tabledict]
    newrows = [i for i in rawrows if i not in rowstobedel]
    newdict = collections.OrderedDict(zip(heads, list(zip(*newrows))))
    for i in newdict:
        table.find(".//col[@name='"+i+"']").text = '|'.join(newdict[i])
    WritePrettyXML(root)
    
def CreateHandle(rawlist):
    tablename = rawlist[0]
    paralist = rawlist[1].split(',')
    regexprimary = re.compile('''\s*(\w+)\s+(\w+|\w+\s+\(\d+\))\s+(primary\s+key)\s*''')
    regex = re.compile('''\s*(\w+)\s+(\w+|\w+\s+\(\d+\))\s*''')
    primarykey = ''
    columns = []
    for i in paralist:
        mat = regexprimary.match(i) or regex.match(i)
        if not mat:
            return
        else:
            columns.append((mat.group(1), mat.group(2)))
            if len(mat.groups()) == 3:
                if primarykey:
                    print('There must be only one primarykey!')
                    return
                primarykey = mat.group(1)
    CreateTable(tablename, columns, primarykey)   
def CreateTable(tablename, columns, primary = ''):
    ''' 
    prarmeter:
    tablename : string of table name
    columns   : list of columns like [('col1', 'data'), ('col2', '13')]
    primary   : if not given , default empty string
    '''
    object = FindTable(tablename)
    if object:
        print('Sorry,Table ', tablename, ' Exist!')
    else:
        root = GetRoot()
        typedict = GetTypeDict()
        newtable = ET.SubElement(root, 'table')
        newtable.attrib['name'] = tablename
        newtable.attrib['primary'] = primary
        for eachcol in columns:
            col = ET.SubElement(newtable, 'col')
            col.attrib['name'] = eachcol[0]
            col.attrib['type'] = eachcol[1]
            if eachcol[1] not in GetTypeDict():
                print("not such type named ", eachcol[1])
                return 
            col.attrib['primary'] = str(primary == eachcol[0]) 
        WritePrettyXML(root)

def FindTable(tablename, filename='DATABASE.xml'):
    '''查找表是否存在，存在则返回表的xml对象'''
    tree = ET.parse(filename)
    root = tree.getroot()
    return root.find(".//table[@name='" + tablename + "']")

def GetRoot(filename='DATABASE.xml'):
    ''' return root '''
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

def CreateDatabase(name):
    db = ET.Element('db')
    db.set('name', name)
    WritePrettyXML(db)
    return db

def init(filename='DATABASE.xml', dbname='db'):
    # 如果数据库文件不存在，则创建数据库
    if not os.path.exists(filename):
        root = CreateDatabase(dbname)
    else:
        tree = ET.parse(filename) # 建立树型存储结构
        root = tree.getroot() # 得到树的根
    return root

def Login():
    if not FindTable('psw'): # 创建用户表
        s1 = 'create table psw(user char primary key, password char);'
        Parse(GetMatched(s1))
        s2 = "insert into psw values('root', '123');"
        Parse(GetMatched(s2))
    tabledict = GetTable('psw') # 更新内存中的表
    while 1:
        user = input("input user:")
        if user not in tabledict['user']:
            print('no such user')
            continue
        psw = getpass.getpass('input psw:')
        ind = tabledict['user'].index(user)
        if tabledict['password'][ind] == psw:
            print("Welcome!")
            break
        else:
            print("password is not correct")
    return user

def test():
    raw = ''
    root = init()
    WritePrettyXML(root)
    currentuser = Login()
    while 1:
        print(">",end="")
        cur = input()
        if raw.startswith('--'):
            continue
        else:
            raw += '\n' + cur
        if raw.strip() == 'q':
            print('Thank you for using.')
            sys.exit()
        if raw.endswith(';'):
            Parse(GetMatched(raw, currentuser))
            raw = ''

if __name__ == "__main__":
    test()
