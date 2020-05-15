

    # -*- coding: utf-8 -*-

from collections import deque
import bisect

class bptNode:
    def __init__(self, order, fillFactor, isLeaf):
        self.isLeaf = isLeaf
        self.parent = None
        self.order, self.fillFactor = order, fillFactor
        self.keys, self.children = [], []
        # the leaf nodes serve as a LinkedList
        if isLeaf == True:
            self.next = None
    
    def split(self):
        mid = (self.order - 1) // 2
        midKey = self.keys[mid]
		if self.isLeaf:
            newNode = bptNode(self.order, self.fillFactor, True)
			newNode.keys = self.keys[mid:]
			newNode.children = self.children[mid:]
			self.keys = self.keys[:mid]
			self.children = self.children[:mid]
			newNode.next = self.next
			self.next = newNode
		else:
            newNode = bptNode(self.order, self.fillFactor, False)
			newNode.keys = self.keys[mid+1:]
			newNode.children = self.children[mid+1:]
			self.keys = self.keys[:mid]
			self.children = self.children[:mid+1]
        newNode.parent = self.parent
		return (midKey, newNode)
    
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
    
    def insert(self, key, value):
		ans, newFilename =  self.tree_insert(key, value, self.root)
		if ans:
			global filecounter
			newRoot = Node()
			newRoot.is_leaf = False
			newRoot.filename = str(filecounter)
			filecounter += 1
			newRoot.keys = [ans]
			newRoot.children = [self.root.filename, newFilename]
			newRoot.updateNode()
			self.root = newRoot

	def tree_insert(self, node, element):
		if node.isLeaf:
			index = bisect.bisect(node.keys, element.key)
			node.keys.insert(index, element.key)
			node.children.insert(index, element.value)
			if node.isFull():
                midKey, newNode = node.splitNode()
				return midKey, newNode.filename
			else:
				return None, None
		else:
			if key < node.keys[0]:
				ans, newFilename = self.tree_insert(key, value, Node(node.children[0]))
			for i in range(len(node.keys)-1):
				if key>=node.keys[i] and key<node.keys[i+1]:
					ans, newFilename = self.tree_insert(key, value, Node(node.children[i+1]))
			if key >= node.keys[-1]:
				ans, newFilename = self.tree_insert(key, value, Node(node.children[-1]))
		if ans:
			index = bisect.bisect(node.keys, ans)
			node.keys[index:index] = [ans]
			node.children[index+1:index+1] = [newFilename]
			if len(node.keys) <= self.factor-1:
				node.updateNode()
				return None, None
			else:
				midKey, newNode = node.splitNode()
				return midKey, newNode.filename
		else:
			return None, None


class BPlusTree:
	def __init__(self, factor, rootfile=-1):
		self.factor = factor
		if rootfile == -1:
			self.root = Node()
			# Initialize root
			global filecounter
			self.root.is_leaf = True
			self.root.keys = []
			self.root.children = []
			self.root.next = None
			self.root.filename = str(filecounter)
			filecounter += 1
			self.root.updateNode()
		else:
			self.root = Node(rootfile)

	def search(self, key):
		return self.tree_search(key, self.root)

	def tree_search(self, key, node):
		if node.is_leaf:
			return node
		else:
			if key < node.keys[0]:
				return self.tree_search(key, Node(node.children[0]))
			for i in range(len(node.keys)-1):
				if key>=node.keys[i] and key<node.keys[i+1]:
					return self.tree_search(key, Node(node.children[i+1]))
			if key >= node.keys[-1]:
				return self.tree_search(key, Node(node.children[-1]))

	def tree_search_for_query(self, key, node):
		if node.is_leaf:
			return node
		else:
			if key <= node.keys[0]:
				return self.tree_search_for_query(key, Node(node.children[0]))
			for i in range(len(node.keys)-1):
				if key>node.keys[i] and key<=node.keys[i+1]:
					return self.tree_search_for_query(key, Node(node.children[i+1]))
			if key > node.keys[-1]:
				return self.tree_search_for_query(key, Node(node.children[-1]))

	def point_query(self, key):
		all_keys = []
		all_values = []
		start_leaf = self.tree_search_for_query(key, self.root)
		keys, values, next_node = self.get_data_in_key_range(key, key, start_leaf)
		all_keys += keys
		all_values += values
		while next_node:
			keys, values, next_node = self.get_data_in_key_range(key, key, Node(next_node.filename))
			all_keys += keys
			all_values += values
		return all_keys, all_values

	def range_query(self, keyMin, keyMax):
		all_keys = []
		all_values = []
		start_leaf = self.tree_search_for_query(keyMin, self.root)
		keys, values, next_node = self.get_data_in_key_range(keyMin, keyMax, start_leaf)
		all_keys += keys
		all_values += values
		while next_node:
			keys, values, next_node = self.get_data_in_key_range(keyMin, keyMax, Node(next_node.filename))
			all_keys += keys
			all_values += values
		return all_keys, all_values

	def get_data_in_key_range(self, keyMin, keyMax, node):
		keys = []
		values = []
		for i in range(len(node.keys)):
			key = node.keys[i]
			if keyMin <= key and key <= keyMax:
				keys.append(key)
				values.append(self.read_data_file(node.children[i]))
		if node.keys[-1] > keyMax:
			next_node = None
		else:
			if node.next:
				next_node = Node(node.next)
			else:
				next_node = None
		return keys, values, next_node

	def insert(self, key, value):
		ans, newFilename =  self.tree_insert(key, value, self.root)
		if ans:
			global filecounter
			newRoot = Node()
			newRoot.is_leaf = False
			newRoot.filename = str(filecounter)
			filecounter += 1
			newRoot.keys = [ans]
			newRoot.children = [self.root.filename, newFilename]
			newRoot.updateNode()
			self.root = newRoot

	def tree_insert(self, key, value, node):
		if node.is_leaf:
			index = bisect.bisect(node.keys, key)
			node.keys[index:index] = [key]
			filename = self.create_data_file(value)
			node.children[index:index] = [filename]
			node.updateNode()
			if len(node.keys) <= self.factor-1:
				return None, None
			else:
				midKey, newNode = node.splitNode()
				return midKey, newNode.filename
		else:
			if key < node.keys[0]:
				ans, newFilename = self.tree_insert(key, value, Node(node.children[0]))
			for i in range(len(node.keys)-1):
				if key>=node.keys[i] and key<node.keys[i+1]:
					ans, newFilename = self.tree_insert(key, value, Node(node.children[i+1]))
			if key >= node.keys[-1]:
				ans, newFilename = self.tree_insert(key, value, Node(node.children[-1]))
		if ans:
			index = bisect.bisect(node.keys, ans)
			node.keys[index:index] = [ans]
			node.children[index+1:index+1] = [newFilename]
			if len(node.keys) <= self.factor-1:
				node.updateNode()
				return None, None
			else:
				midKey, newNode = node.splitNode()
				return midKey, newNode.filename
		else:
			return None, None

	
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
    bpt = bPlusTree(4, 0.8)
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
        bpt.insert(i)
    print("asss", len(l))
    bpt.show()
    #print(bpt.root.keys)
if __name__ == '__main__':
    test()