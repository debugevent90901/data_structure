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
            for _ in range(index):
                cursor = cursor.getNext() 
            return cursor
        raise IndexError("DLinkedList index out of range")

    # modified in lab
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

    # original design
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

####################### bubbleSort ############################

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

####################### selectioSort ############################

    # sorting by swaping the items between nodes, not changing the nodes themselves
    def selectionSort_m(self):
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
    
    # in-place 
    # same as slides
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

####################### insertionSort ############################

    def insertionSort(self):
        cursor = self.first.getNext()
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        while cursor != self.first:
            # keep a record of the next cursor position
            cursor1 = cursor.getNext() 
            self.addout(cursor)
            cursor = cursor1

    # slightly modified
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

    # original code in lab
    # no need two conditions "cursor2 != self.first"
    # None <= evenything is True
    def addout_ori(self, cursor):
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

####################### mergeSort ############################

    # bugs in slide code, slightly modified
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


#  DN<=>A=>B=>C=>D=> ...=>Z
# ↑                     ↑ 
# first                 last
class LinkedList: 
    class __Node:
        def __init__(self,item,next=None):
            self.item=item 
            self.next=next 
        def getItem(self): 
            return self.item
        def getNext(self): 
            return self.next
        def getPrevious(self): 
            return self.previous
        def setItem(self,item): 
            self.item = item
        def setNext(self,next): 
            self.next = next
        def setPrevious(self,previous): 
            self.previous = previous
            
    def __init__(self,contents=[]):
        self.first = LinkedList.__Node(None,None)
        self.numItems = 0 
        self.first.setNext(self.first) 
        self.first.setPrevious(self.first)
        self.last = self.first
        for e in contents:
            self.append(e)
    
    def printList(self):
        tmp = self.first.next
        nodes = []
        for i in range(self.numItems):
            nodes.append(str(tmp.item))
            tmp = tmp.next
        print(' -> '.join(nodes))
        
    def getPrevious(self, cursor, node): 
        tmp = cursor
        while(tmp.next != node):
            tmp = tmp.next
        return tmp
    
    def append(self,item):
        lastNode = self.last
        newNode = LinkedList.__Node(item,self.first)
        lastNode.setNext(newNode) 
        self.first.setPrevious(newNode)
        self.last = newNode
        self.numItems += 1
        
    def locate(self,index):
        if index >= 0 and index < self.numItems:
            cursor = self.first.getNext() 
            for _ in range(index):
                cursor = cursor.getNext() 
            return cursor
        raise IndexError("LinkedList index out of range")
        
    def splice(self,index,other,index1,index2):
        if index1 <= index2:
            begin = other.locate(index1)
            end = other.locate(index2) 
            self.insertList(begin,end,index)
            self.numItems += index2 - index1 + 1
            
    def insertList(self,begin,end,index): 
        address = self.locate(index) 
        successor = address.getNext() 
        begin.setPrevious(address) 
        end.setNext(successor) 
        address.setNext(begin) 
        successor.setPrevious(end)
        
    def SelectionSort(self):
        firstNode = self.first.getNext()
        lastNode = self.last
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
                    lastNode = self.getPrevious(firstNode, location)
                else:
                    self.cut(firstNode,lastNode,location)
            self.addLocation(outlast,location)
            outlast = location
            self.last = location 
            counter -= 1
        self.last.next = None

   def getMinimum(self,first,last):  
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
    
    def cut(self,first,last,location):       
        prev = self.getPrevious(first, location)
        next = location.getNext()
        prev.setNext(next)
        next.setPrevious(prev)
        
    def addLocation(self,outlast,location):
        location.setPrevious(outlast)
        location.setNext(self.first)
        outlast.setNext(location)
        self.first.setPrevious(location)

    def InsertionSort(self):
        cursor = self.first.getNext()
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        while cursor != self.first:
            cursor1 = cursor.getNext()         
            self.addout(cursor)
            cursor = cursor1
        tmp = self.first.next
        for i in range(self.numItems-1):      
            tmp = tmp.next
        self.last=tmp                         
        self.last.next = None
        
    def addout(self,cursor):
        cursor2 = self.first.getNext()
        while (cursor2 != self.first and cursor2.getItem() < cursor.getItem() and cursor2.getNext() != self.first):
            cursor2 = cursor2.getNext()
        if cursor2 != self.first and cursor2.getItem() >= cursor.getItem():   
            previous = self.getPrevious(cursor, cursor2)
            previous.setNext(cursor)
            cursor.setNext(cursor2)
            cursor.setPrevious(previous)
            cursor2.setPrevious(cursor)
        else:                                      
            cursor2.setNext(cursor)
            cursor.setNext(self.first)
            cursor.setPrevious(cursor2)
            self.first.setPrevious(cursor)

class Block(list):
    def __init__(self,contents=[],next=None,previous=None):
        self.next = next 
        self.previous = previous
        
        self.item = [None] * 20 # the constant K
        self.numItems = 0
        self.size = 20
        for e in contents:
            self.append(e)
    
    # Original Node Class
    def getItem(self): 
        return self.item
    def getNext(self): 
        return self.next
    def getPrevious(self): 
        return self.previous
    def setItem(self,item): 
        self.item = item
    def setNext(self,next): 
        self.next = next
    def setPrevious(self,previous): 
        self.previous = previous
    
    # Original Pylist Class
    def __contains__(self,item):
        for i in range(self.numItems):
            if self.items[i] == item:
                return True
        return False

    def __eq__(self,other):
        if type(other) != type(self):
            return False
        if self.numItems != other.numItems:
            return False
        for i in range(self.numItems):
            if self.items[i] != other.items[i]:
                return False
        return True
    
    def __setitem__(self,index,val):
        if index >= 0 and index < self.numItems:
            self.item[index] = val
            return
        raise IndexError("Block assignment index out of range")

    def __getitem__(self,index):
        if index >= 0 and index < self.numItems:
            return self.item[index]
        raise IndexError("Block index out of range")
    
    def __add__(self,other):
        result = PyList(size=self.numItems+other.numItems)
        for i in range(self.numItems):
            result.append(self.items[i])
        for i in range(other.numItems):
            result.append(other.items[i])
        return result
    
    def append(self,item):
        self.items[self.numItems] = item
        self.numItems += 1
    
    def insert(self,i,x):
        if i < self.numItems:
            for j in range(self.numItems-1,i,-1):
                self.items[j+1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
        else:
            self.append(x)
    
    def delete(self,index):
        if index <= self.numItems:
            for j in range(index,self.numItems-1):
                self.items[j] = self.items[j+1]
            self.numItems -= 1
            self.items[self.numItems] = None
        else:
            raise IndexError("Block index out of range")

    def swap(self, l, r):
        temp = self[l]
        self[l] = self[r]
        self[r] = temp
        
    def InsertionSort(self):
        for i in range(1, self.numItems):
            for j in range(i, 0, -1):
                if self[j] > self[j-1]:
                    break
                self.swap(j, j-1)

class ListOfBlocks(Block):
    def __init__(self,contents=[]):
        self.first = Block() 
        self.numBlocks = 0 # num of blocks
        self.numItems = 0  # num of items
        self.first.setNext(self.first) 
        self.first.setPrevious(self.first)
        for e in contents:
            if e == None:
                break
            self.append(e)
            
    def __setitem__(self,index,val):
        if index < 0:
            index += self.numItems
        if index >= 0 and index < self.numItems:
            node = self.first.next
            cursor = 0
            while(cursor + node.numItems <= index):
                cursor += node.numItems
                node = node.next
            node.item[index - cursor] = val
            return
        raise IndexError("ListOfBlock assignment index out of range")

    def __getitem__(self,index):
        if index < 0:
            index += self.numItems
        if index >= 0 and index < self.numItems:
            node = self.first.next
            cursor = 0
            while(cursor + node.numItems <= index):
                cursor += node.numItems
                node = node.next
            return node.item[index - cursor]
        raise IndexError("ListOfBlock index out of range")
    
    def printList(self):
        tmp = self.first.next
        nodes = []
        for i in range(self.numBlocks):
            nodes.append(str(tmp.item))
            tmp = tmp.next
        print(' <-> '.join(nodes))
        
    def append(self,item):
        lastNode = self.first.getPrevious()
        # Add a new node with size 20 if the previous one is full
        if self.first.previous == self.first or self.first.previous.numItems == 20:
            newNode = Block(self.first,lastNode) 
            lastNode.setNext(newNode) 
            self.first.setPrevious(newNode)
            self.numBlocks += 1
            lastNode = self.first.getPrevious()
        lastNode.item[lastNode.numItems] = item
        lastNode.numItems += 1
        self.numItems += 1
    
    def insert(self, index, item):
        if index < 0:
            index += self.numItems
        if index >= 0 and index < self.numItems:
            node = self.first.next
            cursor = 0
            while(cursor + node.numItems <= index):
                cursor += node.numItems
                node = node.next
            if node.numItems < 20:
                for i in range(node.numItems - 1,index - cursor,-1):
                    node.items[i+1] = node.items[i]
                node.items[index - cursor] = item
                node.numItems += 1
            else:
                # add a new block if the current is full
                nextNode = node.getNext()
                newNode = Node(item,self.nextNode,node) 
                nextNode.setPrevious(newNode)
                node.setNext(newNode)
                self.numBlocks += 1
                # move the last item to the next block
                newNode.append(node[20])
                
                for i in range(node.numItems - 2,index - cursor,-1):
                    node.items[i+1] = node.items[i]
                node.items[index - cursor] = item
                node.numItems += 1
                self.numItems += 1
        elif index == self.numItems:
            self.append(x)
        raise IndexError("ListOfBlock index out of range")

    def delete(self, index):
        if index < 0:
            index += self.numItems
        if index >= 0 and index < self.numItems:
            node = self.first.next
            cursor = 0
            while(cursor + node.numItems <= index):
                cursor += node.numItems
                node = node.next
            if node.numItems == 1:
                lastNode = node.getPrevious()
                nextNode = node.getNext()
                lastNode.setNext(nextNode)
                nextNode.setprevious(lastNode)
            else:
                for i in range(index - cursor, node.numItems - 1):
                    node.items[i] = node.items[i+1]
                node.items[index - cursor] = item
                node.numItems -= 1
                self.numItems -= 1
        raise IndexError("ListOfBlock index out of range")
        
    def locate(self, index):
        if index >= 0 and index < self.numBlocks:
            result = self.first.next
            for i in range(index):
                result = result.next
            return result
        return IndexError("Block index out of range")
    
    def MergeSort(self):
        if self.numBlocks < 1:
            return self
        return self.mergeSort(0, self.numBlocks - 1)
    
    def mergeSort(self, l, r): 
        if l < r:
            m = (l+r)//2     
            sort1 = self.mergeSort(l, m) 
            sort2 = self.mergeSort(m + 1, r) 
            return self.merge(sort1, sort2)
        
        # Use Insertion Sort for each single block
        elif l == r:
            block = self.locate(l)
            block.InsertionSort()
            return ListOfBlocks(block.item)
        return IndexError("MergeSort index out of range")

    def merge(self, list1, list2):
        if list1.numItems == 0:
            return list2
        if list2.numItems == 0:
            return list1
        result = ListOfBlocks()
        i = j = 0
        while(i < list1.numItems or j < list2.numItems):
            if i >= list1.numItems:
                result.append(list2[j])
                j += 1
            elif j >= list2.numItems:
                result.append(list1[i])
                i += 1
            else:
                if (list1[i] < list2[j]):
                    result.append(list1[i])
                    i += 1
                else:
                    result.append(list2[j])
                    j += 1
        return result





