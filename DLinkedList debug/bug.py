# -*- coding: utf-8 -*-

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

	def append(self, item):
		lastNode = self.first.getPrevious()
		newNode = DLinkedList.__Node(item, self.first, lastNode)
		lastNode.setNext(newNode)
		self.first.setPrevious(newNode)
		self.numItems += 1

	def locate(self, index):
		if index >= 0 and index < self.numItems:
			cursor = self.first.getNext()
			for i in range(index):
				cursor = cursor.getNext()
			return cursor
		raise IndexError("DLinkedList index out of range")

	def splice(self, index, other, index1, index2):
		if index1 <= index2:
			begin = other.locate(index1)
			end = other.locate(index2)
			self.insertList(begin, end, index)

	def insertList(self, begin, end, index):
		address = self.locate(index)
		successor = address.getNext()
		begin.setPrevious(address)
		end.setNext(successor)
		address.setNext(begin)
		successor.setPrevious(end)



def main():
	a = DLinkedList(['a', 'b', 'c', 'd', 'e'])
	b = DLinkedList(['ass', 'pee', 'shit', 'fuck', 'dick'])
	c = DLinkedList(['ass', 'pee', 'shit', 'fuck', 'dick'])

	'''
	ptr = a.first.getNext()
	while ptr != a.first:
		print(ptr.item)
		ptr = ptr.getNext()
	print("114514114514114514114514114514114514")	
	'''

	a.insertList(b.first.getNext(), b.first.getPrevious(), 2)
	ptrr = a.first.getNext()
	while ptrr != a.first:
		print(ptrr.item)
		ptrr = ptrr.getNext()

	print("#################")

	# 接下来开始报错
	a.splice(3, b, 2, 4)
	ptrrr = a.first.getNext()
	while ptrrr != a.first:
		print(ptrrr.item)
		ptrrr = ptrrr.getNext()


if __name__ == "__main__":
    main()




























