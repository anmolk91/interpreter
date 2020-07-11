import copy
from functools import reduce
from node import Node
from linkedlist import LinkedList

class Interpreter:
    vertices = []
    edges = []
    edgesList = None

    def readApplication(self, inputfile = 'inputPS7.txt', promptsFile = 'promptsPS7.txt'):
        inputFileContent = self.getFileContent(inputfile, 'r')
        promptsFileContent = self.getFileContent(promptsFile, 'r')
        self.processInputData(inputFileContent)
        self.processPromptsData(promptsFileContent)

    def getFileContent(self, filePath, mode):
        with open(filePath, mode) as my_file:
            return my_file.read()

    def processInputData(self, unformattedData):
        tempList = unformattedData.split('\n')
        rawNodes = copy.copy(list(self.filterRawNodes(tempList)))
        self.vertices = self.createVertices(rawNodes)
        self.edges = self.createEdges(rawNodes, self.vertices)
        self.createEdgesList(rawNodes, self.vertices)

    def processPromptsData(self, unformattedPromptsData):
        tempList = unformattedPromptsData.split('\n')
        self.executeActions(tempList)

    def executeActions(self, rawDataList):
        for dataItem in rawDataList:
            if ('showMinList' in dataItem):
                self.displayHireList()
            elif ('searchLanguage' in dataItem):
                self.displayCandidates(dataItem.split(':')[1].strip())
            elif ('DirectTranslate' in dataItem):
                argsList = dataItem.split(':')
                self.findDirectTranslator(argsList[1].strip(), argsList[2].strip())
            elif ('TransRelation' in dataItem):
                argsList = dataItem.split(':')
                self.findTransRelation(argsList[1].strip(), argsList[2].strip())

    def filterRawNodes(self, data):
        def filterFun(str):
            if ('/' in str):
                return True
            else:
                return False
        return filter(filterFun, data)

    
    def createVertices(self, rawData):
        vertices = []
        indice = 0
        for rawItem in rawData:
            for index, item in enumerate(rawItem.split('/')):
                item = item.strip()
                if next((vertex for vertex in vertices if vertex['value'] == item), None) == None:
                    if index == 0:
                        vertices.append({'type': 'interpreter', 'value': item, 'index': indice})
                    else:
                        vertices.append({'type': 'language', 'value': item, 'index' : indice})
                    indice += 1
        return vertices

    def createEdges(self, rawEdgesList, vertices):
        verticesLen = len(vertices)
        edges = [[0 for i in range(verticesLen)] for i in range((verticesLen))]
        for edgesData in list(rawEdgesList):
            row = [item.strip() for item in edgesData.split('/')]
            dataDict = {key : next((node for node in vertices if node['value'] == key), None) for key in row }
            temp = ''
            for index, key in enumerate(dataDict):
                if (index > 0):
                    edges[dataDict[temp]['index']][dataDict[key]['index']] = 1
                    edges[dataDict[key]['index']][dataDict[temp]['index']] = 1
                else:
                    temp = key

        return edges

    def createEdgesList(self, rawEdgesList, vertices):
        def createsList(item):
            tempObj = { 'name': item['value'].strip(), 'listVal': LinkedList() }
            tempNode = Node({ 'value': item['value']})
            tempObj['listVal'].addNode(tempNode)
            return tempObj
        self.edgesList = [createsList(item) for item in vertices]
        for item in rawEdgesList:
            nodesName = [i.strip() for i in item.split('/')]
            parentVal = None
            parentLinkedList = None
            childNode = None
            for index, item in enumerate(nodesName):
                if (index != 0):
                    childNode = Node({'value': item})
                    childNodeList = next((edge for edge in self.edgesList if item.strip() == edge['name']), None)['listVal']
                    childNodeList.addNode(Node({'value': parentVal}))
                    parentLinkedList.addNode(childNode)
                else:
                    parentVal = item
                    parentLinkedList = next((edge for edge in self.edgesList if item.strip() == edge['name']), None)['listVal']
        
    def showAll(self):
        (filteredInterpreters, filteredLanguages) = (self.getFilteredInterpreters(self.vertices), self.getFilteredLanguages(self.vertices))
        output = '--------Function showAll--------'
        output += '\n\nTotal no. of candidates: {totalCandidates}\nTotal no. of languages: {totalLangugages}'.format(totalCandidates = len(filteredInterpreters), totalLangugages = len(filteredLanguages))
        output += '\n\nList of candidates:'
        for candidate in filteredInterpreters:
            output += '\n\n'+ candidate['value'].title()
        output += '\n\n\nList of languages:'
        for language in filteredLanguages:
            output += '\n\n'+ language['value'].title()
        analysisOutput = '\n\n--------Function showAll--------\n\nWorst Complexity will be O(n) where n is the total no of nodes'
        self.printOutput(output)
        self.printAnalysis(analysisOutput)


    def getFilteredInterpreters(self, data):
        def filterInterPreters(dataItem):
            return dataItem['type'] == 'interpreter'
        return list(filter(filterInterPreters, data))
    
    def getFilteredLanguages(self, data):
        def filterLanguage(dataItem):
            return dataItem['type'] == 'language'
        return list(filter(filterLanguage, data))


    def displayHireList(self):
        filteredInterpreters = self.getFilteredInterpreters(self.vertices)
        dataDictList = []
        for interpreter in filteredInterpreters:
            dataDictItem = copy.deepcopy(interpreter)
            subjectList = self.edges[dataDictItem['index']]
            dataDictItem['totalLanguages'] = reduce((lambda x, y: x + y), subjectList)
            dataDictItem['languages'] = [self.vertices[index]['value'] for index, item in enumerate(subjectList) if item == 1]
            dataDictList.append(dataDictItem)
        def getSortKey(item):
            return item['totalLanguages']
        dataDictList.sort(key = getSortKey, reverse = True)
        languagesList = []
        responseList = []
        def filterExistingLists(language):
            return language not in languagesList
        for dataDict in dataDictList:
            tempList = list(filter(filterExistingLists, dataDict['languages']))
            if len(tempList) > 0:
                [languagesList.append(filteredLg) for filteredLg in tempList]
                responseList.append(dataDict)

        output = '--------Function displayHireList--------\n\nNo of candidates required to cover all languages: {count}'.format(count = len(responseList))
        for response in responseList:
            output += '\n' + response['value'].title() + ' / ' + ' / '.join(response['languages'])
        output += '\n\n'
        self.printOutput(output)
        self.printAnalysis()

    def displayCandidates(self, language):
        vertex = next((node for node in self.vertices if node['value'].lower() == language.strip().lower()), None)
        outputStr = '\n\n--------Function displayCandidates --------\n\nList of Candidates who can speak {language}:'.format(language = language)
        if (vertex == None):
            print('Empty')
        else :
            outputData = [self.vertices[index] for index, value in enumerate(self.edges[vertex['index']]) if value == 1]
            for outputDataItem in outputData:
                outputStr += '\n\n{name}'.format(name = outputDataItem['value'].title())
            self.printOutput(outputStr)

    def findDirectTranslator(self, langA, langB):
        langA = langA.strip()
        langB = langB.strip()
        def addVisited(item):
            item['visited'] = False
            return item
        verticesCopy = map(addVisited, copy.deepcopy(self.vertices))
        source = next((language for language in verticesCopy if language['value'] == langA), None)
        destination = next((language for language in verticesCopy if language['value'] == langB), None)
        if source != None and destination != None:
            pathNode = self.findPath(source, destination, copy.deepcopy(self.vertices), self.edges)
            output = '\n\n--------Function findDirectTranslator --------\n\nLanguage A: {langA}\n\nLanguage B: {langB}\n\nDirect Translator: '.format(langA = langA, langB = langB)
            if pathNode != None:
                output += 'Yes, {interpreter} can translate'.format(interpreter = pathNode['value'])
            else:
                output += 'No'
            self.printOutput(output)
        else:
            output = '\n\n--------Function findDirectTranslator --------\n\nWrong Input either {langA} or {langB} not found.'.format(langA = langA, langB = langB)
            self.printOutput(output)

    def findTransRelation(self, langA, langB):
        cloneEdgesList = copy.deepcopy(self.edgesList)
        for edgeNode in cloneEdgesList:
                listVal = edgeNode['listVal']
                listNode = listVal.head
                while (listNode != None):
                    listNode.val['visited'] = False
                    listNode = listNode.next

        source = next((edge for edge in cloneEdgesList if edge['name'] == langA), None)
        respList = []
        pathFound = False
        self.findTransRelationPath(cloneEdgesList, source, langB, respList)
        if (len(respList) != 0):
            respList.insert(0, source['name'])
            pathFound = True
        output = '\n\n--------Function findTransRelation --------\n\nLanguage A: {langA}\n\nLanguage B: {langB}\n\nRelated: No, unfortunately no path found'.format(langA = langA, langB = langB)
        if pathFound == True:
            output = '\n\n--------Function findTransRelation --------\n\nLanguage A: {langA}\n\nLanguage B: {langB}\n\nRelated: Yes, {path} '.format(langA = langA, langB = langB, path = " > ".join(respList))
        self.printOutput(output)
        
        

    def findTransRelationPath(self, edgesList, sourceNode, destinationLang, pathArr):
        itrList = sourceNode['listVal']
        itrNode = itrList.head.next
        itrList.head.val['visited'] = True
        while(itrNode != None):
            if itrNode.val['visited'] == False:
                itrNode.val['visited'] = True
                if itrNode.val['value'] == destinationLang:
                    pathArr.insert(0, itrNode.val['value'])
                    return True
                else:
                    nextNode = next((edge for edge in edgesList if edge['name'] == itrNode.val['value']))
                    val = self.findTransRelationPath(edgesList, nextNode , destinationLang, pathArr)
                    if (val):
                        pathArr.insert(0, itrNode.val['value'])
                        return True
            else:
                return False
            itrNode = itrNode.next
        return pathArr
        


    def findPath(self, source, destination, vertices, edges):
        connectedNodes = [vertices[index] for index, edge in enumerate(edges[source['index']]) if edge == 1]
        for node in connectedNodes:
            childConnectedNodes = [vertices[index] for index, edge in enumerate(edges[node['index']]) if edge == 1]
            for childNode in childConnectedNodes:
                if childNode['value'] == destination['value']:
                    return node
        return None


    def printOutput(self, output):
        with open('outputPS7.txt', 'a') as outputFile:
            outputFile.write(output)

    def printAnalysis(self, analysisOutput):
        with open('analysisPS7.txt', 'a') as outputFile:
            outputFile.write(output)
