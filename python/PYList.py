# -*- coding: utf-8 -*-


class PyList(list):

    def __init__(self,contents = [], size = 20):
        self.items = [None] * size
        self.numItems = 0
        self.size = size
        for e in contents:
            self.append(e)
            
    def __contains__(self, item):
        for i in range(self.numItems):
            if self.items[i] == item:
                return True
        return False

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        if self.numItems != other.numItems:
            return False
        for i in range(self.numItems):
            if self.items[i] != other.items[i]:
                return False
        return True
    
    def __setitem__(self, index, val):
        if index >= 0 and index < self.numItems:
            self.items[index] = val
            return
        raise IndexError("PyList assignment index out of range")

    def __getitem__(self, index):
        if index >= 0 and index < self.numItems:
            return self.items[index]
        raise IndexError("PyList index out of range")
    
    def __add__(self, other):
        result = PyList(size = self.numItems + other.numItems)
        for i in range(self.numItems):
            result.append(self.items[i])
        for i in range(other.numItems):
            result.append(other.items[i])
        return result
    
    def append(self, item):
        if self.numItems == self.size:
            self.allocate()
        self.items[self.numItems] = item
        self.numItems += 1
    
    def insert(self, i, x):
        if self.numItems == self.size:
            self.allocate()
        if i < self.numItems:
            for j in range(self.numItems-1, i, -1):
                self.items[j+1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
        else:
            self.append(x)
    
    def delete(self, index):
        if self.numItems <= self.size / 4:
            self.deallocate()
        if index <= self.numItems:
            for j in range(index, self.numItems-1):
                self.items[j] = self.items[j+1]
            self.numItems -= 1
            self.items[self.numItems] = None
        else:
            raise IndexError("PyList index out of range")
        
    def allocate(self):
        newlength = 2 * self.size
        newList = [None] * newlength
        for i in range(self.numItems):
            newList[i] = self.items[i]
        self.items = newList
        self.size = newlength
        
    def deallocate(self):
        newlength = int(self.size / 2)
        newList = [None] * newlength
        for i in range(self.numItems):
            newList[i] = self.items[i]
        self.items = newList
        self.size = newlength

    def selectionSort(self):
        for i in range(self.numItems-1):
            minIndex = i
            for j in range(i+1, self.numItems):
                if self.items[minIndex] > self.items[j]:
                    minIndex = j
            if i == minIndex:
                continue
            else:
                self.items[i], self.items[minIndex] = self.items[minIndex], self.items[i]

    def bubbleSort(self):
        for i in range(self.numItems-1):
            for j in range(self.numItems-1-i):
                if self.items[j] > self.items[j+1]:
                    self.items[j], self.items[j+1] = self.items[j+1], self.items[j]

    # another bubbleSort
    '''
    def bubbleSort(self):
        while True:
            is_swaped = 0
            for i in range(self.numItems):
                if self.items[i] > self.items[i+1] and self.items[i+1] != None:
                    self.items[i], self.items[i+1] = self.items[i+1], self.items[i]
                    is_swaped += 1
            if is_swaped == 0:
                break
    '''

    def insertionSort(self):
        for i in range(1, self.numItems):
            left, right = 0, i-1
            tmp = self.items[i]
            while left <= right:
                mid = left + (right - left) / 2
                if self.items[mid] > tmp:
                    right = mid - 1
                else:
                    left = mid + 1
            for j in range(i-1, left-1, -1):
                self.items[j+1] = self.items[j]
            self.items[left] = tmp


a = PyList([2, 45, 11, 3, 67, 103, 34, 22, 1])
b = PyList([2, 45, 11, 3, 67, 103, 34, 22, 1])
c = PyList([2, 45, 11, 3, 67, 103, 34, 22, 1])
a.bubbleSort()
b.selectionSort()
c.insertionSort()
print(a.items)
print(b.items)
print(c.items)














