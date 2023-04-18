import csv
from multiprocessing.connection import answer_challenge
import CustomerClass
import random
from ServerClass import Server


## take in time string formatted as 00:00:00 and convert it to total seconds
def toSeconds(time):
    time = str(time)
    numbers = time.split(":")
    hours = int(numbers[0])
    minutes = int(numbers[1])
    seconds = int(numbers[2])
    return hours*3600 + minutes*60 + seconds

def toPercent(percent):
    numberString = percent.split("%")
    number = float(numberString[0]) / 100
    return number

def randomD(min, max):
    return random.uniform(min, max)

index = []
incoming_calls = []
answer_calls = []
answer_rate = []
abandonded_calls = []
answer_speed = []
talk_duration = []
waiting_time =[]
service_level = []


#  CSV FORMAT
#  Index,Incoming Calls,Answered Calls,Answer Rate,Abandoned Calls,Answer Speed (AVG),Talk Duration (AVG),Waiting Time (AVG),Service Level (20 Seconds)
#  Open sample data file
with open('data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    #next(reader)

    for row in reader:
        index.append(int(row[0]))
        incoming_calls.append(int(row[1]))
        answer_calls.append(int(row[2]))
        answer_rate.append(str(row[3]))
        abandonded_calls.append(int(row[4]))
        answer_speed.append(toSeconds(row[5]))
        talk_duration.append(toSeconds(row[6]))
        waiting_time.append(toSeconds(row[7]))
        service_level.append(str(row[8]))

avg = sum(abandonded_calls) / len(abandonded_calls)
numofA = len(abandonded_calls)
answerSpeedSecondList = list()
rand = random.randint(0, max(answer_speed))
#print(rand)

randomDay = random.randint(min(index), max(index))
randomServiceTime = random.randint(min(talk_duration), max(talk_duration))

customerCount = int(input("how many customers for this simulation: "))
serverCount = int(input("how many servers for this simulation: "))

#intialize total num of customer
customerEntered = 0.0
customerList = []
for i in range(customerCount):
    num = random.randint(0, 4)
    if num == 4:
        cus = CustomerClass.Customer(i, randomD(0.2, 1.3) + customerEntered, randomD(0, randomServiceTime + 2))
    else:
        cus = CustomerClass.Customer(i, randomD(0.2, 1.3) + customerEntered, randomD(0, randomServiceTime))
    customerEntered = cus.getEntryTime()
    customerList.append(cus)
customerList[0].setServiceStartTime(customerList[0].getEntryTime())
customerList[0].setServiceEndTime(customerList[0].getServiceStartTime() + customerList[0].getServiceTime())
print(customerList[0].toString())

for i in range(1, len(customerList)):
    cus = customerList[i]
    prevCus = customerList[i-1]

    cus.setServiceStartTime(prevCus.getServiceEndTime())
    cus.setServiceEndTime(cus.getServiceStartTime() + cus.getServiceTime())
    print(cus.toString())

## List of servers
serverList = []
for i in range(serverCount):
    serverList[i] = Server()

## dictionary of server and customer pairs
serverCustDuo = dict()
for i in range(serverCount):
    serverCustDuo[serverList[i]] = customerList.pop(0)

serverKeys = serverCustDuo.keys()
