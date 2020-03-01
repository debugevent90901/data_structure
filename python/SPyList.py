# -*- coding: utf-8 -*-
# aka cs225 lab1

from PyList import PyList

class SPyList(PyList):

    def __init__(self, contents = [], size = 10):
        self.items = [None] * size
        self.keys = []                         			        
        self.numItems = 0
        self.size = size
        for e in contents:
            self.append(e)
    
    def append(self, item):
        if type(item) is not dict:
        	raise TypeError("Wrong Element Tpye, dict Type Expected")
        if item['key'] in self.keys:      				
            raise KeyError("Key already exists")
        if self.numItems == self.size:
            self.allocate()
        self.items[self.numItems] = item
        self.numItems += 1
        self.keys.append(item['key'])           		
        
    def __setitem__(self, index, val):
        if type(val) is not dict:
            raise TypeError("Wrong Element Tpye, dict Type Expected")
        if index >= 0 and index < self.numItems:
            old_key = self.items[index]['key']          
            if val['key'] != old_key and val['key'] in self.keys:
                raise KeyError("Key already exists")
            self.keys.remove(old_key)
            self.keys.append(val['key'])
            self.items[index] = val
            return
        raise IndexError("PyList assignment index out of range")
        
    def __add__(self, other):
        raise SyntaxError("Add operation not defined")
        
    def insert(self, i, x):
        if type(x) is not dict:
            raise TypeError("Wrong Element Tpye, dict Type Expected")
        if x['key'] in self.keys:                     
            raise KeyError("Key already exists")
        if self.numItems == self.size:
            self.allocate()
        if i < self.numItems:
            for j in range(self.numItems-1, i-1, -1):
                self.items[j+1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
            self.keys.append(x['key'])
        else:
            self.append(x)
            
    def projection(self, projectList):
        newContent = []
        for item in self.items:
            if item == None:
                continue
            newItem = {}
            for key in item.keys():
                if key in projectList:
                	newItem[key] = item[key]
            newContent.append(newItem)
        return PyList(newContent)
    
    def projection_m(self, projectList):
        newContent = []
        for item in self.items:
            if item == None:
                continue
            newItem = {}
            for key in item.keys():
                if key in projectList:
                    newItem[key] = item[key]
            newContent.append(newItem)
        # If there are duplicated elements, raise an error
        for i in range(len(newContent) - 1):
            if (newContent[i] in newContent[i+1:]):
                raise ValueError("Duplicated records after projection")
        return PyList(newContent)

    def equi_join(self, other):
        if type(other) is not SPyList:
            raise TypeError("Wrong Argument Tpye, SPyList Type Expected")
        newContent = []
        for selfItem in self.items:
            if selfItem == None:
                continue
            for otherItem in other.items:
                if otherItem == None:
                    continue
                commonKeys = set(selfItem.keys()).intersection(set(otherItem.keys()))		# When calculating the time complexity, don't use this function
                continueFlag = 0
                for key in commonKeys:
                    if selfItem[key] != otherItem[key]:
                        continueFlag  = 1
                        break
                if continueFlag:
                    continue
                joinRecord = selfItem.copy()
                for otherKey in set(otherItem.keys()).difference(set(selfItem.keys())):		# When calculating the time complexity, don't use this function
                    joinRecord[otherKey] = otherItem[otherKey]
                newContent.append(joinRecord)
        return SPyList(newContent)

def test1():
	s = SPyList([{'key':1,'A':'a','X':'x'},{'key':2,'B':'b','Y':'y'},{'key':3,'C':'c','Z':'z'}])
	s.insert(0,{'key':5,'A':'a','X':'x'})             #insert a new record with a new key
	#s.insert(0,{'key':3,'A':'a','X':'x'})            #insert a new record with existed key
	s[0] = {'key':8,'A':'a','F':'f'}                  #assign values with a new key
	#s[0] = {'key':3,'A':'a','X':'x'}                 #assign values with existed key
	#s.insert(1,{'key':1,'A':'a','X':'x'})            #insert with exsited key
	print(s.items)

def test2():
	s = SPyList([{'key':1,'A':'a','X':'x','Y':'y'},{'key':2,'B':'b','Y':'y'},{'key':3,'C':'c','Z':'z'}])
	#s_p1 = s.projection(['key', 'A', 'Y'])
	#print(s_p1.items)
	s_p2 = s.projection_m(['key', 'A', 'Y'])
	print(s_p2.items)
	s_p3 = s.projection_m(['A', 'Y'])
	print(s_p3.items)
	#s_p4 = s.projection_m(['Y'])
	#print(s_p4.items)

def test3():
	s1 = SPyList([{'key':1,'A':'a','X':'x','Y':'y'},{'key':2,'B':'b','Y':'y'},{'key':3,'C':'c','Z':'z'}])
	s2 = SPyList([{'key':1,'A':'a','X':'x','Z':'z'},{'key':2,'B':'c','X':'x'},{'key':3,'C':'c','X':'x','Y':'y'},{'key':4,'D':'d','Z':'z'}])
	s3 = s1.equi_join(s2)
	print(s3.items)

def main():
	#test1()
	#test2()
	test3()

if __name__ == "__main__":
    main()












