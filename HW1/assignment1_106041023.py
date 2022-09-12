
user = input('Welcome to Pymoney, please enter your name:')
total = int(input('How much money do you have? '))
idx = 0
accum = {} #accumulates the total amount you spent on something
items = [] #your item
cash = [] #this could be + or -, + means income, - means expense
income = 0 #total income
expense = 0 #total expense

#press ctrl + D will leave the while loop...

while True:
    try:

          obj,amount = input('Add an expense or income record with description and amount:').split() #obj: the item name / amount: the cash (+or-)
          
          items.append(obj) #item records the objects that create cash flows
          cash.append(int(amount)) #price (or salary) of the object
          total+=cash[idx]

          if not items[idx] in accum: #if an item has never been recorded, add this to dictionary'accum'
              accum[items[idx]] = 0
          accum[items[idx]]+=cash[idx] #accumulate how much you spent (gained) on this item

          if cash[idx] > 0:
              income+=cash[idx]
          else:
              expense-=cash[idx]
          
          print('Now you have ' + str(total) + ' dollars.\n' )
          idx= idx+1




    except EOFError:
        break

print('\n')

print('------- The current status of ' + user +' \'s'+' ASSEET: -------'+'\n')

for i in range(idx):
    if cash[i] < 0:
        print (items[i]+' cost you '+str(-cash[i])+' dollars '+'\n')

    else:
        print (items[i]+' gave you '+str(cash[i])+' dollars '+'\n')
print('\n')

print('Total income : ' + str(income) + '\nTotal expense : ' + str(expense) + '\n')

for key in accum.keys():  #accum is dictionary, use 'key()' to extract its index
    if accum[key] > 0:
        print('You totally got ' + str(accum[key]) + ' from ' + key +',which is ' + str(accum[key]*100//income) + '% of your income.\n' )#how much dose this item account for your income
    else:
        print('You totally spent ' + str(-accum[key]) + ' on ' + key +',which is '+ str(-accum[key]*100 //expense) +'% of your expense.\n')