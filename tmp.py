# -*- coding: utf-8 -*-

from collections import deque

class bptNode:
    def __init__(self, parameter, isLeaf):
        self.parent = None
        if isLeaf == True:
            self.isLeaf = True
            self.loadFactor = parameter
            self.items = []
            self.next = None
        else:
            self.isLeaf = False
            self.order = parameter
            self.children = []  
            self.indice = []

    def isFull(self):
        if self.isLeaf == True:
            return len(self.items) > self.loadFactor
        else:
            return len(self.indice) >= self.order - 1

    def isEmpty(self):
        if self.isLeaf == True:
            return len(self.items) <= (self.loadFactor + 1) / 2 
        else:
            return len(self.indice) <= (self.order + 1) / 2 - 1

class bPlusTree:
    def __init__(self, order, loadFactor): 
        if loadFactor > order:
            raise ValueError('loadFactor must be less or equal then order')
        else:
            self.order = order
            self.loadFactor = loadFactor
            self.root = bptNode(loadFactor, True)
            self.leaf = self.root

    def insert(self, element):

        def split_node(oldNode):
            mid = self.order // 2
            newNode = bptNode(self.order, False)
            newNode.indice = oldNode.indice[mid:]
            newNode.children = oldNode.children[mid:]
            newNode.parent = oldNode.parent

            for child in newNode.children:
                child.parent = newNode

            if oldNode.parent is None:
                newRoot = bptNode(self.order, False)
                newRoot.indice = [oldNode.indice[mid - 1]]
                newRoot.children = [oldNode, newNode]
                oldNode.parent = newNode.parent = newRoot
                self.root = newRoot
            else:
                i = oldNode.parent.children.index(oldNode)
                oldNode.parent.indice.insert(i, oldNode.indice[mid - 1])
                oldNode.parent.children.insert(i + 1, newNode)

            oldNode.indice = oldNode.indice[:mid - 1]
            oldNode.children = oldNode.children[:mid]
            return oldNode.parent

        def split_leaf(oldLeaf):
            mid = (self.loadFactor + 1) // 2
            newLeaf = bptNode(self.loadFactor, True)
            newLeaf.items = oldLeaf.items[mid:]
            if oldLeaf.parent == None:
                newRoot = bptNode(self.order, False)
                newRoot.indice = [oldLeaf.items[mid].key]
                newRoot.children = [oldLeaf, newLeaf]
                oldLeaf.parent = newLeaf.parent = newRoot
                self.root = newRoot
            else:
                i = oldLeaf.parent.children.index(oldLeaf)
                oldLeaf.parent.indice.insert(i, oldLeaf.items[mid].key)
                oldLeaf.parent.children.insert(i + 1, newLeaf)
                newLeaf.parent = oldLeaf.parent

            newLeaf.next = oldLeaf.next
            oldLeaf.items = oldLeaf.items[:mid]
            oldLeaf.next = newLeaf

        def insert_node(n):
            if not n.isLeaf:
                if n.isFull():
                    insert_node(split_node(n))
                else:
                    p = bPlusTree.__bisect(n.indice, element, 'right')
                    insert_node(n.children[p])
            else:
                p = bPlusTree.__bisect(n.items, element, 'right')
                n.items.insert(p, element)
                if n.isFull():
                    split_leaf(n)
                else:
                    return

        insert_node(self.root)

    
    def __bisect(a, x, direction, low=0, high=None):
        if high is None:
            high = len(a)
        while low < high:
            mid = (low + high) // 2
            if direction == 'right':
                if x < a[mid]:
                    high = mid
                else:
                    low = mid + 1
            if direction == 'left':
                if x > a[mid]:
                    low = mid + 1
                else:
                    high = mid
        return low

    def show(self):
        print('this b+tree is:\n')
        q = deque()
        h = 0
        q.append([self.root, h])
        while True:
            try:
                w, hei = q.popleft()
            except IndexError:
                return
            else:
                if not w.isLeaf:
                    print(w.indice, 'the height is', hei)
                    if hei == h:
                        h += 1
                    q.extend([[i, h] for i in w.children])
                else:
                    print([v.key for v in w.items], 'the leaf is,', hei)

class element:
    __slots__ = ('key', 'value')

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return str((self.key, self.value))
   
    def __lt__(self, other):
        if type(other) == element:
            if self.key < other.key:
                return True 
        elif self.key < other:
            return True
        else:
            return False 

    def __eq__(self, other):
        if type(other) == element:
            if self.key == other.key:
                return True
        elif self.key == other:
            return True
        else:
            return False

def test():
    l = []
    bpt = bPlusTree(4, 4)
    l.append(element(8, "Harry"))
    l.append(element(14, "George"))
    l.append(element(2, "Sandra"))
    l.append(element(15, "Qing"))
    l.append(element(3, "Ying"))
    l.append(element(1, "Liz"))
    l.append(element(16, "Sarah"))
    l.append(element(6, "Fred"))
    l.append(element(5, "Qing"))
    l.append(element(27, "Bernie"))
    l.append(element(37, "Yuan"))
    l.append(element(18, "Juan"))
    l.append(element(25, "Iris"))
    l.append(element(7, "Chen"))
    l.append(element(13, "Chen"))
    l.append(element(20, "Lisa"))
    l.append(element(22, "Victor"))
    l.append(element(23, "Ralf"))
    l.append(element(24, "Eva"))
    for i in l:
        bpt.insert(i)
    bpt.show()

if __name__ == '__main__':
    test()