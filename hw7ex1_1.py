# -*- coding: utf-8 -*-


class Graph:
    def __init__(self, edges=[]):
        self.vertexList = VertexList(edges)
        for e in edges:
            self.addEdge(e)
            self.addEdge((e[1], e[0]))

    def addEdge(self, edge):
        vertex = self.vertexList.locate(edge[0])
        edgelist = vertex.edges
        if edgelist != None:
            edgelist.add(edge[1])
        else:
            edgelist = EdgeList(edge[1])
        vertex.setEdges(edgelist)

    def __iter__(self):
        vertices = self.vertexList
        for v in vertices:
            x = vertices.locate(v)
            y = x.edges
            if y != None:
                for z in y:
                    yield (v, z)

    def insertVertex(self, item):
        if not (item in self.vertexList):
            self.vertexList.append(item)

    def deleteVertex(self, item):
        return self.vertexList.remove(item)

    def insertEdge(self, edge):
        self.vertexList.addVertex(edge)
        self.addEdge(edge)
        self.addEdge((edge[1], edge[0]))

    def deleteEdge(self, edge):
        self.__deleteEdge(edge)
        self.__deleteEdge((edge[1], edge[0]))

    def __deleteEdge(self, edge):
        if not (edge[0] in self.vertexList):
            print("There is no edge", edge)
            return False
        vertexlocation = self.vertexList.locate(edge[0])
        edgelist = vertexlocation.getEdges()
        if edgelist == None:
            print("There is no edge", edge)
            return False
        res = edgelist.remove(edge[1])
        if res == False:
            print("There is no edge", edge)
        return res

    def outgoingEdges(self, item):
        vertex = self.vertexList.locate(item)
        if vertex == None:
            print("There is no vertex", item)
            return []
        edgelist = vertex.getEdges()
        if edgelist == None:
            return []
        res = []
        for v in edgelist:
            res.append((item, v))
        return res

    # works as an iterator
    def outgoingEdge(self, item):
        vertex = self.vertexList.locate(item)
        if vertex == None:
            print("There is no vertex", item)
            return []
        edgelist = vertex.getEdges()
        if edgelist == None:
            print("There is no outgoing edge")
            return []
        for v in edgelist:
            yield (item, v)

    def bfs(self, vertex):
        if not (vertex in self.vertexList):
            print("There is no vertex", vertex)
            return None
        length = self.vertexList.getlength()
        distance = [None] * length
        parent = [None] * length
        index = self.vertexList.index(vertex)
        distance[index] = 0
        parent[index] = vertex
        currentlayer = Fifo(length)
        currentlayer.pushback(vertex)
        nextlayer = Fifo(length)
        for l in range(length):
            for u in currentlayer:
                print(u)
                loc = self.vertexList.locate(u)
                edgelist = loc.getEdges()
                if edgelist != None:
                    for v in edgelist:
                        idx = self.vertexList.index(v)
                        if parent[idx] == None:
                            nextlayer.pushback(v)
                            distance[idx] = l + 1
                            parent[idx] = u
            currentlayer = nextlayer
            nextlayer = Fifo(length)
        return (distance, parent)

    def allDFS(self):
        numVertices = self.vertexList.getlength()
        initlist = [None] * numVertices
        self.tree = PyList(initlist, numVertices)
        for i in range(numVertices):
            newgraph = Graph([])
            self.tree[i] = newgraph
        for s in self.vertexList:
            self.mark = [None] * numVertices
            self.dfsPos = 1   
            self.dfsNum = [1] * numVertices
            self.finishingTime = 1
            self.finishTime = [1] * numVertices
            idx = self.vertexList.index(s)
            if self.mark[idx] == None:
                self.mark[idx] = s
                self.dfsNum[idx] = self.dfsPos
                self.dfsPos += 1
                self.dfs(s, s, idx)

    def dfs(self, vertex1, vertex2, index):
        for e in self.outgoingEdges(vertex2):
            idx = self.vertexList.index(e[1])
            # useless, can delete it
            if self.mark[idx] != None:
                self.__traverseNontreeEdge(e)
            else:
                self.tree[index].insertEdge(e)
                self.__traverseTreeEdge(e)
                self.mark[idx] = e[1]
                self.dfs(vertex2, e[1], index)
        self.backtrack(vertex1, vertex2)

    def __traverseTreeEdge(self, e):
        idx = self.vertexList.index(e[1])
        self.dfsNum[idx] = self.dfsPos
        self.dfsPos += 1

    def __traverseNontreeEdge(self, e):
        self.dfsPos = self.dfsPos

    def backtrack(self, vertex1, vertex2):
        idx = self.vertexList.index(vertex2)
        self.finishTime[idx] = self.finishingTime
        self.finishingTime += 1
    
    def singleDFS(self, vertex):
        numVertices = self.vertexList.getlength()
        self.mark = [None] * numVertices
        self.dfsPos, self.finishingTime = 1, 1   
        self.dfsNum, self.finishTime = [1] * numVertices, [1] * numVertices
        idx = self.vertexList.index(vertex)
        self.mark[idx] = vertex
        self.dfsNum[idx] = self.dfsPos
        self.dfsPos += 1
        tmp = []
        self.DFS(tmp, vertex, vertex, idx)
        return tmp
            
    def DFS(self, tmp, vertex1, vertex2, index):
        tmp.append(vertex2)
        for e in self.outgoingEdges(vertex2):
            idx = self.vertexList.index(e[1])
            if self.mark[idx] == None:
                self.__traverseTreeEdge(e)
                self.mark[idx] = e[1]
                self.DFS(tmp, vertex2, e[1], index)
        self.backtrack(vertex1, vertex2)

    def connectedComponents(self):
        numVertices = self.vertexList.getlength()
        visited = PyList(numVertices * [False], numVertices)
        ans = []
        for i in self.vertexList:
            index = self.vertexList.index(i)
            if visited[index] == False:
                path = self.singleDFS(i)
                for j in path:
                    visited[self.vertexList.index(j)] = True
                ans.append(path)
        return ans
    
class VertexList:
    class __Vertex:
        def __init__(self, item, next=None, previous=None):
            self.item = item
            self.next = next
            self.previous = previous
            self.edges = None

        def getItem(self):
            return self.item

        def getNext(self):
            return self.next

        def getPrevious(self):
            return self.previous

        def getEdges(self):
            return self.edges

        def setItem(self, item):
            self.item = item

        def setNext(self, next):
            self.next = next

        def setPrevious(self, previous):
            self.previous = previous

        def setEdges(self, edge):
            self.edges = edge

    def __init__(self, edges=[]):
        self.dummy = VertexList.__Vertex(None, None, None)
        self.numVertices = 0
        self.dummy.setNext(self.dummy)
        self.dummy.setPrevious(self.dummy)
        for e in edges:
            self.addVertex(e)

    def __iter__(self):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            yield cursor.getItem()

    def append(self, item):
        lastVertex = self.dummy.getPrevious()
        newVertex = VertexList.__Vertex(item, self.dummy, lastVertex)
        lastVertex.setNext(newVertex)
        self.dummy.setPrevious(newVertex)
        self.numVertices += 1

    def __contains__(self, item):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            vertex = cursor.getItem()
            if vertex == item:
                return True
        return False

    def locate(self, vertex):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            item = cursor.getItem()
            if vertex == item:
                return cursor

    def addVertex(self, edge):
        node1 = edge[0]
        node2 = edge[1]
        if not (node1 in self):
            self.append(node1)
        if not (node2 in self):
            self.append(node2)

    def remove(self, item):
        cursor = self.dummy
        location = None
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            vertex = cursor.getItem()
            edgelist = cursor.edges
            if edgelist != None:
                if item in edgelist:
                    print(item, "cannot be deleted, as it appears in an edge.")
                    return False
            if vertex == item:
                location = cursor
        if location == None:
            print(item, "is not a vertex.")
            return False
        nextVertex = location.getNext()
        prevVertex = location.getPrevious()
        prevVertex.setNext(nextVertex)
        nextVertex.setPrevious(prevVertex)
        self.numVertices -= 1
        return True

    def index(self, item):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            if cursor.getItem() == item:
                return i
        return -1

    def getlength(self):
        return self.numVertices


class EdgeList:
    class __Edge:
        def __init__(self, item, next=None, previous=None):
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

    def __init__(self, edge):
        self.first = EdgeList.__Edge(edge, None, None)
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        self.numEdges = 1

    def add(self, edge):
        lastEdge = self.first.getPrevious()
        newEdge = EdgeList.__Edge(edge, self.first, lastEdge)
        lastEdge.setNext(newEdge)
        self.first.setPrevious(newEdge)
        self.numEdges += 1

    def __iter__(self):
        cursor = self.first
        for i in range(self.numEdges):
            yield cursor.getItem()
            cursor = cursor.getNext()

    def __contains__(self, item):
        cursor = self.first
        for i in range(self.numEdges):
            vertex = cursor.getItem()
            if vertex == item:
                return True
            cursor = cursor.getNext()
        return False

    def remove(self, item):
        cursor = self.first
        for i in range(self.numEdges):
            vertex = cursor.getItem()
            if vertex == item:
                nextVertex = cursor.getNext()
                prevVertex = cursor.getPrevious()
                prevVertex.setNext(nextVertex)
                nextVertex.setPrevious(prevVertex)
                self.numEdges -= 1
                if (cursor == self.first):
                    self.first = nextVertex
                return True
            cursor = cursor.getNext()
        return False

# Definition of PyList class
class PyList:
    def __init__(self, contents=[], size=20):
        self.items = [None] * size
        self.numItems = 0
        self.size = size
        for e in contents:
            self.append(e)

    def __setitem__(self, index, val):
        if index >= 0 and index < self.numItems:
            self.items[index] = val
            return
        raise IndexError("PyList assignment index out of range")

    def __getitem__(self, index):
        if index >= 0 and index < self.numItems:
            return self.items[index]
        raise IndexError("PyList index out of range")

    def append(self, item):
        if self.numItems == self.size:
            self.allocate()
        self.items[self.numItems] = item
        self.numItems += 1

    def allocate(self):
        newlength = 2 * self.size
        newList = [None] * newlength
        for i in range(self.numItems):
            newList[i] = self.items[i]
        self.items = newList
        self.size = newlength

    def insert(self, i, x):
        if self.numItems == self.size:
            self.allocate()
        if i < self.numItems:
            for j in range(self.numItems - 1, i, -1):
                self.items[j + 1] = self.items[j]
            self.items[i] = x
            self.numItems += 1
        else:
            self.append(x)

    def __add__(self, other):
        result = PyList(size=self.numItems + other.numItems)
        for i in range(self.numItems):
            result.append(self.items[i])
        for i in range(other.numItems):
            result.append(other.items[i])
        return result

    def delete(self, index):
        if self.numItems == self.size / 4:
            self.deallocate()
        if index <= self.numItems:
            for j in range(index, self.numItems - 2):
                self.items[j] = self.items[j + 1]
            self.numItems -= 1
        else:
            raise IndexError("PyList index out of range")

    def deallocate(self):
        newlength = self.size / 2
        newList = [None] * newlength
        for i in range(self.numItems):
            newList[i] = self.items[i]
        self.items = newList
        self.size = newlength

    def __contains__(self, item):
        for i in range(self.numItems):
            if self.items[i] == item:
                return True
            return False

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        if self.numItems != other.numItems:
            return False
        for i in range(self.numItems):
            if self.items[i] != self.items[i]:
                return False
            return True

    def qsort(self):
        if self.numItems <= 1:
            return self
        pivot = self.items[0]
        list1 = PyList([], self.numItems)
        listp = PyList([], self.numItems)
        list2 = PyList([], self.numItems)
        for i in range(self.numItems):
            if self.items[i] < pivot:
                list1.append(self.items[i])
            else:
                if self.items[i] == pivot:
                    listp.append(self.items[i])
                else:
                    list2.append(self.items[i])
        slist1 = list1.qsort()
        slist2 = list2.qsort()
        outlist = slist1 + listp + slist2
        return outlist

    def radixSort(self, numdigits, digits):
        sortedlist = self
        for i in range(numdigits):
            sortedlist = sortedlist.Ksort(i, digits)
        return sortedlist

    def Ksort(self, round, digits):
        bucket = PyList([], digits)
        for k in range(digits):
            newlist = PyList([], self.numItems)
            bucket.append(newlist)
        for i in range(self.numItems):
            item = self.items[i]
            item1 = item // (digits ** round) % digits
            bucket[item1].append(item)
        result = bucket[0]
        for k in range(digits - 1):
            result = result + bucket[k + 1]
        return result


# Definition of FIFO class
class Fifo:
    class __Node:
        def __init__(self, val):
            self.val = val
            self.next = None
    def __init__(self, content=[]):
        self.head = None
        self.end = None
        self.length = 0
        for i in content:
            self.pushback(i)
    def pushback(self, val):
        node = self.__Node(val)
        if self.end is None:
            assert (self.head is None)
            self.head = self.end = node
        else:
            self.end.next = node
            self.end = node
        self.length += 1
    def popfront(self):
        if self.head is None:
            return None
        node = self.head
        self.head = node.next
        if self.head is None:
            self.end = None
        self.length -= 1
        return node.val
    def is_empty(self):
        if self.head is None:
            assert (self.end is None)
            return True
        return False
    def show(self):
        temp = self.head
        while temp is not None:
            print(temp.val)
            temp = temp.next

edges = [(1,2),(2,4),(3,5),(2,5),(1,5),(3,4),(3,1),(6,2),(6,3)]
g = Graph(edges)
g.insertVertex(7)
g.insertVertex(8)
g.deleteVertex(1)
g.deleteVertex(7)
g.insertEdge((1,7))
g.deleteEdge((1,2))
print(g.connectedComponents())

ass = [(1, 0), (2, 3), (3, 4)]
a = Graph(ass)
v = a.connectedComponents()
print(v)