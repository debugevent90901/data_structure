# -*- coding: utf-8 -*-

from PyList import PyList
from DLinkedList import DLinkedList

#a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
a = [123, 45, 3, 114514, 8964, 73, 42, 6, 11, 1000]
test2 = DLinkedList(a)
test2.printList()
test2.mergeSort()
test2.printList()