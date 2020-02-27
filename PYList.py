# -*- coding: utf-8 -*-
# main.py


class PyList(list):
    def __init__(self, content=[], size = 20):
        self.items = [None]*size
        self.numItems = 0
        self.size = size
        for e in content:
            self.append(e)

    def __contains__(self,item):
        for i in range(self.numItems):
            if self.items[i] == item:
                return True
            return False

    def __eq__(self,other):
        if (type(self) != type(other)):
            return False
        if self.numItems != other.numItems:
            return False
        for i in range(self.numItems):
            if (self.items[i] != other.items[i]):
                return False
        return True

    def __setitem__(self,index,val):
        if index >= 0 and index <= self.numItems-1:
            self.items[index] = val
            return
        raise IndexError("Pylist assignment index out of range.")

    def __getitem__(self,index):
        if index >= 0 and index <= self.numItems-1:
            return self.items[index]
        raise IndexError("Pylist index out of range.")

    def append(self,item):
        if self.numItems == self.size:
            self.allocate()
        self.items[self.numItems] = item
        self.numItems += 1

    def __add__(self,other):
        result = PyList(size=self.numItems+other.numItems)
        for i in range(self.numItems):
            result.append(self.items[i])
        for i in range(other.numItems):
            result.append(self.items[i])
        return result

    def insert(self,i,x):
        if self.numItems == self.size:
            self.allocate()
        if i < self.numItems:
            for j in range(self.numItems-1,i,-1):
                self.items[j+1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
        else:
            self.append(x)

    def delete(self,index):
        if (self.numItems == self.size/4):
            self.deallocate()
        if index >= self.numItems:
            raise IndexError("PyList index out of range.")
        else:
            for i in range(index,self.numItems-1):
                self.items[i] = self.items[i+1]
            self.numItems -= 1
            return

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

    def delete_last(self,k):
        if k>self.numItems:
            self.numItems = 0
            self.size = 1
            self.items = [None]*self.size
            return
        else:
            rest = self.numItems - k
            self.numItems = rest
            while (self.numItems <= int(self.size/4)):
                self.deallocate()
            return
        return


if __name__ == "__main__":
    a = list(range(128))
    pylist = PyList(a,128)
    for i in range(pylist.numItems):
        print(pylist.items[i])
    print("-------")
    pylist.delete_last(125)
    for i in range(pylist.numItems):
        print(pylist.items[i])
    print(pylist.size)