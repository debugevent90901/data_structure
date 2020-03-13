# -*- coding: utf-8 -*-

#  DN<=>A<=>B<=>C<=>D<=> ...<=>Z<=>(back to Dummy Node)
# ↑
# first

class DLinkedList: 
    class __Node:
        def __init__(self, item, next = None, previous = None):
            self.item = item 
            self.next = next 
            self.previous = previous
        def getItem(self): 
            return self.item
        def getNext(self): 
            return self.next
        def getPrevious(self): 
            return self.previous
        def setItem(self, item): 
            self.item = item
        def setNext(self, next): 
            self.next = next
        def setPrevious(self, previous): 
            self.previous = previous
            
    def __init__(self, contents = []):
        self.first = DLinkedList.__Node(None, None, None) 
        self.numItems = 0 
        self.first.setNext(self.first) 
        self.first.setPrevious(self.first)
        for e in contents:
            self.append(e)
    
    def printList(self):
        tmp = self.first.next
        nodes = []
        for i in range(self.numItems):
            nodes.append(str(tmp.item))
            tmp = tmp.next
        print(' <-> '.join(nodes))

    def append(self, item):
        lastNode = self.first.getPrevious()
        newNode = DLinkedList.__Node(item, self.first, lastNode) 
        lastNode.setNext(newNode) 
        self.first.setPrevious(newNode)
        self.numItems += 1
        
    def locate(self, index):
        if index >= 0 and index < self.numItems:
            cursor = self.first.getNext() 
            for _ in range(index):
                cursor = cursor.getNext() 
            return cursor
        raise IndexError("DLinkedList index out of range")
        
    def splice(self, index, other, index1, index2):
        if index1 <= index2:
            begin = other.locate(index1)
            end = other.locate(index2) 
            self.insertList(begin, end, index)
            self.numItems += index2 - index1 + 1
            
    def insertList(self, begin, end, index): 
        address = self.locate(index) 
        successor = address.getNext() 
        begin.setPrevious(address) 
        end.setNext(successor) 
        address.setNext(begin) 
        successor.setPrevious(end)
        
    # in-place
    def selectionSort(self):
        firstNode = self.first.getNext()
        lastNode = self.first.getPrevious()
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        counter = self.numItems
        outlast = self.first
        while counter != 0:
            location = self.getMinimum(firstNode,lastNode)
            if location == firstNode:
                firstNode = location.getNext()
            else:
                if location == lastNode:
                    lastNode = location.getPrevious()
                else:
                    self.cut(firstNode,lastNode,location)
            self.addLocation(outlast,location)
            outlast = location
            counter -= 1
            
    # getMinimum() determines the node with the minimum item
    def getMinimum(self, first, last):  
        minimum = first.getItem()
        cursor = first
        location = first
        while cursor != last:
            cursor = cursor.getNext()
            item = cursor.getItem()
            if item < minimum:
                minimum = item
                location = cursor
        return location
    
    #cut() deletes the node with the minimum item from the inlist:
    #location is actually the min node that you found
    def cut(self, first, last, location):      
        prev = location.getPrevious()
        next = location.getNext()
        prev.setNext(next)
        next.setPrevious(prev)
        
    # addLocation() adds the node with the minimum item to the outlist
    def addLocation(self, outlast, location):
        location.setPrevious(outlast)
        location.setNext(self.first)
        outlast.setNext(location)
        self.first.setPrevious(location)

    # in-place
    def insertionSort(self):
        cursor = self.first.getNext()
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        while cursor != self.first:
        	# keep a record of the next cursor position
            cursor1 = cursor.getNext() 
            self.addout(cursor)
            cursor = cursor1
    
    # no need two conditions "cursor2 != self.first"
    # None <= evenything is True
    def addout(self, cursor):
        cursor2 = self.first.getNext()
        while cursor2 != self.first and cursor2.getItem() < cursor.getItem() and cursor2.getNext() != self.first:
            cursor2 = cursor2.getNext()
        # insert before cursor2
        if cursor2 != self.first and cursor2.getItem() >= cursor.getItem(): 
            previous = cursor2.getPrevious()
            previous.setNext(cursor)
            cursor.setNext(cursor2)
            cursor.setPrevious(previous)
            cursor2.setPrevious(cursor)
        # insert at the end of the output
        else:                                   
            cursor2.setNext(cursor)
            cursor.setNext(self.first)
            cursor.setPrevious(cursor2)
            self.first.setPrevious(cursor)


    def mergeSort(self, threshold):
        if self.numItems <= threshold:
            self.insertionSort()
        else:
            secondList = self.split()
            self.mergeSort(threshold)
            secondList.mergeSort(threshold)
            self.merge(secondList)

    def split(self):
        index = self.numItems / 2
        cursor = self.locate(index)
        secondList = DLinkedList([])
        lastNode1, lastNode2 = cursor.getPrevious(), self.first.getPrevious()
        self.first.setPrevious(lastNode1)
        lastNode1.setNext(self.first)
        secondList.first.setNext(cursor)
        cursor.setPrevious(secondList.first)
        lastNode2.setNext(secondList.first)
        secondList.first.setPrevious(lastNode2)
        secondList.numItems = self.numItems - index
        self.numItems = index
        return secondList

    def merge(self, other):
        firstNode, secondNode = self.first.getNext(), other.first.getNext()
        self.numItems = self.numItems + other.numItems
        current = self.first
        count = 1
        while count <= self.numItems:
            if firstNode.getItem() != None and secondNode.getItem() != None:
                if firstNode.getItem() <= secondNode.getItem():
                    current.setNext(firstNode)
                    firstNode.setPrevious(current)
                    firstNode = firstNode.getNext()
                else:
                    current.setNext(secondNode)
                    secondNode.setPrevious(current)
                    secondNode = secondNode.getNext()
            else:
                if firstNode.getItem() == None:
                    current.setNext(secondNode)
                    secondNode.setPrevious(current)
                    secondNode = secondNode.getNext()
                else:
                    current.setNext(firstNode)
                    firstNode.setPrevious(current)
                    firstNode = firstNode.getNext()
            count += 1
            current = current.getNext()
