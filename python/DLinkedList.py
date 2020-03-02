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

	def bubbleSort(self):
		while True:
			is_swaped = 0
			ptr = self.first.getNext()
			while ptr != self.first:
				if ptr.item > ptr.getNext().item and ptr.getNext().item != None:
					ptr.item, ptr.getNext().item = ptr.getNext().item, ptr.item
					is_swaped += 1
				ptr = ptr.getNext()
			if is_swaped == 0:
				break

	def selectionSort(self):
		firstNode = self.first.getNext()
		lastNode = self.first.getPrevious()
		outlast = self.first
		self.first.setNext(self.first)
		self.first.setPrevious(self.first)
		counter = self.numItems
		while counter != 0:
			location = self.getMinimum(firstNode, lastNode)
			self.cut(firstNode, lastNode, location)
			self.addLocation(location, outlast)
			counter -= 1

	def getMinimum(self, first, last):
		minimum = first.getItem()
		cursor = first
		location = first
		while cursor != last:
			cursor = cursor.getNext()
			item = cursor.getItem()
			if item < minimum:
				minimum = item
				location = cursor
		return location
	
	def cut(self, first, last, location):
		if location = first:
			first = location
		else:
			if location = last:
				last = location
			else:
				prev = location.getPrevious()
				next = location.getNext()
				prev.setNext(next)
				next.setPrevious(prev)

	def addLocation(self,location, outlast):
		location.setPrevious(outlast)
		location.setNext(self.first)
		outlast.setNext(location)
		outlast = location
		self.first.setPrevious(location)




a = DLinkedList(['a', 'b', 'c', 'd', 'e'])
b = DLinkedList(['ass', 'pee', 'shit', 'fuck', 'dick'])

ptr = a.first.getNext()
while ptr != a.first:
	print(ptr.item)
	ptr = ptr.getNext()
print("114514114514114514114514114514114514")
a.selectionSort()
ptr = a.first.getNext()
while ptr != a.first:
	print(ptr.item)
	ptr = ptr.getNext()

























