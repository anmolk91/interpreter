import copy
from functools import reduce
from node import Node
from linkedlist import LinkedList

class Interpreter:
    """
        Interpreter class defines a relation between interpreters and languages
        providing inbuilt functions like finding transRelations or a direct translator for languages
        also provides minimum no of translators that would be required to cover all languages
    """
    vertices = []
    edges = []
    edgesList = None

    def readApplication(self, inputFile = 'inputPS7.txt', promptsFile = 'promptsPS7.txt'):
        """ Reads the file using the file path provided.
            if file paths not provided then takes default path into account
            takes inputFile for the input data containing list of interpreters and languages they speak
            takes promptsFile for the prompts or actions that needs to be performed on the input provided
        """
        inputFileContent = self.getFileContent(inputFile, 'r')
        promptsFileContent = self.getFileContent(promptsFile, 'r')
        self.processInputData(inputFileContent)
        self.processPromptsData(promptsFileContent)

    def getFileContent(self, filePath, mode):
        """
            opens file in the mode provided and returns of the file
        """
        with open(filePath, mode) as my_file:
            return my_file.read()

    def processInputData(self, unformattedData):
        """
            reads the unformatted data from the input file and converts it to meaningful data structure
            creates vertices, adjacency matrix and adjacency list
        """
        tempList = unformattedData.split('\n')
        rawNodes = copy.copy(list(self.filterRawNodes(tempList)))
        self.vertices = self.createVertices(rawNodes)
        self.edges = self.createEdges(rawNodes, self.vertices)
        self.createEdgesList(rawNodes, self.vertices)

    def processPromptsData(self, unformattedPromptsData):
        """
            processes unformatted data from the prompts file
            calls execution method which executes the prompts
        """
        tempList = unformattedPromptsData.split('\n')
        self.executeActions(tempList)

    def executeActions(self, rawDataList):
        """
            prompts from the prompts file are checked
            accordingly functions are exectured as per the prompt
        """
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
        """
            raw data from the input file is filtered
        """
        def filterFun(str):
            if ('/' in str):
                return True
            else:
                return False
        return filter(filterFun, data)

    
    def createVertices(self, rawData):
        """
            creates vertices/nodes for the input data provided
            each node is a dict object seggregated as type of interpreter or language
        """
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
        """
            creates adjacency matrix which defines the relationship between nodes
        """
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
        """
            creates adjacency list for the vertices and the edges
        """
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
        """
            function displays the total number of unique candidates and languages
        """
        (filteredInterpreters, filteredLanguages) = (self.getFilteredInterpreters(self.vertices), self.getFilteredLanguages(self.vertices))
        output = '--------Function showAll--------'
        output += '\n\nTotal no. of candidates: {totalCandidates}\nTotal no. of languages: {totalLangugages}'.format(totalCandidates = len(filteredInterpreters), totalLangugages = len(filteredLanguages))
        output += '\n\nList of candidates:'
        for candidate in filteredInterpreters:
            output += '\n\n'+ candidate['value'].title()
        output += '\n\n\nList of languages:'
        for language in filteredLanguages:
            output += '\n\n'+ language['value'].title()
        analysisOutput = '\n\n--------Function showAll--------\n\nWorst Complexity will be O(n) where n is the total no of nodes\n\n 3 iterations were executed twice to filter data for language and interpreters and third loop for creating output which was divided as a sum of no interpreters and the languages that can be spoken'
        self.printOutput(output)
        self.printAnalysis(analysisOutput)


    def getFilteredInterpreters(self, data):
        """
            filter function use to filter interpreters in the vertices
        """
        def filterInterPreters(dataItem):
            return dataItem['type'] == 'interpreter'
        return list(filter(filterInterPreters, data))
    
    def getFilteredLanguages(self, data):
        """
            filter function use to filter language in the vertices
        """
        def filterLanguage(dataItem):
            return dataItem['type'] == 'language'
        return list(filter(filterLanguage, data))


    def displayHireList(self):
        """
            function displays the minimum number of candidates that need to be hired to cover all the languages
        """
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
        self.printAnalysis('\n\n--------Function displayHireList--------\n\nFunction for time complexity is F(n) = (n^2 + nlog(n) + n^2)\n\nWorst Complexity = O(n^2)\n\n')

    def displayCandidates(self, language):
        """
             function displays all the candidates who can speak a particular language
        """
        vertex = next((node for node in self.vertices if node['value'].lower() == language.strip().lower()), None)
        outputStr = '\n\n--------Function displayCandidates --------\n\nList of Candidates who can speak {language}:'.format(language = language)
        if (vertex == None):
            self.printOutput('\n\n--------Function displayCandidates --------\n\n No language found with this name')
        else :
            outputData = [self.vertices[index] for index, value in enumerate(self.edges[vertex['index']]) if value == 1]
            for outputDataItem in outputData:
                outputStr += '\n\n{name}'.format(name = outputDataItem['value'].title())
            self.printOutput(outputStr)
            self.printAnalysis('\n\n--------Function displayCandidates --------\n\nFunction for time complexity is F(n) = (n + n)\n\nWorst Complexity = O(n)\n\n')

    def findDirectTranslator(self, langA, langB):
        """
            function find one candidate can directly translate from language A to language B
        """
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
            self.printAnalysis('\n\n--------Function findDirectTranslator --------\n\nFunction for time complexity is F(n) = (n^2)\n\nWorst Complexity = O(n^2)\n\n')
        else:
            output = '\n\n--------Function findDirectTranslator --------\n\nWrong Input either {langA} or {langB} not found.'.format(langA = langA, langB = langB)
            self.printOutput(output)

    def findTransRelation(self, langA, langB):
        """
            function finds out if two languages are related to each other
        """
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
        self.printAnalysis('\n\n--------Function findTransRelation --------\n\nFunction for time complexity is F(t) = f(n) + f(e) where f is a function of traversing each nodes and a function for traversing through each edge\n\nWorst Complexity = O(N + E)')
        
        

    def findTransRelationPath(self, edgesList, sourceNode, destinationLang, pathArr):
        """
            dfs traversal of the edges to find a path between sourceNode which contains the source language and the destination language
            uses adjacency list for traversing
        """
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
        """
            bfs traversal to find out a direct translator between the languages
            uses adjacency matrix to traverse between each vertices
        """
        connectedNodes = [vertices[index] for index, edge in enumerate(edges[source['index']]) if edge == 1]
        for node in connectedNodes:
            childConnectedNodes = [vertices[index] for index, edge in enumerate(edges[node['index']]) if edge == 1]
            for childNode in childConnectedNodes:
                if childNode['value'] == destination['value']:
                    return node
        return None


    def printOutput(self, output):
        """
            prints the output for the functions in the output file
        """
        with open('outputPS7.txt', 'a') as outputFile:
            outputFile.write(output)

    def printAnalysis(self, analysisOutput):
        """
            prints the time analysis for each function in the analysis file
        """
        with open('analysisPS7.txt', 'a') as outputFile:
            outputFile.write(analysisOutput)
