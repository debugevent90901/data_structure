# -*- coding: utf-8 -*-

class HashSet:
    def __init__(self, contents = []):
        self.items = [None] * 20
        self.numItems = 0
        for e in contents:
            self.add(e)
            
    def add(self, item):
        if HashSet.__add(item, self.items):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= 0.75:
                self.items = HashSet.__rehash(self.items, [None]*2*len(self.items))
                
    def __contains__(self, item):
        index = hash(item) % len(self.items)
        while self.items[index] != None:
            if self.items[index] == item:
                return True
            index = (index + 1) % len(self.items)
        return False
    
    def delete(self, item):
        if HashSet.__remove(item, self.items):
            self.numItems -= 1
            load = max(self.numItems,20) / len(self.items)
            if load <= 0.25:
                self.items = HashSet.__rehash(self.items, [None]*(len(self.items) // 2))
        else:
            raise KeyError("Item not in HashSet")

    # FROM LAB checking of equality of sets or subsets and operations for set union, intersection and difference
    def __eq__(self, other):
        if self.numItems != other.numItems:
            return False
        # Loop over the items of *other*
        for otherItem in other.items:
            if otherItem != None and type(otherItem) != HashSet.__Placeholder:
                if not self.__contains__(otherItem):
                    return False
        return True
    
    def union(self, other):
        newContents = []
        for selfItem in self.items:
            if selfItem != None and type(selfItem) != HashSet.__Placeholder:
                newContents.append(selfItem)
        for otherItem in other.items:
            if otherItem != None and type(otherItem) != HashSet.__Placeholder:
                if otherItem not in newContents:
                    newContents.append(otherItem)
        return HashSet(newContents)
    
    def intersection(self, other):
        newContents = []
        for selfItem in self.items:
            if selfItem != None and type(selfItem) != HashSet.__Placeholder:
                if other.__contains__(selfItem):
                    newContents.append(selfItem)
        return HashSet(newContents)
    
    def difference(self, other):
        newContents = []
        for selfItem in self.items:
            if selfItem != None and type(selfItem) != HashSet.__Placeholder:
                if not other.__contains__(selfItem):
                    newContents.append(selfItem)
        return HashSet(newContents)

    # ===== Hidden Class =====
    class __Placeholder:
        def __init__(self):
            pass
        
        def __eq__(self, other):
            return False
    
    # ===== Auxiliary Functions =====
    # They all have '__' as prefixes to indicate that they are private methods to the class
    def __add(item, items):
        index = hash(item) % len(items)
        location = -1
        while items[index] != None:
            if items[index] == item:
                return False
            if location < 0 and type(items[index]) == HashSet.__Placeholder:
                location = index
            index = (index + 1) % len(items)
        if location < 0:
            location = index
        items[location] = item
        return True

    def __rehash(olditems, newitems):
        for e in olditems:
            if e != None and type(e) != HashSet.__Placeholder:
                HashSet.__add(e, newitems)
        return newitems

    def __remove(item, items):
        index = hash(item) % len(items)
        while items[index] != None:
            if items[index] == item:
                nextIndex = (index + 1) % len(items)
                if items[nextIndex] == None:
                    items[index] = None
                else:
                    items[index] = HashSet.__Placeholder()
                return True
            index = (index + 1) % len(items)
        return False

#######################################################################
#######################################################################
#######################################################################

class HashSet_m:
    def __init__(self, contents = [], loadMax = 0.75, loadMin = 0.25):
        self.items = [None] * 20
        self.numItems = 0
        self.loadMax = loadMax
        self.loadMin = loadMin
        for e in contents:
            self.add(e)
            
    def add(self, item):
        if HashSet_m.__add(item, self.items):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= self.loadMax: 
                self.items = HashSet_m.__rehash(self.items, [None]*2*len(self.items))
                
    def __contains__(self, item):
        index = hash(item) % len(self.items)
        while self.items[index] != None:
            if self.items[index] == item:
                return True
            index = (index + 1) % len(self.items)
        return False
    
    def delete(self, item):
        if HashSet_m.__remove(item, self.items):
            self.numItems -= 1
            load = max(self.numItems,20) / len(self.items)
            if load <= self.loadMin: # Modification
                self.items = HashSet_m.__rehash(self.items, [None]*(len(self.items) // 2))
        else:
            raise KeyError("Item not in HashSet")
    
    def __eq__(self, other):
        if self.numItems != other.numItems:
            return False
        # Loop over the items of *other*
        for otherItem in other.items:
            if otherItem != None and type(otherItem) != HashSet_m.__Placeholder:
                if not self.__contains__(otherItem):
                    return False
        return True
    
    def union(self, other):
        newContents = []
        for selfItem in self.items:
            if selfItem != None and type(selfItem) != HashSet_m.__Placeholder:
                newContents.append(selfItem)
        for otherItem in other.items:
            if otherItem != None and type(otherItem) != HashSet_m.__Placeholder:
                if otherItem not in newContents:
                    newContents.append(otherItem)
        return HashSet_m(newContents)
    
    def intersection(self, other):
        newContents = []
        for selfItem in self.items:
            if selfItem != None and type(selfItem) != HashSet_m.__Placeholder:
                if other.__contains__(selfItem):
                    newContents.append(selfItem)
        return HashSet_m(newContents)
    
    def difference(self, other):
        newContents = []
        for selfItem in self.items:
            if selfItem != None and type(selfItem) != HashSet_m.__Placeholder:
                if not other.__contains__(selfItem):
                    newContents.append(selfItem)
        return HashSet_m(newContents)

    def __getitem__(self, item):
        idx = hash(item) % len(self.items)
        while self.items[idx] != None:
            if self.items[idx] == item:
                return self.items[idx]
            idx = (idx + 1) % len(self.items)
        return None

    # ===== Hidden Class =====
    class __Placeholder:
        def __init__(self):
            pass
        
        def __eq__(self,other):
            return False
    
    # ===== Auxiliary Functions =====
    # They all have '__' as prefixes to indicate that they are private methods to the class
    def __add(item, items):
        index = hash(item) % len(items)
        location = -1
        while items[index] != None:
            if items[index] == item:
                return False
            if location < 0 and type(items[index]) == HashSet_m.__Placeholder:
                location = index
            index = (index + 1) % len(items)
        if location < 0:
            location = index
        items[location] = item
        return True

    def __rehash(olditems, newitems):
        for e in olditems:
            if e != None and type(e) != HashSet_m.__Placeholder:
                HashSet_m.__add(e,newitems)
        return newitems

    def __remove(item, items):
        index = hash(item) % len(items)
        while items[index] != None:
            if items[index] == item:
                nextIndex = (index + 1) % len(items)
                if items[nextIndex] == None:
                    items[index] = None
                else:
                    items[index] = HashSet_m.__Placeholder()
                return True
            index = (index + 1) % len(items)
        return False

#######################################################################
#######################################################################
#######################################################################

class HashSetChaining:
    def __init__(self, contents = [], loadMax = 0.75, loadMin = 0.25):
        self.items = [None] * 20
        self.numItems = 0
        self.loadMax = loadMax
        self.loadMin = loadMin
        for e in contents:
            self.add(e)
            
    def add(self, item):
        if HashSetChaining.__add(item, self.items):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= self.loadMax:
                self.items = HashSetChaining.__rehash(self.items, [None]*2*len(self.items))
                
    def __contains__(self, item):
        index = hash(item) % len(self.items)
        if self.items[index] == None or type(self.items[index]) == HashSetChaining.__Placeholder:
            return False
        if item in self.items[index]:
            return True
        return False
    
    def delete(self, item):
        if HashSetChaining.__remove(item, self.items):
            self.numItems -= 1
            load = max(self.numItems,20) / len(self.items)
            if load <= self.loadMin:
                self.items = HashSetChaining.__rehash(self.items, [None]*(len(self.items) // 2))
        else:
            raise KeyError("Item not in HashSet")
    
    def __eq__(self, other):
        if self.numItems != other.numItems:
            return False
        # Loop over the items of *other*
        for otherChain in other.items:
            if otherChain != None and type(otherChain) != HashSetChaining.__Placeholder:
                for otherItem in otherChain:
                    if not self.__contains__(otherItem):
                        return False
        return True
    
    def union(self, other):
        newContents = []
        for selfChain in self.items:
            if selfChain != None and type(selfChain) != HashSetChaining.__Placeholder:
                for selfItem in selfChain:
                    newContents.append(selfItem)
        for otherChain in other.items:
            if otherChain != None and type(otherChain) != HashSetChaining.__Placeholder:
                for otherItem in otherChain:
                    if otherItem not in newContents:
                        newContents.append(otherItem)
        return HashSetChaining(newContents)
    
    def intersection(self, other):
        newContents = []
        for selfChain in self.items:
            if selfChain != None and type(selfChain) != HashSetChaining.__Placeholder:
                for selfItem in selfChain:
                    if other.__contains__(selfItem):
                        newContents.append(selfItem)
        return HashSetChaining(newContents)
    
    def difference(self, other):
        newContents = []
        for selfChain in self.items:
            if selfChain != None and type(selfChain) != HashSetChaining.__Placeholder:
                for selfItem in selfChain:
                    if not other.__contains__(selfItem):
                        newContents.append(selfItem)
        return HashSetChaining(newContents)

    # ===== Hidden Class =====
    class __Placeholder:
        def __init__(self):
            pass
        
        def __eq__(self,other):
            return False
    
    # ===== Auxiliary Functions =====
    # They all have '__' as prefixes to indicate that they are private methods to the class
    def __add(item, items):
        index = hash(item) % len(items)
        if items[index] == None:
            items[index] = []
        if item in items[index]:
            return False
        items[index].append(item)
        return True

    def __rehash(olditems, newitems):
        for chain in olditems:
            if chain != None and type(chain) != HashSetChaining.__Placeholder:
                for e in chain:
                    HashSetChaining.__add(e,newitems)
        return newitems

    def __remove(item, items):
        index = hash(item) % len(items)
        if item in items[index]:
            items[index].remove(item)
            # If the list is empty, replace it with a placeholder
            if items[index] == []:
                items[index] = HashSetChaining.__Placeholder()
            return True
        return False

#######################################################################
#######################################################################
#######################################################################

class HashMap:
    class __KVPair:
        def __init__(self, key, value):
            self.key = key
            self.value = value
        
        def __eq__(self, other):
            if type(self) != type(other):
                return False
            return self.key == other.key
        
        def getKey(self):
            return self.key
        
        def getValue(self):
            return self.value
        
        def __hash__(self):
            return hash(self.key)
    
    def __init__(self):
        self.hSet = HashSet_m()
    
    def __len__(self):
        return len(self.hSet)
    
    def __contains__(self, item):
        return HashMap.__KVPair(item, None) in self.hSet
    
    def not__contains__(self, item):
        return item not in self.hSet
    
    def __setitem__(self, key, value):
        self.hSet.add(HashMap.__KVPair(key, value))
    
    def __getitem__(self, key):
        if HashMap.__KVPair(key, None) in self.hSet:
            val = self.hSet[HashMap.__KVPair(key, None)].getValue()
            return val
        raise KeyError("Key " + str(key) + " not in HashMap")
    
    def __iter__(self):
        for x in self.hSet:
            yield x.getKey()




