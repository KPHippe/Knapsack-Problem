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
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value



def main(args):
    #do stuff here
    if test: 
        trials = 5
        for n in range(100, 1001, 100):
            averageTime = 0.0
            totalTime = 0
            for trial in range(trials):
                items = [
                    item(1,29),
                    item(7,49),
                    item(5,30),
                    item(5,25),
                    item(4,24)
                ]
                '''worst case would be where items is equal to weight capacity (n x n board)'''
                capacity = n
                #generate random item lists of length capacity

                items = generateWorstItemsList(n, n)

                if debug: print("Number of items: " + str(len(items)))
                print("Number of items: " + str(len(items)))

                #test time
                startTime = time.time()
                knapsack = pickItems(items, capacity)
                if debug: print("Table size: " + str(len(knapsack)) + ", " + str(len(knapsack[0])))
                results = backTrace(items, knapsack, capacity)
                endTime = time.time()
                totalTime += endTime - startTime

                if printing:
                    #print items results here
                    print(*results)

                print(totalTime)
            averageTime = totalTime / trials
            print("n: ", n, " average time: ", averageTime)
            time.sleep(.5)
            #add to csv
            with open('01DynamicData.csv', 'a') as file : 
                    writer = csv.writer(file)
                    writer.writerow([n, averageTime])
        


    if default: 
        capacity = 20
        items = [
            item(3,10),
            item(3,10),
            item(4,15),
            item(4,15),
            item(4,15),
            item(2,8),
            item(2,8)
        ]
        knapsack = pickItems(len(items), capacity)
        results = backTrace(items, knapsack, capacity)

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
    for x in range(length):
        randWeight = random.randint(1, capacity)
        randValue = int(round(randWeight * random.uniform(.1, int(capacity * .20))))
        itemsList.append(item(randWeight, randValue))

    return itemsList       


'''Helper printing methods'''
def printMatrix(arr):
    print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in arr]))



if __name__ == '__main__':
    main(sys.argv[1:])