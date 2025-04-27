#GroceryStoreSim.py
#Name: Aurora Gunubu    
#Date: 4/27/25
#Assignment: Lab 11

import simpy
import random
eventLog = []
waitingShoppers = []
idleTime = 0

def shopper(env, id):
    arrive = env.now
    items = random.randint(1, 20)
    #Shopping times change based on number of items
    if items < 5: 
        shoppingTime = items / 2  # shopping time takes 1/2 a minute per item
    elif items <= 10:
        shoppingTime = items * 0.75 # shopping time takes 3/4 of a minute per item
    else:
        shoppingTime = items # shopping time takes a minute per item
    
    yield env.timeout(shoppingTime)
    # join the queue of waiting shoppers
    waitingShoppers.append((id, items, arrive, env.now))
    
def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1) # wait a minute and check again

        customer = waitingShoppers.pop(0)
        items = customer[1]
        #Assumption: Checker can scan 15 items/minute
        if items < 15: 
            checkoutTime = (items // 15) + 1 #If number of items is less than 15, takes 1 minute 
        else:
            checkoutTime = (items // 15) + 1 #If number of items is 15+, takes 2 minutes 
        yield env.timeout(checkoutTime)

        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))

def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(1) #New shopper every minute

def processResults():
    totalWait = 0
    totalShoppers = 0
    totalItems = 0
    totalShoppingTime = 0

    for e in eventLog:
        waitTime = e[4] - e[3] #depart time - done shopping time
        shoppingTime = e[3] - e[2]
        totalShoppingTime = totalShoppingTime + shoppingTime
        totalWait += waitTime
        totalShoppers += 1
        totalItems += e[1]

    avgWait = totalWait / totalShoppers
    avgItems = totalItems / totalShoppers
    avgShoppingTime = totalShoppingTime / totalShoppers

    print("The average wait time was %.2f minutes." % avgWait)
    print("The total idle time was %d minutes" % idleTime)
    print("The average amount of items bought was %d items" % avgItems)       
    print("The average shopping time was %.2f minutes." % avgShoppingTime)

def main():
    numberCheckers = 1

    env = simpy.Environment()

    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=180 )
    print(len(waitingShoppers))
    processResults()

if __name__ == '__main__':
    main()