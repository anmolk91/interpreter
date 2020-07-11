class LinkedList:
    def __init__(self):
        self.head = None
        self.current = None

    def addNode(self, node):
        if (self.head == None):
            self.head = node
            self.current = node
        else:
            self.current.next = node
            self.current = node

    def iterate(self):
        itrNode = self.head
        itrStr = '';
        while (itrNode != None):
            itrStr += '--> ' + itrNode.val['value']
            itrNode = itrNode.next

        print(itrStr)