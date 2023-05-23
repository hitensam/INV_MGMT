
import datetime; # print("\n")

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
# print(today())
# print(datetime.date(2022, 9, 11))
