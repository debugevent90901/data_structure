# -*- coding: utf-8 -*-

from PyList import PyList
from DLinkedList import DLinkedList
from HashSet import HashSet
from queue import Fifo

queue = Fifo()
for i in range(20):
    queue.pushback(i)
for i in range(5):
    queue.popfront()
for i in range(20,28):
    queue.pushback(i)
for x in queue:
    print(x)
print(queue.size,queue.length)

print('#######')
for i in range(queue.length):
    y = queue.front()
    x = queue.popfront()
    print(i,y,x)
