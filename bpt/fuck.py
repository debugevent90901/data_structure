# -*- coding: utf-8 -*-

from collections import deque

class bptNode:
    def __init__(self, order, fillFactor, isLeaf):
        self.isLeaf = isLeaf
        self.parent = None
        self.order, self.fillFactor = order, fillFactor
        self.keys, self.children = [], []
        # the leaf nodes serve as a LinkedList
        if isLeaf == True:
            self.next = None
    
    # whether the node is full
    def isFull(self):
        return len(self.keys) > self.order - 1 

    # if isEmpty == False, the node is not full enough to split
    def isEmpty(self):
        return len(self.keys) <= int(self.order * self.fillFactor) 

class bPlusTree:
    def __init__(self, order, fillFactor): 
        self.order, self.fillFactor = order, fillFactor
        # traverse as Tree
        self.root = bptNode(order, fillFactor, True)
        # traverse leaves as LinkedList
        self.leaf = self.root

    def insert(self, element):

        def split(oldNode):
            mid = (self.order) // 2
            if oldNode.isLeaf:
                newNode = bptNode(self.order, self.fillFactor, True)
                newNode.keys, newNode.children = oldNode.keys[mid:], oldNode.children[mid:]
                newNode.parent = oldNode.parent
                # update LinkedList
                newNode.next = oldNode.next
                oldNode.next = newNode
            else:
                newNode = bptNode(self.order, self.fillFactor, False)
                newNode.keys, newNode.children = oldNode.keys[mid+1:], oldNode.children[mid+1:]
                newNode.parent = oldNode.parent
                for child in newNode.children:
                    child.parent = newNode
            if oldNode.parent == None:
                newRoot = bptNode(self.order, self.fillFactor, False)
                newRoot.keys, newRoot.children = [oldNode.keys[mid]], [oldNode, newNode]
                oldNode.parent = newNode.parent = newRoot
                self.root = newRoot
            else:
                i = oldNode.parent.children.index(oldNode)
                oldNode.parent.keys.insert(i, oldNode.keys[mid])
                oldNode.parent.children.insert(i+1, newNode)
                if oldNode.parent.isFull():
                    split(oldNode.parent)
            oldNode.keys = oldNode.keys[:mid]
            oldNode.children = oldNode.children[:mid] if oldNode.isLeaf else oldNode.children[:mid+1]
            return oldNode.parent

        def __insert(node):
            if node.isLeaf == False:
                if node.isFull():
                    __insert(split(node))
                else:
                    index = bPlusTree.__bisect(node.keys, element.key)
                    __insert(node.children[index])
            else:
                index = bPlusTree.__bisect(node.keys, element.key)
                node.keys.insert(index, element.key)
                node.children.insert(index, element)
                if node.isFull():
                    split(node)

        __insert(self.root)

    def search(self, min=None, max=None):

        def __search(node, key):
            if node.isLeaf:
                index = bPlusTree.__bisect(node.keys, key)
                return (index, node)
            else:
                index = bPlusTree.__bisect(node.keys, key)
                return __search(node.children[index], key)
        
        node, leaf = self.root, self.leaf
        result = []
        if min is None and max is None:
            raise ValueError('range not available')
        elif min is not None and max is not None and min > max:
            raise ValueError('upper bound must not be less than lower bound')
        elif min is None:
            while True:
                for key in leaf.keys:
                    if key <= max:
                        result.append(leaf.children[leaf.keys.index(key)])
                    else:
                        return result if result != [] else None
                if leaf.next == None:
                    return result if result != [] else None
                else:
                    leaf = leaf.next
        elif max is None:
            index, leaf = __search(node, min)
            result.extend(leaf.children[index:])
            while True:
                if leaf.next == None:
                    return result if result != [] else None
                else:
                    leaf = leaf.next
                    result.extend(leaf.children)
        else:
            if min == max:
                index, leaf = __search(node, min)
                try:
                    if leaf.keys[index] == min:
                        return leaf.children[index]
                except IndexError:
                    if leaf.next.keys[0] == min:
                        return leaf.next.children[0]
                    else:
                        return None
            else:
                index1, leaf1 = __search(node, min)
                index2, leaf2 = __search(node, max)
                if leaf1 is leaf2:
                    if index1 == index2:
                        return result if result != [] else None
                    else:
                        result.extend(leaf1.children[index1:index2])
                        return result if result != [] else None
                else:
                    result.extend(leaf1.children[index1:])
                    leaf = leaf1
                    while True:
                        if leaf.next == leaf2:
                            result.extend(leaf2.children[:index2+1])
                            return result if result != [] else None
                        else:
                            result.extend(leaf.next.children)
                            leaf = leaf.next
                
    def delete(self, key):

        def merge(n, i):
            if n.children[i].isLeaf:
                n.children[i].keys = n.children[i].keys + n.children[i + 1].keys
                n.children[i].children = n.children[i].children + n.children[i + 1].children
                n.children[i].next = n.children[i + 1].next
            else:
                n.children[i].keys = n.children[i].keys + [n.keys[i]] + n.children[i+1].keys
                n.children[i].children = n.children[i].children + n.children[i + 1].children
            n.children.remove(n.children[i + 1])
            n.keys.remove(n.keys[i])
            if n.keys == []:
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
                n.children[i + 1].keys.insert(0, n.children[i].keys[-1])
                n.keys[i + 1] = n.children[i].keys[-1]
                n.children[i].children.pop()
                n.children[i].keys.pop()
            else:
                # 如果 i不空，但是i+1节点为空
                # 则将i中的最后一个追加到i+1的第一个中，并刷新n在i+1的索引值
                n.children[i + 1].keys.insert(0, n.children[i].keys[-1])
                n.children[i + 1].children.insert(0, n.children[i].children[-1])
                n.children[i].keys.pop()
                n.children[i].children.pop()
                n.keys[i] = n.children[i+1].keys[0]

        def tran_r2l(n, i):
            if not n.children[i].isLeaf:
                n.children[i].children.append(n.children[i + 1].children[0])
                n.children[i + 1].children[0].parent = n.children[i]
                n.children[i].keys.append(n.keys[i])
                n.keys[i] = n.children[i + 1].keys[0]
                n.children[i + 1].children.remove(n.children[i + 1].children[0])
                n.children[i + 1].keys.remove(n.children[i + 1].keys[0])
            else:
                n.children[i].keys.append(n.children[i + 1].keys[0])
                n.children[i].children.append(n.children[i + 1].children[0])
                n.children[i + 1].keys.remove(n.children[i + 1].keys[0])
                n.children[i + 1].children.remove(n.children[i + 1].children[0])
                n.keys[i] = n.children[i + 1].keys[0]

        def __delete(n, key):
            if not n.isLeaf:
                p = bPlusTree.__bisect(n.keys, key)
                if p == len(n.keys):
                    if not n.children[p].isEmpty():
                        return __delete(n.children[p], key)
                    elif not n.children[p - 1].isEmpty():
                        tran_l2r(n, p - 1)
                        return __delete(n.children[p], key)
                    else:
                        try:
                            merge(n, p)
                        except IndexError:
                            return __delete(n.children[p], key)
                else:
                    if not n.children[p].isEmpty():
                        return __delete(n.children[p], key)
                    elif not n.children[p + 1].isEmpty():
                        tran_r2l(n, p)
                        return __delete(n.children[p], key)
                    else:
                        return __delete(merge(n, p), key)
            else:
                p = bPlusTree.__bisect(n.keys, key)
                try:
                    pp = n.keys[p]
                except IndexError:
                    return -1
                else:
                    if pp != key:
                        return -1
                    else:
                        n.keys.remove(key)
                        n.children.remove(n.children[p])
                        return 0
                        
        item = self.search(key, key)   
        if item != None:    
            __delete(self.root, item.key)
        else:
            raise ValueError("element does not exist.")
    
    def __bisect(a, x, low=0, high=None):
        if high is None:
            high = len(a)
        while low < high:
            mid = (low + high) // 2
            if x > a[mid]:
                low = mid + 1
            else:
                high = mid
        return low

    # actually no need, helps to debug, delete when finished
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
                    print(w.keys, 'the height is', hei)
                    if hei == h:
                        h += 1
                    q.extend([[i, h] for i in w.children])
                else:
                    print([v for v in w.children], 'the leaf is,', hei)

class element:
    __slots__ = ('key', 'value')

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return str((self.key, self.value))
    
    
def test():
    l = []
    bpt = bPlusTree(5, 0.6)
    l.append(element(8, "#8"))
    l.append(element(14, "#14"))
    l.append(element(2, "#2"))
    l.append(element(15, "#15"))
    l.append(element(3, "#3"))
    l.append(element(1, "#1"))
    l.append(element(16, "#16"))
    l.append(element(6, "#6"))
    l.append(element(5, "#5"))
    l.append(element(27, "#27"))
    l.append(element(37, "#37"))
    l.append(element(18, "#18"))
    l.append(element(25, "#25"))
    l.append(element(7, "#7"))
    l.append(element(13, "#13"))
    l.append(element(20, "#20"))
    l.append(element(22, "#22"))
    l.append(element(23, "#23"))
    l.append(element(24, "#24"))

    for i in l:
        #print(i)
        bpt.insert(i)
    bpt.show()
    #a = bpt.search(min=16,max=16)
    #print(a)
    bpt.delete(24)
    bpt.show()

if __name__ == '__main__':
    test()

