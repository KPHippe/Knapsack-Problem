import random
import sys
import math
import time
import csv
import copy

''' Helper globals '''
debug = False
test = True
testLowCapacity = False
default = False
printing = False

class item:
    def __init__(self, weight, value, quantity, index):
            self.weight = weight
            self.value = value
            self.quantity = quantity
            self.index = index
            self.worth = value / weight
        
    def __eq__(self, other):
        return not self.worth<other.worth and not other.worth< self.worth
    def __ne__(self, other):
        return self.worth<other.worth or other.worth < self.worth
    def __gt__(self, other):
        return other.worth < self.worth
    def __ge__(self, other):
        return not self.worth<other.worth
    def __le__(self, other):
        return not other.worth<self.worth
    def __lt__(self, other):
        return self.worth<other.worth


class node: 
    def __init__(self, items, curWeight, curValue, children):
        # self.parents = parents
        self.items = items
        self.children = children
        self.curWeight = curWeight
        self.curValue = curValue

    def addChildren(self, node):
        self.children.append(node)
        # node.parents.append(self)



'''Globals to help with recursion'''
maxNode = node([],0,0,[])
maxValue = 0
allNodes = {}

def main(args):
    global maxNode
    global maxValue
    global allNodes
    if test:
        trials = 5
        for n in range(100, 1001, 100):
            averageTime = 0.0
            totalTime = 0
            for trial in range(trials):
                '''worst case would be where items is equal to weight capacity (n x n board)'''
                capacity = n
                if testLowCapacity:
                    #makes it so the capacity is 10% of N, will make graph search much faster
                    capacity = int(capacity * .1 )
                #generate random item lists of length capacity
                items = generateDenseItemsList(n, n)

                #test time
                startTime = time.time()

                firstItemsList = [0 for x in range(len(items))]
                firstNode = node(firstItemsList, 0, 0, [])
                #start the search
                search(firstNode, capacity, items)

                endTime = time.time()
                totalTime += endTime - startTime
                '''add some sort of printing here'''

                print(totalTime)
            averageTime = totalTime / trials
            print("n: ", n, " average time: ", averageTime)
            #add to csv
            with open('0NGraphRandomSparse.csv', 'a') as file : 
                    writer = csv.writer(file)
                    writer.writerow([n, averageTime])


    if default:
            capacity = 30
            items = [
                item(7,47,1,0),
                item(5,30,3,1),
                item(5,25,3,2),
                item(4,24,3,3),
            ]

            items.sort(reverse = True)
            if debug: 
                for i in range(len(items)):
                    print("Item " , i, " Value: " , items[i].worth, " origIndex: " , items[i].index)
            currentMaxNode = None
            # #generate first node
            firstItemsList = [0 for x in range(len(items))]
            firstNode = node(firstItemsList, 0, 0, [])
            #start the search
            search(firstNode, capacity, items)
            
            #found everything, now print it out
            print("**************\n\nMaxNode value: ", str(maxNode.curValue))
            print(''.join(str(i) for i in maxNode.items))
            print("Greedy choice: " , str(greedyCheck(items, capacity)))

def search(rootNode, totalCapacity, items):
    global maxNode
    global maxValue
    global allNodes
    #add current node to visited dictionary
    allNodes[tuple(rootNode.items)] = [rootNode.curWeight, rootNode.curValue]
    if debug: print("Length of allnodes: ", str(len(allNodes)))
    #generate children
    generateChildren(rootNode, items, totalCapacity)
    if debug: print("Length of children: " , str(len(rootNode.children)))
    for i in range(len(rootNode.children)):
        if rootNode.children[i].curValue > maxValue:
            maxValue = rootNode.children[i].curValue
            maxNode = rootNode.children[i]
            if debug: print("Current max value: " , str(maxValue), " CurrentMaxNode value: " , str(maxNode.curValue))
        
        search(rootNode.children[i], totalCapacity, items)
    

def generateChildren(curNode, items, totalCapacity):
    global allNodes
    for i in range(len(curNode.items)):
        #check if the quantity of current item has not been reached
        if curNode.items[i] < items[items[i].index].quantity:
            #generate new state, if weight allows
            #only add new child if weight is acceptable
            if curNode.curWeight + items[items[i].index].weight <= totalCapacity:
                copyItemsList = list(copy.deepcopy(curNode.items))
                copyItemsList[i] += 1
                #if this state hasn't already been 'visited' continue to making new state
                if tuple(copyItemsList) not in allNodes:
                    tempWeight = curNode.curWeight + items[items[i].index].weight
                    tempVal = curNode.curValue + items[items[i].index].value
                    #check if the val is less than the current greedy solution
                    #if it is less don't add to the list
                    '''remove if complexity gets too large'''
                    if tempVal >= greedyCheck(items, tempWeight):
                        tempNode = node(copyItemsList, tempWeight, tempVal, [])
                        curNode.children.append(tempNode)


def greedyCheck(items, curWeight):
    finalVal = 0
    for i in range(len(items)):
        for j in range(items[items[i].index].quantity):
            if items[items[i].index].weight <= curWeight:
                curWeight -= items[items[i].index].weight
                finalVal += items[items[i].index].value
    
    return finalVal

'''Input generation methods''' 
def generateWorstItemsList(length, capacity):
    itemsList = []
    index = 0
    while length > 0:
        randWeight = random.randint(1, capacity)
        randValue = int(round(randWeight * random.uniform(.1, 3)))
        randQuantity = random.randint(1, int(capacity * .20))
        if length - randQuantity < 0:
            randQuantity = random.randint(1, length)
        length -= randQuantity
        itemsList.append(item(randWeight, randValue, randQuantity, index))
        index += 1
    
    return itemsList

#generates lists with not lots of unique objects but many of the same
def generateDenseItemsList(length, capacity):
    itemsList = []
    index = 0
    while length > 0:
        randWeight = random.randint(1, capacity)
        randValue = int(round(randWeight * random.uniform(.1, 3)))
        randQuantity = random.randint(int(capacity * .20), int(capacity*.50))
        if length - randQuantity < 0:
            randQuantity = random.randint(1, length)
        length -= randQuantity
        itemsList.append(item(randWeight, randValue, randQuantity, index))
        index += 1
    
    return itemsList
#generates items list
def generateSparseItemsList(length, capacity):
    itemsList = []
    index = 0
    while length > 0:
        randWeight = random.randint(1, capacity)
        randValue = int(round(randWeight * random.uniform(.1, 3)))
        randQuantity = random.randint(1, int(capacity * .05))
        if length - randQuantity < 0:
            randQuantity = random.randint(1, length)
        length -= randQuantity
        itemsList.append(item(randWeight, randValue, randQuantity, index))
        index += 1
    
    return itemsList

if __name__ == '__main__':
    main(sys.argv[1:])
