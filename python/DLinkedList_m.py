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
        print("The DLinkedList has %d items" %self.numItems)
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
            for i in range(index):
                cursor = cursor.getNext() 
            return cursor
        raise IndexError("DLinkedList index out of range")

    def splice(self, index, other, index1, index2, insert_en = True):
        if index1 <= index2:
            if insert_en:
                begin = other.locate(index1)
                end = other.locate(index2)
                self.insertList(begin, end, index)
                self.numItems += index2 - index1 + 1
            # If there is no insertion, then cut the self list by index1 and index2
            else:
                begin = self.locate(index1)
                end = self.locate(index2)
                self.first.setPrevious(end)
                self.first.setNext(begin) 
                begin.setPrevious(self.first)
                end.setNext(self.first)
                self.numItems = index2 - index1 + 1

    def insertList(self, begin, end, index): 
        address = self.locate(index) 
        successor = address.getNext() 
        begin.setPrevious(address) 
        end.setNext(successor) 
        address.setNext(begin) 
        successor.setPrevious(end)

    def bubbleSort(self):
		while True:
			is_swaped = 0
			ptr = self.first.getNext()
			while ptr != self.first:
				if ptr.item > ptr.getNext().item and ptr.getNext().item != None:
					ptr.item, ptr.getNext().item = ptr.getNext().item, ptr.item
					is_swaped += 1
				ptr = ptr.getNext()
			if is_swaped == 0:
				break

    def selectionSort(self):
		cursor1 = self.first.getNext()
		while cursor1.getNext() != self.first:
			minNode = cursor1
			cursor2 = cursor1.getNext()
			while cursor2 != self.first:
				if minNode.getItem() > cursor2.getItem():
					minNode = cursor2
				cursor2 = cursor2.getNext()
			if cursor1 == minNode:
				cursor1 = cursor1.getNext()
			else:
				tmp = cursor1.getItem()
				cursor1.setItem(minNode.getItem())
				minNode.setItem(tmp)
				cursor1 = cursor1.getNext()

    def insertionSort(self):
        cursor = self.first.getNext()
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        while cursor != self.first:
        	# keep a record of the next cursor position
            cursor1 = cursor.getNext() 
            self.addout(cursor)
            cursor = cursor1
        
    def addout(self, cursor):
        cursor2 = self.first.getNext()
        while cursor2.getItem() < cursor.getItem() and cursor2.getNext() != self.first:
            cursor2 = cursor2.getNext()
        # insert before cursor2
        if cursor2.getItem() >= cursor.getItem(): 
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