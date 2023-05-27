# import datetime; # print("\n")

# INDIA_TIME = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30) #Adding 5:30 hrs to UCT Time

# def today():
#     global INDIA_TIME
#     # datetime.datetime.strftime(INDIA_TIME,"%Y-%m-%d")  #Date of Issue
#     # issue = datetime.datetime.strptime(issue,"%d %B %Y")   
#     return (datetime.datetime.strftime(INDIA_TIME,"%d-%m-%Y"))

# print(today())
# # print(datetime.date(2022, 9, 11))

import pandas as pd
# from SSI.app1.models import stock
# from django.db.models import Q

file = pd.read_csv('D:\Downloads\data.csv')

# print(file.head)

# print(list(file.loc[[0,2]]))
# for i in range(64):
#     # print(file.loc[[i, 0][0]])
# print(file.shape)

l = file.values.tolist()

for i in range(len(l)):
    print('Name : ', l[i][0], " ",'width ',l[i][1], " ", 'roll : ', l[i][2], " net :", l[i][3], " gross : ", l[i][4] )
    try:
        stock.objects.filter(Q(item = (l[i][0])) & Q(Roll_no =  int(l[i][2]))\
                & Q(width =  int(l[i][1]))).get() #changes
        flag = 1
        # print('try working')
    except:
        flag = 0
    if (flag):
            context = {'message' : 'Details exists already with same item and roll no.'}
            print(context)
    else:
        obj = stock(item=l[i][0], width = float(l[i][1]), Roll_no = int(l[i][2]), Net_wt=float(l[i][3]), Gr_wt=float(l[i][4]))
        obj.save()