from datetime import datetime
import time
import requests


data = []
sim_avg1 = 0
exp_avg1 = 0
sim_avg2 = 0
exp_avg2 = 0
sim_avg3 = 0
exp_avg3 = 0

def sim_avg(data, period):
    length = len(data)
    sum = 0
    for i in range(length - period, length):
        sum += data[i]
    return sum / period


def exp_avg(data, period, previous):
    length = len(data)
    smoothing = 2 / (period + 1)
    return (data[length - 1] - float(previous)) * smoothing + float(previous)


# adjust period to do analyze different portions of time:
# period = 60 - exponential moving averages of n minutes
# period = 3600 - exponential moving averages of n hours
# period = 86400 - exponential moving averages of n days
def main():
    key = input("Please enter your API key: ")
    coin = input("What currency would you like to use? Please type its abreviation: ")
    print("For moving averages of n minutes, the period should be 60 seconds\nFor moving averages of n hours, the period should be 3660 seconds\nFor moving averages of n days, the period should be 86400 seconds")
    period = int(input("What is the desired unit for our moving averages? Please answer in seconds: "))
    print("We will use 3 exponential moving averages. Please enter the size of each moving average you wish to use in order from smallest to largest:")
    first = int(input("Size of first moving average: "))
    second = int(input("Size of second moving average: "))
    third = int(input("Size of third moving average: "))
    while True:
        live = requests.get('http://api.coinlayer.com/api/live?access_key=' + str(key))
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        try:
            price = live.json()["rates"][coin]
        except:
            print("Error: Currency or API key not found. Please try again")
            main()
        print("At " + current_time + ", the price of " + coin +  " is: " + str(price))
        data.append(price)
        if(len(data) == first):
            sim_avg1 = sim_avg(data, first)
            print("The " + str(first) + " " + str(period) + "-second moving average is: " + str(sim_avg1))
        elif(len(data) == first + 1):
            exp_avg1 = exp_avg(data, first, sim_avg1)
            print("The " + str(first) + " " + str(period) + "-second moving average is: " + str(exp_avg1))
        elif(len(data) > first):
            exp_avg1 = exp_avg(data, first, exp_avg1)
            print("The " + str(first) + " " + str(period) + "-second moving average is: " + str(exp_avg1))

        if(len(data) == second):
            sim_avg2 = sim_avg(data, second)
            print("The " + str(second) + " " + str(period) + "-second moving average is: " + str(sim_avg2))
        elif(len(data) == second + 1):
            exp_avg2 = exp_avg(data, second, sim_avg1)
            print("The " + str(second) + " " + str(period) + "-second moving average is: " + str(exp_avg2))
        elif(len(data) > second):
            exp_avg2 = exp_avg(data, second, exp_avg1)
            print("The " + str(second) + " " + str(period) + "-second moving average is: " + str(exp_avg2))

        if(len(data) == third):
            sim_avg3 = sim_avg(data, third)
            print("The " + str(third) + " " + str(period) + "-second moving average is: " + str(sim_avg3))
        elif(len(data) == third + 1):
            exp_avg3 = exp_avg(data, third, sim_avg1)
            print("The " + str(third) + " " + str(period) + "-second moving average is: " + str(exp_avg3))
        elif(len(data) > third):
            exp_avg3 = exp_avg(data, third, exp_avg1)
            print("The " + str(third) + " " + str(period) + "-second moving average is: " + str(exp_avg3))

        if len(data) > first and len(data) > second and (len(data) == third or len(data) > third):
            if exp_avg1 > exp_avg2 > exp_avg3:
                print("BUY ORDER")
            if exp_avg1 < exp_avg2:
                print("SELL ORDER")




        time.sleep(period)


if __name__ == "__main__":
    main()
