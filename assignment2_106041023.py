import sys
import os

def initialize(): #whenever we initialize our program, we must create new data or read our old data
    read_record = []

    path = os.getcwd()+'/record.txt' #this part is getting the current working directory + the records we saved
    existing = 1
    s = [] #this will store all data in record.txt 

    if os.path.exists(path): #if the file exists
        fpr = open('record.txt','r')
        s = fpr.readlines()
        fpr.close()
    
    else: #the file is not created yet, create a new one
        fpr_new = open('record.txt','a')
        existing = 0
        fpr_new.close()

    if existing:
        if len(s) == 0: #the file is empty! all entries must be deleted by the user
            existing = 0

        else:
            j = 0
            for i in s:
                line = i.split()
                if len(line)!=2: #the line wasn't seperated into the correct format (ex. item,amount) shouldn't be recorded
                    if j == 0: #first line error
                        existing = 0
                    continue
                try:
                    amount = int(line[1])
                except:
                    if j == 0:
                        existing = 0
                    continue
                new = (line[0],amount) #placing the item & amount into our data
                read_record.append(new)
                j = j + 1

    if existing:
         print('welcome back~')
    if existing == 0:
        s = input("How much money do you have?")
        try:
            ini_money = int(s)
        except:
            print('Invalid value for money. Set to 0 by default.')
            ini_money = 0
        read_record = [('initial_money', ini_money)] + read_record

    return read_record

def add(r):
    tip = input(
        'Add expense or income record(s) seperated by \', \' with description and amount.\n'
        + 'The format of a record should be like this: a 2, b 3, c 4.\n')
    try:
        x = tip.split(', ') #split the added items: ex. (breakfast  -50), (milk -100), (salary +2000)
    except:
        pass
    for tmp in x:
        i = tmp.split() #spliting: 'breakfast' and '-50'
        if len(i)!=2:
            print(
                'The format of a record should be like this: a 2, b 3, c 4.\nFail to add '+tmp)
            return r
        else:
            try:
                amount = int(i[1])
            except:
                print(
                    'The format of a record should be like this: a 2, b 3, c 4.\nFail to add '+tmp)
                return r
            r.append((i[0],amount))

    return r

def view_detail(r):  #to check what the user had done(add or delete)
    pin = [] #percentage of income
    pex = [] #percentage of expense
    income = 0
    expense = 0
    i = 0
    for item, amount in r:  # 計算總支出/收入
        if i > 0:
            if amount > 0:
                income += amount
            else:
                expense -= amount
        i = i+1
    i = 0
    for item, amount in r:  # 計算各項支出/收入比例
        if i > 0:
            if amount > 0:
                pin.append(str(round(100*amount/income, 3)))
                pex.append('-') #put a dash for the percentage of expense
            else:
                pex.append(str(round(-100*amount/expense, 3)))
                pin.append('-')
        i = i+1 #we need to skip the first entry (total amount)

    # 顯示

    print("| {:^4s}|{:^23s}|{:^25s}|{:^25s}|".format(
        'id', 'Description', 'Income (percentage)', 'Expense (percentage)'))  # 置中顯示
    print('====== ======================= ========================= =========================')
    
    now = r[0][1]  # r[0][1] is our total amount of money
    #print(now)
    i = 0
    for item, amount in r:
        if i > 0:
            now += amount #caculate the total money again with new entries from r (from the initial money...)
            if amount > 0:
                print("|{:^5d}|{:^23s}|{:^25s}|{:^25s}|".format(
                    i, item, str(amount)+'('+pin[i-1]+'%)', pex[i-1])) #item starts from 0 in pin and pex
            else:
                print("|{:^5d}|{:^23s}|{:^25s}|{:^25s}|".format(
                    i, item, pin[i-1], str(-amount)+'('+pex[i-1]+'%)'))

            print(
                '────────────────────────────────────────────────────────────────────────────────────')
        i = i+1
    print("|{:^29s}|{:^25d}|{:^25d}|".format(
        'Total', income, expense))
    print('Now you have ' + str(now) + ' dollars.')



def view_added(r):
    pin = {}
    pex = {}
    dic = {}  # 以名稱為key,金額為value
    income = 0
    expense = 0
    i = 0
    now = 0
    for item, amount in r:  # 計算總支出/收入
        now += amount
        if i > 0:
            if not item in dic:
                dic[item] = 0 #if this item is new to dictionary, add it into dic and remember to set the initial amount as '0'

            dic[item] += amount

        i = i+1

    for item in dic:  # 計算各項支出/收入比例

        if dic[item] > 0:
            pin[item] = (str(round(100*dic[item]/now, 3)))
            pex[item] = ('-')
        else:
            pex[item] = (str(round(-100*dic[item]/now, 3)))
            pin[item] = ('-')
    i = i+1

    # 顯示

    print("|{:^23s}|{:^25s}|{:^25s}|".format(
        'Description', 'Income (percentage)', 'Expense (percentage)'))  # 置中顯示
    print(' ======================= ========================= =========================')

    print("|{:^23s}|{:^25s}|{:^25s}|".format(
        'initial money', str(r[0][1])+'(' + str(round(100*r[0][1]/now, 3)) + '%)', '-'))
    print(
        '─────────────────────────────────────────────────────────────────────────────')

    for item in dic:

        if dic[item] > 0:
            print("|{:^23s}|{:^25s}|{:^25s}|".format(
                  item, str(dic[item])+'('+pin[item]+'%)', pex[item]))

        else:
            print("|{:^23s}|{:^25s}|{:^25s}|".format(
                  item, pin[item], str(-dic[item])+'('+pex[item]+'%)'))

        print(
            '─────────────────────────────────────────────────────────────────────────────')

    print("|{:^23s}|{:^51d}|".format(
        'Now you have', now))


def delete(r):

    view_delete(r)  # 透過view選擇要刪除的編號
    print('Chose the id you want to delete:')

    sdel_id = input()

    try:  # error(5) the user inputs in an invalid format in respect of your design
        del_id = int(sdel_id)
    except:
        print('id does not exist.')
        return r

    if del_id == 0: #if you delete your initial money...
        s = input("How much money do you have?")
        # error(1) user inputs initial amountcannot be converted to integer.
        try:
            ini_money = int(s)
        except:
            print('Invalid value for money. Set to 0 by default.')
            ini_money = 0
        r = [('initial_money', ini_money)] + r[1:]
        return r

    if del_id > len(r):  # error(6)the specified record does not exist
        print('id does not exist.')
        return r

    r = r[:del_id]+r[del_id+1:] #recover the data without the entry of id you selected
    return r


def view_delete(r):
    pin = []
    pex = []
    income = 0
    expense = 0
    i = 0
    for item, amount in r:  # 計算總支出/收入
        if i > 0:
            if amount > 0:
                income += amount
            else:
                expense -= amount
        i = i+1
    i = 0
    for item, amount in r:  # 計算各項支出/收入比例
        if i > 0:
            if amount > 0:
                pin.append(str(round(100*amount/income, 3)))
                pex.append('-')
            else:
                pex.append(str(round(-100*amount/expense, 3)))
                pin.append('-')
        i = i+1

    # 顯示

    print("| {:^4s}|{:^23s}|{:^25s}|{:^25s}|".format(
        'id', 'Description', 'Income (percentage %)', 'Expense (percentage %)'))  # 置中顯示
    print('====== ======================= ========================= =========================')
    print("|{:^5s}|{:^23s}|{:^25s}|{:^25s}|".format(
        '0', 'initial money', str(r[0][1])+'(-)', '-'))
    print(
        '────────────────────────────────────────────────────────────────────────────────────')
    now = r[0][1]
   # print(r[0][1])
    i = 0
    for item, amount in r:
        if i > 0:
            now += amount
            if amount > 0:
                print("|{:^5d}|{:^23s}|{:^25s}|{:^25s}|".format(
                    i, item, str(amount)+'('+pin[i-1]+')', pex[i-1]))
            else:
                print("|{:^5d}|{:^23s}|{:^25s}|{:^25s}|".format(
                    i, item, pin[i-1], str(-amount)+'('+pex[i-1]+')'))

            print(
                '────────────────────────────────────────────────────────────────────────────────────')
        i = i+1 #skip the first line  which indicates the initial money


def save(r):
    path = os.getcwd()+'/record.txt'

    if os.path.exists(path):  # file exists
        fpr = open('record.txt', 'w')
        for item, amount in r:
            fpr.write(item+' '+str(amount)+'\n')
        fpr.close()

    else:  # error(7) file doesn't exist
        fpr_new = open('record.txt', 'a')
        for item, amount in r:
            fpr_new.write(item+' '+str(amount)+'\n')
        fpr_new.close()
                

    







records = initialize()

#record is the variable that records all possible data added by the user

while True:

    command = input('What do you want to do (add / view detail / view added / delete / exit)? ')

    if command == 'add':
        records = add(records) #adding something new to our datagram/ update 'record'
    elif command == 'view detail':
        view_detail(records)
    elif command == 'view added':
        view_added(records)
    elif command == 'delete':
        records = delete(records)
    elif command == 'exit': #save the result whenever the user exit
        save(records)
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')
    
#print (stdout) is for normal program output, while stderr is only for error message
       