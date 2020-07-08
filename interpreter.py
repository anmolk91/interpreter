import copy
from functools import reduce

class Interpreter:
    vertices = []
    edges = []
    actions = []
    output = ''

    def readApplication(self, inputfile):
        if inputfile == '' or inputfile == None:
            return

        fileContent = self.getFileContent(inputfile, 'r')
        self.processData(fileContent)

    def getFileContent(self, filePath, mode):
        with open(filePath, mode) as my_file:
            return my_file.read()

    def processData(self, unformattedData):
        tempList = unformattedData.split('\n')
        rawNodes = copy.copy(list(self.filterRawNodes(tempList)))
        self.actions = self.filterActions(tempList)
        self.vertices = self.createVertices(rawNodes)
        self.edges = self.createEdges(rawNodes, self.vertices)

    def filterActions(self, rawDataList):
        actions = ['showAll']
        actionsToBeProcessed = []
        for dataItem in rawDataList:
            if dataItem in actions:
                actionsToBeProcessed.append(dataItem)
        return actionsToBeProcessed

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
        self.printOutput(output)

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

    def findTransRelation(self, langA, langB):
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


    def findPath(self, source, destination, vertices, edges):
        connectedNodes = [vertices[index] for index, edge in enumerate(edges[source['index']]) if edge == 1]
        for node in connectedNodes:
            childConnectedNodes = [vertices[index] for index, edge in enumerate(edges[node['index']]) if edge == 1]
            for childNode in childConnectedNodes:
                if childNode['value'] == destination['value']:
                    return node
        return None


    def printOutput(self, output):
        with open('output.txt', 'a') as outputFile:
            outputFile.write(output)
