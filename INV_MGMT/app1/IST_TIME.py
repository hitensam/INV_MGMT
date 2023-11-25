import datetime
from . import models
INDIA_TIME = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30) #Adding 5:30 hrs to UCT Time

def today():
    global INDIA_TIME
    # datetime.datetime.strftime(INDIA_TIME,"%Y-%m-%d")  #Date of Issue
    # issue = datetime.datetime.strptime(issue,"%d %B %Y")   
    return (datetime.datetime.strftime(INDIA_TIME,"%Y-%m-%d"))

def fileDate():
    global INDIA_TIME
    # datetime.datetime.strftime(INDIA_TIME,"%Y-%m-%d")  #Date of Issue
    # issue = datetime.datetime.strptime(issue,"%d %B %Y")   
    return (datetime.datetime.strftime(INDIA_TIME,"%d-%m-%Y"))

def getPid(got_val):
    print("\ndate_got: ",got_val+"")
    # got_val = str(got_val)
    
    value = datetime.datetime.strptime(got_val,"%Y-%M-%d")
    # print(value,"\n")
    value = datetime.datetime.strftime(value,'%d-%M-%y')
    # print(value,"\n")
    value = value.replace("-", "")
    startValue = value+"1"
    startNum = 2

    while(len(models.Proforma_Invoice.objects.filter(PID = int(startValue)).all()) !=0):
        startValue = value + str(startNum);
        startNum = startNum + 1
    
    return startValue

    