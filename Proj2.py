#Kyle Easterling
#March 10, 2014
#COSC251 Project 2
##############################################################################

import sys
import shlex

##############################################################################
#Problem 1 methods

class City:
    '''City class holds the user input intersection values in iStart and iEnd,
    and stores the end data in a matrix which is really just a two dimensional
    list.'''
    def __init__ (self):
        self.iStart = list()
        self.iEnd = list()
        self.matrix = list()

def setDimensions(cityList):
    '''Cycles through each city in cityArray, finds the largest intersection
    and appends rows and columns until the city's matrix is of that size.'''
    for city in cityList:
        iMax = 0
        for j in range(len(city.iStart)):
            if city.iStart[j] > iMax:
                iMax = city.iStart[j]
            if city.iEnd[j] > iMax:
                iMax = city.iEnd[j]
        for k in range(iMax+1):
            city.matrix.append(list())
            for n in range(iMax+1):
                city.matrix[k].append(0)
    return

def Problem1():
    '''Takes the user input and stores it into a single string for parsing.
    Stops reading if it detects a -1 in the last read line of input. Sends
    user input to parseCityInput(lines, cityList)'''
    cityList = list()
    endOfInput = False
    lines = ""
    print("Enter Problem 1 input:")
    while(endOfInput == False):
        lines += sys.stdin.readline()
        if("-1" in lines):
            endOfInput = True
            
    parseCityInput(lines, cityList)
    createMatrices(cityList)
    printMatrices(cityList)  
    return

def parseCityInput(lines, cityList):
    '''Takes in a list containing the user input grid as strings and a list
    to contain all the cities.
    Parses the input string from getInput and stores the ordered pairs in
    the related City object.'''
    pairsExpected = 0
    cityNum = -1
    pairStatus = False

    #remove whitespace and split numbers into a list
    inputList = shlex.split(lines)

    for i in inputList:
        if(int(i) == -1):
            if(pairsExpected != 0):
                print("unexpected eof, exiting program")
                sys.exit()
            break
        elif(pairsExpected == 0):
            pairsExpected = int(i)
            cityNum += 1
            cityList.append(City())
        else:
            if(pairStatus == False):
                cityList[cityNum].iStart.append(int(i))
                pairStatus = True
            else:
                cityList[cityNum].iEnd.append(int(i))
                pairStatus = False
                pairsExpected -= 1

    return


def createMatrices(cityList):
    '''Takes in a list of city objects.
    Now that we know how many intersections are in each city and what
    those intersections are, we can create the matrices and determine the
    different paths.
    Calls printMatrices(cityList) to print matrices of all cities in cityList.'''
    #left is the left hand side of an ordered pair, and right is the right
    #hand side.
    #isInfinite is a boolean to notify if a two-way street (or infinite
    #loop) has been detected.
    left = 0
    right = 0
    isInfinite = False
    setDimensions(cityList)

    #go through each city, get the origin pair and call recursiveSearch with
    #it. If it does not return that an infinite loop has been found, increment
    #by 1.
    for city in cityList:
        for j in range(len(city.iStart)):
            isInfinite = False
            left = city.iStart[j]
            right = city.iEnd[j]
            if(city.matrix[left][right] != -1) and (not recursiveSearch(left,right,city,isInfinite)):
                city.matrix[left][right] += 1
            else:
                city.matrix[left][right] = -1
  
    return

def recursiveSearch(left, right, city, isInfinite):
    '''Takes in the left and right coordinates of a street, the city object
    containing that street, and a boolean indicating whether a two way street
    connects to intersection (left,right).
    Recursively goes through every possible path that can be taken from
    the origin pair and returns whether an infinite loop has been found.
    From start to bottom:
    Go through each starting intersection value.
    Check if the value matches the intersection you left from.
    If the current street matches the origin, do nothing and find the next
    matching start value.
    If you have arrived at the original intersection, you have entered an
    infinite loop.
    If the current street is part of an infinite loop, then so must the
    current path.
    If we are already in an infinite loop, the path must be an infinite loop.                   #
    Otherwise, we are fine and can safely increment the possible paths by 1.
    Returns whether a two way street has been found.'''
    for i in range(len(city.iStart)):
        if(city.iStart[i] == right):
            if(left == city.iStart[i]) and (right == city.iEnd[i]):
                continue
            tempRight = city.iEnd[i]
            if(left == tempRight):
                city.matrix[left][tempRight] = -1
                isInfinite = True
                recursiveSearch(left,tempRight,city,isInfinite)
            elif(city.matrix[right][tempRight] == -1):
                city.matrix[left][tempRight] = -1
                continue
            elif(isInfinite):
                city.matrix[left][tempRight] = -1
                isInfinite = recursiveSearch(left,tempRight,city,isInfinite)
            else:
                city.matrix[left][tempRight] += 1
                isInfinite = recursiveSearch(left,tempRight,city,isInfinite)
    return isInfinite

def printMatrices(cityList):
    '''Takes in a list of city objects.
    Prints the matrix of possible routes for each city.'''
    for i in range(len(cityList)):
        print("matrix for city ",i)
        for j in cityList[i].matrix:
            print(j)
    return

##############################################################################
#Problem 2 methods

def Problem2(input):
    '''Takes in a string, "input", and places the input split by whitespace
    into a list.
    Makes sure each word is valid in the sequence and sends it to be evaluated.
    Prints the index of each word, or prints 0 for invalid words.

    >>> input = "ab z ba"
    >>> Problem2(input)
    27
    26
    0
    '''
    words = input.split(" ")
    for word in words:
        valid = True
        if(len(word) >= 1):
            for i in range(0 , (len(word) - 1)):
                if(ord(word[i]) > ord(word[i+1])):
                    valid = False
            if(valid):
                print(lazyEval(word))
            else:
                print("0")
    return

def charToIndex(character):
    '''Returns the integer value of a lower case character as though a
    characters' value ranges from 1 to 26.'''
    return ord(character) - 96

def lazyEval(checkString):
    '''Takes in a word to be evaluated.
    Walks through the entire sequence until the matching word is found.
    This function will work for words greater than 5 letters long, but will
    take longer as words get longer.
    Returns the word's index in the sequence.'''
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    if(len(checkString) > 26):
        return 0

    #We check for all words of length 1 before count is used, so count starts
    #at 26.
    count = 26
    basis = list(alphabet)
    
    #If the string is just a letter in the alphabet, return its value here.
    if checkString in basis:
        return basis.index(checkString) + 1
 
    newList = list()
    for i in range(1, 27):    
        newList.clear()
        #If length of input is less than length of current basis, then we have
        #not found the string and so it doesn't exist.
        if(len(checkString) < len(basis[0])):
            return 0
        #walk through all elements in basis
        for element in basis:
            #Walk from the last element of "element" to 26.
            #So, if element is "ab", then walk from index("b") to 26.
            #Or, if element is "abc", then walk from index("c") to 26, etc.
            for tempIndex in range(charToIndex(element[-1]) , 26):
                tempStr = element + alphabet[tempIndex]
                count = count + 1
                if tempStr == checkString:
                    return count
                newList.append(tempStr)
        #Clear old basis and set it to the set of all valid combinations
        #with the previous length so it can be used for the next length
        #without going through combinations we've already tried.
        basis.clear()
        basis = newList.copy()
        
    return 0

#############################################################################
#Problem 3 methods

def Problem3(input):
    '''Takes in a string of user input.
    Splits equations by whitespace and sends each one to be
    parsed with parseEquation(equation).'''
    equations = input.split(" ")
    
    for equation in equations:
        parseEquation(equation)

    return

def parseEquation(equation):
    '''Takes in an equation.
    Splits the equation into sidesfrom the equals
    sign, then gets each section of each side by splitting again from plus
    signs. Sends each section to sectionParser(sideDict,sectionList), compares
    the dictionaries of the right and left sides and prints whether
    the equation balances or not.

    >>> equation = "C2O2+2H=2HCO"
    >>> parseEquation(equation)
    C2O2+2H=2HCO balances
    '''
    split = equation.find('=')
    lhs = equation[0:split]
    rhs = equation[split+1:len(equation)]
    lhsSections = list()
    rhsSections = list()
    lhsDict = dict()
    rhsDict = dict()
    
    lhsSections = lhs.split('+')
    rhsSections = rhs.split('+')
    
    sectionParser(lhsDict, lhsSections)

    sectionParser(rhsDict, rhsSections)
    
    if(rhsDict == lhsDict):
        print(equation, "balances")
    else:
        print(equation, "does not balance")

    return

def sectionParser(sideDict,sectionList):
    '''Takes in a dictionary and a list of sections of a side of an equation.
    Goes through each section, determines what each character is and acts
    accordingly.
    For coefficients: determines how many characters the coefficient is, then
    stores it.
    For uppercase chars: stores it as the current element (with any trailing
    lowercase chars) and looks for possible trailing subscript. Defaults to 1
    if subscript is not found, then multiplies by that section's coefficient
    before adding the amount of the element into the dictionary.
    For lowercase and subscript: continues to the next character.'''
    for section in sectionList:
        coefficient = 1
        for i in range(0,len(section)):
            if((i == 0) and isInteger(section[i])):
                j = 0
                while(isInteger(section[i+1])):
                    j += 1
                coefficient = int(section[i:j+1])
                continue
            elif(isUppercase(section[i])):
                element = section[i]
                if((i+1) < len(section)):
                    if(isLowercase(section[i+1])):
                        element += section[i+1]
                #this line adds the element with this instance's amount to the
                #dictionary if it isn't already in it. Otherwise, it just adds
                #this instance's amount to the element's existing entry in the
                #dictionary.
                sideDict[element] = (sideDict[element] + checkSubscript(i+1,section,coefficient)) if (element in sideDict) else checkSubscript(i+1,section,coefficient)
                continue
            elif((i+1 < len(section)) and isLowercase(section[i+1])): continue
            elif(isInteger(section[i])): continue

    return

def checkSubscript(i, section, coefficient):
    '''Takes in the index in a section, the section, and the section's co-
    efficient.
    So long as the next character is not an uppercase character,
    add it to the subscript string.
    Returns the coefficient if there is no subscript.
    Otherwise, returns the subscript times the coefficient.'''
    subscript = ""
    while(i < len(section) and not isUppercase(section[i])):
        if not isLowercase(section[i]):
            subscript += section[i]
        i += 1
    if(subscript == ""):
        return coefficient

    return int(subscript) * coefficient

def isUppercase(character):
    '''Takes in a character.
    Returns true if the character is an uppercase letter, else returns false.'''
    if(ord(character) > 64 and ord(character) < 91):
        return True
    return False

def isLowercase(character):
    '''Takes in a character.
    Returns true if the character is a lowercase letter, else returns false.'''
    if(ord(character) > 96 and ord(character) < 193):
        return True
    return False

def isInteger(character):
    '''Takes in a character.
    Returns true if the character is an integer 2 through 9, else returns
    false.'''
    if(ord(character) > 49 and ord(character) < 58):
        return True
    return False

##############################################################################
#Problem 4 methods

class Node:
    '''A node is a point on the grid. Nodes consist of the amount of zombies
    times 5 (so really, the chance of dying), a tuple matching the coords
    of the node, the node that led to this one, and the total chance of
    dying up to this point.'''
    def __init__ (self,zombies,coords):
        self.zombies = zombies
        self.coords = coords
    def setPrevious(self, previous):
        self.previous = previous
    def setTotal(self, total):
        self.total = total


def Problem4():
    '''Gets the size of the grid from user input, then creates a list of that
    size and a two-dimensional list matching the grid input by the user. Then,
    creates a grid of nodes containing each node's chance of dying and
    coordinates.
    Prints the value returned by traverseGrid(grid,size).'''
    grid = list()
    print("Enter Problem 4 input:")
    size = int(input())
    tempGrid = list()

    for i in range(0, size):
        grid.append(list())
        tempGrid.append(input().split(" "))

    for i in range(0, size):
        for j in range(0, size):
            grid[i].append(Node((int(tempGrid[i][j]) * 5), (i, j)))
    
    print(traverseGrid(grid, size))
    
    return

def traverseGrid(grid, size):
    '''Takes in a grid of nodes and the size (equal to both length and width
    of the grid).
    This method is modeled after Dijkstra's algorithm. We keep a set of all
    the edges of the nodes we have traversed. We look through the set for the
    edge with the best chance of survival (plus the total chance of survival
    from the start until that edge!) and move to the connected node. We update
    that node to link to the path that led to it, remove it from our list of
    known edges and add any new edges connecting to that node. If that node is
    the destination, then we are finished.
    This would also make it very easy to print the best path should there be
    reason to.
    Returns the best possible chance of survival.'''
    edgeSet = set()
    start = grid[0][size-1]
    start.setTotal(start.zombies)
    end = grid[size-1][0]
    destination = False

    addEdges(edgeSet, grid, start, size)

    while(not destination):
        lowest = 100

        for edge in edgeSet:
            if((edge[1].zombies + edge[0].total) < lowest):
                bestNode = edge[1]
                bestPrevious = edge[0]
                lowest = bestNode.zombies + bestPrevious.total

        if(lowest == 100):
            print("You will die.")
            return

        bestNode.setTotal(bestPrevious.total +  bestNode.zombies)
        bestNode.setPrevious(bestPrevious)
        edgeSet.remove((bestPrevious, bestNode))
        addEdges(edgeSet,grid,bestNode,size)
        
        if(bestNode == end):
            destination = True
    
    return 100 - bestNode.total

    return

def addEdges(edgeSet, grid, node, size):
    '''Takes in the set of all known edges, the grid of nodes, the current
    node, and the grid size.
    If the nodes above and to the right of the current node are valid, add new
    edges. (an edge is a tuple of a traversed node and an unknown node above it
    or to its right)'''
    i = node.coords[0]
    j = node.coords[1]
    if(i+1 < size):
        edgeSet.add((node, grid[i+1][j]))
    if(j-1 > -1):
        edgeSet.add((node, grid[i][j-1]))

    return

if __name__ == "__main__":
    import doctest
    doctest.testmod()
