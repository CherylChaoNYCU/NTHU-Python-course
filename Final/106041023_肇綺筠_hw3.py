import sys
import os

# ****************************************************


class Record:
    """Represent a record."""

    def __init__(self, s):
        # 1. Define the formal parameters so that a Record can be instantiated
        #    by calling Record('meal', 'breakfast', -50).
        # 2. Initialize the attributes from the parameters. The attribute
        #    names should start with an underscore (e.g. self._amount)
        try:
            r = s.split(' ') #r[0] = ctgr / r[1] = item name / r[2] = price
        except:
            print('Invalid input. Fail to add.\n')
            self._built = -1
            return

        if len(r) != 3: #includes category / item / expense or income
            print('Invalid input. Fail to add.\n')
            self._built = -1
            return
        try:
            amount = int(r[2])
        except:
            print('Invalid input. Fail to add.\n')
            self._built = -1
            return

        self._ctgr = r[0]
        self._dscrpt = r[1]
        self._amount = amount
        self._built = 1

        # Define getter methods for each attribute with @property decorator.
        # Example usage:
        # >>> record = Record('meal', 'breakfast', -50)
        # >>> record.amount
        # -50

    @property
    def built(self):
        return self._built

    @property
    def ctgr(self):
        return self._ctgr

    @property
    def dscrpt(self):
        return self._dscrpt

    @property
    def amount(self):
        return self._amount


class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""

    def __init__(self):
        # 1. Read from 'records.txt' or prompt for initial amount of money.
        # 2. Initialize the attributes (self._records and self._initial_money)
        #    from the file or user input.
        self.amount = 0
        self.list = []
        path = os.getcwd()+'/records.txt'
        welcome = 1  # check if error exists
        s = []  # storing data from txt
        if os.path.exists(path):  # file exists
            fpr = open('records.txt', 'r')
            s = fpr.readlines()
            fpr.close()

        else:  # error(7) file doesn't exist
            fpr_new = open('records.txt', 'a')  #the file is not created yet, create a new one
            welcome = 0
            fpr_new.close()

        if welcome:  # get initial money from txt
            if len(s) == 0:  #the file is empty! all entries must be deleted by the user
                welcome = 0

            else:

                try:
                    self.amount = int(s[0]) #load the money we have
                except:
                    welcome = 0
                for line in s[1:]:
                    self.add(line, categories) #adding all lines and categories into records

        if welcome:
            print("Welcome back!")

        if welcome == 0:  # error happens, user input
            s = input("How much money do you have?")
            # error(1) user inputs initial amount cannot be converted to integer.
            try:
                self.amount = int(s)
            except:
                print('Invalid value for money. Set to 0 by default.')
                self.amount = 0

    def add(self, s, categories):

        # 1. Define the formal parameter so that a string input by the user
        #    representing a record can be passed in.
        # 2. Convert the string into a Record instance.
        # 3. Check if the category is valid. For this step, the predefined
        #    categories have to be passed in through the parameter.
        # 4. Add the Record into self._records if the category is valid.
        r = Record(s) #s represents users' input like : meal dinner -100
        if r.built == -1:
            return
        if categories.is_category_valid(r.ctgr, categories.ctgr, 0) is True: #placing input ctgr and the whole ctgr into function, check if the input string exist in the ctgr table in categories
            self.list.append(r)
        else:
            print('The specified category is not in the category list.')
            print("You can check the category list by command \"view categories\".")
            print("Fail to add a record.")

    def view(self):
        # 1. Print all the records and report the balance.
        now_amount = self.amount #this is the current money we have, which is recored at 'view'
        print('Here\'s your expense and income records:')
        print("|{:<23s}|{:<25s}|{:<25s}|".format(
            'Category', 'Description', 'Amount'))
        print(
            ' ======================= ========================= =========================')
        for r in self.list: #reminder: r stands for "record", which is initialized at records.add
            print("|{:<23s}|{:<25s}|{:<25s}|".format(
                r.ctgr, r.dscrpt, str(r.amount)))  # 置中顯示
            now_amount += r.amount

        print(
            ' ======================= ========================= =========================')
        print('Now you have ' + str(now_amount)+' dollars.')

    def delete(self):
        # 1. Define the formal parameter.
        # 2. Delete the specified record from self._records.

        print(
            '====== ======================= ========================= =========================')
        j = 0
        for r in self.list:
            print("| {:<4s}|{:<23s}|{:<25s}|{:<25s}|".format(
                str(j), r.ctgr, r.dscrpt, str(r.amount)))  # 置中顯示

            j = j+1

        print(
            '====== ======================= ========================= =========================')

        sid = input('Chose the id you want to delete: ')
        try:
            id = int(sid)
        except:
            print('Invalid input. Fail to delete.')
            return
        if id < 1 or id >= j:
            print('Invalid input. Fail to delete.')
            return

        self.list = self.list[:id] + self.list[id+1:] #connecting the elements before and after id together(id element will be covered)

    def save(self):

        # 1. Write the initial money and all the records to 'records.txt'.
        path = os.getcwd()+'/records.txt'

        if os.path.exists(path):  # file exists
            fpr = open('records.txt', 'w')
            fpr.write(str(self.amount)+'\n')
            for r in self.list:
                fpr.write(r.ctgr + ' ' + r.dscrpt + ' ' + str(r.amount) + '\n')
            fpr.close()

        else:  # error(7) file doesn't exist
            fpr_new = open('records.txt', 'a')
            fpr.write(str(self.amount)+'\n')
            for r in self.list:
                fpr.write(r.ctgr + ' ' + r.dscrpt + ' ' + str(r.amount) + '\n')
            fpr.close()

    def find(self, fctgr): #fctgr is the category the user want to find
        # 1. Define the formal parameter to accept a non-nested list
        #    (returned from find_subcategories)
        if categories.is_category_valid(fctgr, categories.ctgr, 0) is False:
            print('Category does not exist.')
            return
        l = categories.find_subcategories(fctgr)

        # 2. Print the records whose category is in the list passed in
        #    and report the total amount of money of the listed records.
        ttl_a = 0
        found = 0
        for r in self.list:
            for c in l: #l records all the subcategories under fctgr
                if r.ctgr == c: #element in records matched
                    ttl_a += r.amount # adding up the total amount
                    found = 1
                    break

        if found == 0:
            print('No record in this category.')
            return

        print('Here\'s your expense and income records under category ' + fctgr + ' :')

        print("|{:<23s}|{:<25s}|{:<25s}|{:<25s}|".format(
            'Category', 'Description', 'Amount', 'Percentage(%)'))
        print(
            ' ======================= ========================= ========================= =========================')
        for r in self.list:
            for c in l:
                if r.ctgr == c:
                    print("|{:<23s}|{:<25s}|{:<25s}|{:<25s}|".format(
                        r.ctgr, r.dscrpt, str(r.amount), str(round(r.amount*100/ttl_a, 3))))

                    break
        print(
            ' ======================= ========================= ========================= =========================')
        print('The total amount above is '+str(ttl_a))


class Categories:
    """Maintain the category list and provide some methods."""

    def __init__(self):
        self._ctgr = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', [
            'bus', 'railway']], 'income', ['salary', 'bonus']]

    @property
    def ctgr(self):
        return self._ctgr

    def view(self, l, id=0, s=0):
        # 1. Define the formal parameters so that this method
        #    can be called recursively.
        # 2. Recursively print the categories with indentation.
        # 3. Alternatively, define an inner function to do the recursion.
        # print('****' + str(id) + ' ' + str(l[id]))
        if id == len(l):
            return
        if type(l[id]) == list:
            self.view(l[id], 0, s+1)
        else:
            space = '    '*s
            print(space + ' - ' + l[id])

        self.view(l, id+1, s)

    def is_category_valid(self, string, l, id=0):

        # 1. Define the formal parameters so that a category name can be
        #    passed in and the method can be called recursively.
        # 2. Recursively check if the category name is in self._categories.
        # 3. Alternatively, define an inner function to do the recursion.

        if id == len(l): #we traverse to the end of ctgr table and couldn't find the string we want -> invalid -> return false
            return False
        
        #the below function will recursively traverse each element in the ctgr table, until we find the element matches the input string->valid!
        if type(l[id]) == list:
            if self.is_category_valid(string, l[id], 0) is True:
                return True

        if l[id] == string:
            return True

        return self.is_category_valid(string, l, id+1)

    def find_subcategories(self, f_ctgr):

        def find_subcategories_gen(category, l, found=False):
            if type(l) == list:
                for index, child in enumerate(l):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(l) \
                            and type(l[index + 1]) == list:
                        # When the target category is found,
                        # recursively call this generator on the subcategories
                        # with the flag set as True.
                        yield from find_subcategories_gen(category, l[index + 1], True)
            else:
                if l == category or found:
                    yield l

        return(list(find_subcategories_gen(f_ctgr, self.ctgr, False)))

        # A list generated by find_subcategories_gen(category, self._categories)

# ****************************************************


global categories
categories = Categories()
records = Records()


while True:
    command = input(
        '\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
    if command == 'add':
        record = input(
            'Add an expense or income record with \' Categories Description Amount \' :\n')
        records.add(record, categories)
    elif command == 'view':
        records.view()
    elif command == 'delete':
        records.delete()
    elif command == 'view categories':
        categories.view(categories.ctgr)
    elif command == 'find':
        category = input('Which category do you want to find? ')
        records.find(category)
    elif command == 'exit':
        records.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')
