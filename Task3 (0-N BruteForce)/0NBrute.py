import random
import sys
import math
import time
import csv

''' Helper globals '''
debug = False
test = True
default = False
printing = False


class item:
    def __init__(self, weight, value, quantity):
        self.weight = weight
        self.value = value
        self.quantity = quantity

def main(args):
    if test: 
        trials = 5
        for n in range(5, 25, 1):
            averageTime = 0.0
            totalTime = 0
            for trial in range(trials):
                items = [
                    item(7,47,1),
                    item(5,30,1),
                    item(5,25,1),
                    item(4,24,1),
                ]
                '''worst case would be where items is equal to weight capacity (n x n board)'''
                capacity = n
                #generate random item lists of length capacity

                items = generateWorstItemsList(n, n)

                if debug: print("Number of items: " + str(len(items)))

                #test time
                startTime = time.time()
                newItems = enumerateItems(items)
                knapsack = findAllCombinations(newItems)
                results = findBestCombination(knapsack, capacity)
                endTime = time.time()
                totalTime += endTime - startTime

                if printing:
                    #print items results here
                    print("Length of knapsack: ", len(knapsack))
                    print("Number of items: " , len(results[0]), " value: " , results[1])

                print("n:  " , n , " time: ", totalTime)
            averageTime = totalTime / trials
            print("n: ", n, " average time: ", averageTime)
            time.sleep(.5)
            #add to csv
            with open('0NBruteData.csv', 'a') as file : 
                    writer = csv.writer(file)
                    writer.writerow([n, averageTime])
        
    if default: 
        items = [
            item(7,47,1),
            item(5,30,1),
            item(5,25,1),
            item(4,24,1),
        ]
        capacity = 10
        allCombinations = findAllCombinations(items)
        # printCombinations(allCombinations)
        # print(allCombinations[1][0].value)
        results = findBestCombination(allCombinations, capacity)
        printBestCombination(results[0], results[1])


def findAllCombinations(items):
    if len(items) == 0:
        return [[]]

    totalCombinations = []
    for combs in findAllCombinations(items[1:]):
        totalCombinations += [combs, combs+[items[0]]]
    return totalCombinations

def findBestCombination(combinations, capacity):
    curBestValue = -1
    curBestCombo = None

    for x in range(len(combinations)):
        curValue = 0
        curWeight = 0
        for y in range(len(combinations[x])):
            curWeight += combinations[x][y].weight
            curValue += combinations[x][y].value
        if curWeight <= capacity and curValue > curBestValue:
            curBestCombo = combinations[x]
            curBestValue = curValue

    return [curBestCombo, curBestValue]


'''Input generation methods''' 
def generateWorstItemsList(length, capacity):
    itemsList = []
    while length > 0:
        randWeight = random.randint(1, capacity)
        randValue = int(round(randWeight * random.uniform(.1, 3)))
        randQuantity = random.randint(1, 7)
        if length - randQuantity < 0:
            randQuantity = random.randint(1, length)
        length -= randQuantity
        itemsList.append(item(randWeight, randValue, randQuantity))
    
    return itemsList

#generates lists with not many duplicate items
def generateSparseItemList(length, capacity):
    return None
#generates lists with many duplicate items
def generateDenseItemList(length, capacity):
    return None

'''Helper methods'''
def printCombinations(arr):
    # print('\n'.join([''.join([''.format(item.weight) for item in row]) for row in arr]))
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            print("weight: ", str(arr[x][y].weight), " value: " , str(arr[x][y].value))
        print("new list: ")

def printBestCombination(items, value):
    print( ''.join(value.weight) for value in items)
    print("Value: ", str(value))

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