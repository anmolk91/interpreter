from interpreter import Interpreter

def driverMethod(pathName):
    interpretersData = Interpreter()
    interpretersData.readApplication(pathName)
    # print(interpretersData.edges)
    # print(interpretersData.vertices)
    interpretersData.findTransRelation('Hindi   ', '  Gujarati   ')

driverMethod('hello-world.txt')