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

    def search(self, min=None, max=None):

        def search_key(node, k):
            if node.isLeaf:
                index = bPlusTree.__bisect(node.items, k, 'left')
                return (index, node)
            else:
                index = bPlusTree.__bisect(node.indice, k, 'right')
                return search_key(node.children[index], k)

        node, leaf, result = self.root, self.leaf, []
        if min is None and max is None:
            raise ValueError('you need to setup searching range')
        elif min is not None and max is not None and min > max:
            raise ValueError('upper bound must be greater or equal than lower bound')
        if min is None:
            while True:
                for item in leaf.items:
                    if item <= max:
                        result.append(item)
                    else:
                        return result
                if leaf.next == None:
                    return result
                else:
                    leaf = leaf.next
        elif max is None:
            index, leaf = search_key(node, min)
            result.extend(leaf.items[index:])
            while True:
                if leaf.next == None:
                    return result
                else:
                    leaf = leaf.next
                    result.extend(leaf.items)
        else:
            if min == max:
                index, leaf = search_key(node, min)
                try:
                    if leaf.items[index] == min:
                        result.append(leaf.items[index])
                        return result
                    else:
                        return result
                except IndexError:
                    return result
            else:
                index1, leaf1 = search_key(node, min)
                index2, leaf2 = search_key(node, max)
                if leaf1 is leaf2:
                    if index1 == index2:
                        return result
                    else:
                        result.extend(leaf1.items[index1:index2])
                        return result
                else:
                    result.extend(leaf1.items[index1:])
                    leaf = leaf1
                    while True:
                        if leaf.next == leaf2:
                            result.extend(leaf2.items[:index2 + 1])
                            return result
                        else:
                            result.extend(leaf.next.items)
                            leaf = leaf.next

    def delete(self, key):

        def merge(n, i):
            if n.children[i].isLeaf:
                n.children[i].items = n.children[i].items + n.children[i + 1].items
                n.children[i].next = n.children[i + 1].next
            else:
                n.children[i].indice = n.children[i].indice + [n.indice[i]] + n.children[i + 1].indice
                n.children[i].children = n.children[i].children + n.children[i + 1].children
            n.children.remove(n.children[i + 1])
            n.indice.remove(n.indice[i])
            if n.indice == []:
                n.children[0].parent = None
                self.root = n.children[0]
                del n
                return self.root
            else:
                return n

        def tran_l2r(n, i):
            if not n.children[i].isLeaf:
                # 将i的最后一个节点追加到i+1的第一个节点
                n.children[i + 1].children.insert(0, n.children[i].children[-1])
                n.children[i].children[-1].parent = n.children[i + 1]
                # 追加 i+1的索引值，以及更新n的i+1索引值
                n.children[i + 1].indice.insert(0, n.children[i].indice[-1])
                n.indice[i + 1] = n.children[i].indice[-1]
                n.children[i].children.pop()
                n.children[i].indice.pop()
            else:
                # 如果 i不空，但是i+1节点为空
                # 则将i中的最后一个追加到i+1的第一个中，并刷新n在i+1的索引值
                n.children[i + 1].items.insert(0, n.children[i].items[-1])
                n.children[i].items.pop()
                n.indice[i] = n.children[i + 1].items[0].key

        def tran_r2l(n, i):
            if not n.children[i].isLeaf:
                n.children[i].children.append(n.children[i + 1].children[0])
                n.children[i + 1].children[0].parent = n.children[i]
                n.children[i].indice.append(n.indice[i])
                n.indice[i] = n.children[i + 1].indice[0]
                n.children[i + 1].children.remove(n.children[i + 1].children[0])
                n.children[i + 1].indice.remove(n.children[i + 1].indice[0])
            else:
                n.children[i].items.append(n.children[i + 1].items[0])
                n.children[i + 1].items.remove(n.children[i + 1].items[0])
                n.indice[i] = n.children[i + 1].items[0].key

        def del_node(n, kv):
            if not n.isLeaf:
                p = bPlusTree.__bisect(n.indice, kv, 'right')
                if p == len(n.indice):
                    if not n.children[p].isEmpty():
                        return del_node(n.children[p], kv)
                    elif not n.children[p - 1].isEmpty():
                        tran_l2r(n, p - 1)
                        return del_node(n.children[p], kv)
                    else:
                        return del_node(merge(n, p), kv)
                else:
                    if not n.children[p].isEmpty():
                        return del_node(n.children[p], kv)
                    elif not n.children[p + 1].isEmpty():
                        tran_r2l(n, p)
                        return del_node(n.children[p], kv)
                    else:
                        return del_node(merge(n, p), kv)
            else:
                p = bPlusTree.__bisect(n.items, kv, 'left')
                try:
                    pp = n.items[p]
                except IndexError:
                    return -1
                else:
                    if pp != kv:
                        return -1
                    else:
                        n.items.remove(kv)
                        return 0
        item = self.search(key, key)   
        if item != None:    
            del_node(self.root, item[0])
        else:
            raise ValueError("element does not exist.")
    
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

    def __iter__(self):
        cursor = self.leaf
        while cursor != None:
            yield cursor
            cursor = cursor.next

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
    '''
    print("########")
    for i in bpt:
        for j in i.items:
            print(j.value, end=' ')
    print("########")
    #print([kv.value for kv in bpt.search(15, 15)])
    a = bpt.search(15, 15)
    print(a)
    print("########")
    '''
    bpt.delete(24)
    bpt.show()
    
if __name__ == '__main__':
    test()