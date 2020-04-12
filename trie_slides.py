# -*- coding: utf-8 -*-

class Trie:

    class TrieNode:
        def __init__(self, item, next = None, follows = None):
            self.item = item
            self.next = next
            self.follows = follows
    
    def __init__(self):
        self.start = None
    
    def insert(self, item):
        self.start = Trie.__insert(self.start, item)
    
    def __contains__(self, item):
        return Trie.__contains(self.start, item+["#"])

    def __insert(node, item):
        if item == []:
            newnode = Trie.TrieNode("#")
            return newnode
        if node == None:
            key = item.pop(0)
            newnode = Trie.TrieNode(key)
            newnode.follows = Trie.__insert(newnode.follows, item)
            return newnode
        else:
            key = item[0]
            if node.item == key:
                key = item.pop(0)
                node.follows = Trie.__insert(node.next, item)
            else:
                node.next = Trie.__insert(node.next, item)
            return node
        
    def __contains(node, item):
        if item == []:
            return True
        if node == None:
            return False
        key = item[0]
        if node.item == key:
            key = item.pop(0)
            return Trie.__contains(node.follows, item)
        return Trie.__contains(node.next, item)
    
    def print_trie(self, root, level_f=0):
        if root is None:
            return
        if root.item != '#':
            print(root.item, '-', end='')
        else:
            print(root.item, end='')
        self.print_trie(root.follows, level_f + 1)
        if root.next is not None:
            print('\n')
            str_sp = ' ' * level_f * 3
            print(str_sp + '|')
            print(str_sp, end='')
        self.print_trie(root.next, level_f)
        return

t = Trie()
t.insert(["a", "s", "s"])
t.insert(["f", "u", "c", "k"])
t.insert(["b", "i", "t", "c", "h"])
t.insert(["a", "s", "s", "h", "o", "l", "e"])
t.print_trie(t.start)
'''
print(["a", "s", "s"] in t)
print(["c", "o", "m", "m", "i", "e"] in t)
'''