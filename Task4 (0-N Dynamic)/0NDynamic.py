import random
import sys
import math
import time
import csv


''' Helper globals '''
debug = False
test = True
testLowCapacity = False
default = False
printing = False

class item:
    def __init__(self, weight, value, quantity):
        self.weight = weight
        self.value = value
        self.quantity = quantity

def main(args):
    #do stuff here
    if test: 
        trials = 5
        for n in range(100, 1001, 100):
            averageTime = 0.0
            totalTime = 0
            for trial in range(trials):
                '''worst case would be where items is equal to weight capacity (n x n board)'''
                capacity = n
                if testLowCapacity:
                    capacity = capacity // 10
                #generate random item lists of length capacity
                items = generateWorstItemsList(n, n)

                #test time
                startTime = time.time()

                newItems = enumerateItems(items)
                knapsack = pickItems(newItems, capacity)
                results = backTrace(newItems, knapsack, capacity)

                endTime = time.time()
                totalTime += endTime - startTime
                if debug: print("Table size: " + str(len(knapsack)) + ", " + str(len(knapsack[0])))
                if printing:
                    #print items results here
                    print(*results)

                print(totalTime)
            averageTime = totalTime / trials
            print("n: ", n, " average time: ", averageTime)
            #add to csv
            with open('0NDynamicDataRandomDense.csv', 'a') as file : 
                    writer = csv.writer(file)
                    writer.writerow([n, averageTime])
        


    if default: 
        # items = generateWorstItemsList(20, 20)
        # print("length of items before enumeration: " + str(len(items)))
        # newItems = enumerateItems(items)
        # print("length of items after enumeration: " + str(len(newItems)))

        newItems = [
            item(7,47,1),
            item(5,30,1),
            item(5,25,1),
            item(4,24,1),
        ]
        capacity = 10
        knapsack = pickItems(newItems, capacity)
        results = backTrace(newItems, knapsack, capacity)
        if printing: print(*results)

def pickItems(items, W):
    #initialize array of j rows (items) and W columns (weights from 0-W)
    knapsack = [[0 for j in range(W + 1)] for y in range(len(items)+1)]

    if debug: printMatrix(knapsack)

    # rows correspond to items, columns corresponds to weight
    if debug: print("rows: " + str(len(knapsack)) + " columns: " + str(len(knapsack[0])))
    for row in range(1, len(knapsack)):
        for col in range(1, len(knapsack[row])):
            if items[row-1].weight > col: 
                knapsack[row][col] = knapsack[row-1][col]
            else:
                knapsack[row][col] = max(knapsack[row-1][col], knapsack[row-1][col - items[row-1].weight] + items[row-1].value)
    
    if debug: printMatrix(knapsack)
    
    return knapsack

def backTrace(items, knapsack, capacity):
    results = []
    for x in range(len(items), 0, -1):
        if debug: print("x: " + str(x) + " capacity: " + str(capacity) + " item val:" + str(knapsack[x][capacity]))
        if knapsack[x][capacity] != knapsack[x-1][capacity]:
            results.insert(0,1)
            capacity = capacity - items[x-1].weight
        else:
            results.insert(0,0)

    if debug: print(*results)
    return results

'''Input generation methods''' 
def generateWorstItemsList(length, capacity):
    itemsList = []
    while length > 0:
        randWeight = random.randint(1, capacity)
        randValue = int(round(randWeight * random.uniform(.1, 3)))
        randQuantity = random.randint(1, int(capacity * .20))
        if length - randQuantity < 0:
            randQuantity = random.randint(1, length)
        length -= randQuantity
        itemsList.append(item(randWeight, randValue, randQuantity))
    
    return itemsList

#generates lists with not lots of unique objects but many of the same
def generateDenseItemsList(length, capacity):
    itemsList = []
    while length > 0:
        randWeight = random.randint(1, capacity)
        randValue = int(round(randWeight * random.uniform(.1, 3)))
        randQuantity = random.randint(int(capacity * .20), int(capacity*.50))
        if length - randQuantity < 0:
            randQuantity = random.randint(1, length)
        length -= randQuantity
        itemsList.append(item(randWeight, randValue, randQuantity))

    
    return itemsList
#generates items list
def generateSparseItemsList(length, capacity):
    itemsList = []
    while length > 0:
        randWeight = random.randint(1, capacity)
        randValue = int(round(randWeight * random.uniform(.1, 3)))
        randQuantity = random.randint(1, int(capacity*.05))
        if length - randQuantity < 0:
            randQuantity = random.randint(1, length)
        length -= randQuantity
        itemsList.append(item(randWeight, randValue, randQuantity))

    return itemsList

'''Helper methods'''
def printMatrix(arr):
    print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in arr]))

def enumerateItems(items):
    newItems = []
    for x in range(len(items)):
        if items[x].quantity > 1:
            for i in range(items[x].quantity):
                newItems.append(item(items[x].weight, items[x].value, 1))
        else:
            newItems.append(item(items[x].weight, items[x].value, 1))


    return newItems


if __name__ == '__main__':
    main(sys.argv[1:])