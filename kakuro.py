import csp

kakuro1 = [['*', '*', '*', [6, ''], [3, '']],
           ['*', [4, ''], [3, 3], '_', '_'],
           [['', 10], '_', '_', '_', '_'],
           [['', 3], '_', '_', '*', '*']]

# difficulty 0
kakuro2 = [
    ['*', [10, ''], [13, ''], '*'],
    [['', 3], '_', '_', [13, '']],
    [['', 12], '_', '_', '_'],
    [['', 21], '_', '_', '_']]

# difficulty 1
kakuro3 = [
    ['*', [17, ''], [28, ''], '*', [42, ''], [22, '']],
    [['', 9], '_', '_', [31, 14], '_', '_'],
    [['', 20], '_', '_', '_', '_', '_'],
    ['*', ['', 30], '_', '_', '_', '_'],
    ['*', [22, 24], '_', '_', '_', '*'],
    [['', 25], '_', '_', '_', '_', [11, '']],
    [['', 20], '_', '_', '_', '_', '_'],
    [['', 14], '_', '_', ['', 17], '_', '_']]

# difficulty 2
kakuro4 = [
    ['*', '*', '*', '*', '*', [4, ''], [24, ''], [11, ''], '*', '*', '*', [11, ''], [17, ''], '*', '*'],
    ['*', '*', '*', [17, ''], [11, 12], '_', '_', '_', '*', '*', [24, 10], '_', '_', [11, ''], '*'],
    ['*', [4, ''], [16, 26], '_', '_', '_', '_', '_', '*', ['', 20], '_', '_', '_', '_', [16, '']],
    [['', 20], '_', '_', '_', '_', [24, 13], '_', '_', [16, ''], ['', 12], '_', '_', [23, 10], '_', '_'],
    [['', 10], '_', '_', [24, 12], '_', '_', [16, 5], '_', '_', [16, 30], '_', '_', '_', '_', '_'],
    ['*', '*', [3, 26], '_', '_', '_', '_', ['', 12], '_', '_', [4, ''], [16, 14], '_', '_', '*'],
    ['*', ['', 8], '_', '_', ['', 15], '_', '_', [34, 26], '_', '_', '_', '_', '_', '*', '*'],
    ['*', ['', 11], '_', '_', [3, ''], [17, ''], ['', 14], '_', '_', ['', 8], '_', '_', [7, ''], [17, ''], '*'],
    ['*', '*', '*', [23, 10], '_', '_', [3, 9], '_', '_', [4, ''], [23, ''], ['', 13], '_', '_', '*'],
    ['*', '*', [10, 26], '_', '_', '_', '_', '_', ['', 7], '_', '_', [30, 9], '_', '_', '*'],
    ['*', [17, 11], '_', '_', [11, ''], [24, 8], '_', '_', [11, 21], '_', '_', '_', '_', [16, ''], [17, '']],
    [['', 29], '_', '_', '_', '_', '_', ['', 7], '_', '_', [23, 14], '_', '_', [3, 17], '_', '_'],
    [['', 10], '_', '_', [3, 10], '_', '_', '*', ['', 8], '_', '_', [4, 25], '_', '_', '_', '_'],
    ['*', ['', 16], '_', '_', '_', '_', '*', ['', 23], '_', '_', '_', '_', '_', '*', '*'],
    ['*', '*', ['', 6], '_', '_', '*', '*', ['', 15], '_', '_', '_', '*', '*', '*', '*']]




class Kakuro(csp.CSP):
    def __init__(self, kakuroBoard):
        #board contains the input board
        #necessary for groups initialization
        self.board = kakuroBoard
        self.setGroups()
        #print(self.groups)
        variables = self.getVariables()
        #print("VARIABLES:")
        #print(variables)
        #each empty slot can get a value in range [1,9]
        domains = {v: list(range(1,10)) for v in variables}
        #getting all neighbours of each variable with the help of groups set
        #with self.getNeighbors
        csp.CSP.__init__(self, variables, domains, self.getNeighbors(variables), self.kakuro_constraint)
        #self.display(self.infer_assignment)

    def display(self):
        assignment = self.infer_assignment()
        numOfRows = len(self.board)
        numOfColumns = len(self.board[0])
        lastRow = numOfRows - 1
        lastColumn = numOfColumns - 1

        for row in range(numOfRows):
            for column in range(numOfColumns):
                currentBlock = self.board[row][column]
                if(self.isNumBlock(currentBlock)):
                    print(' ',assignment[(row + 1, column + 1)],' ', end='')
                elif(self.isWallBlock(currentBlock)):
                    print(' ','*',' ', end='')
                else:
                    print(currentBlock, end='')
                if(column == lastColumn):
                    print('\n')



    def kakuro_constraint(self, A, a, B, b):
        #can get all keen neighbours of A and B through A
        Aneighbors = self.neighbors[A]

        #B is not contained in the neighbors of A
        if(B not in Aneighbors):
            return True

        #used to get the limit of the group in O(1)
        groupsOfA = self.getVariableGroups(A)
        #final group we have to check for
        keenGroup = []

        #A and B are on the same row
        if(A[0] == B[0]):
            #getting the limit from the first element of the row group
            limit = groupsOfA[0][0]
            #keen neighbours of A and B
            for member in Aneighbors:
                if(member[0] == A[0]):
                    keenGroup.append(member)
            #A in not included in its neighbours
            keenGroup.append(A)

            return self.evaluateGroup(keenGroup, limit, A, B, a, b)
        #A and B are on the same column
        elif(A[1] == B[1]):
            #getting the limit from the first element of the column group
            limit = groupsOfA[1][0]
            #keen neighbours of A and B
            for member in Aneighbors:
                if(member[1] == A[1]):
                    keenGroup.append(member)
            #A in not included in its neighbours
            keenGroup.append(A)

            return self.evaluateGroup(keenGroup, limit, A, B, a, b)

    #returns True if the variables A and B conflict with each other
    #else returns False
    def evaluateGroup(self, keenGroup, limit, A, B, a, b):
        currentAssignments = self.infer_assignment()
        numOfAssignments = 0
        totalGroupValue = 0

        #assigning the same value to A and B is illegal
        if(a == b):
            return False

        #for each point in group
        for point in keenGroup:
            if(point == A):
                totalGroupValue += a
                numOfAssignments += 1
            elif(point == B):
                totalGroupValue += b
                numOfAssignments += 1
            #checking if point has an already assigned value
            elif point in currentAssignments:
                totalGroupValue += currentAssignments[point]
                numOfAssignments += 1

        if(numOfAssignments == len(keenGroup)):
            return (totalGroupValue == limit)
        else:
            return (totalGroupValue < limit)


    def getVariables(self):
        numOfRows = len(self.board)
        numOfColumns = len(self.board[0])
        kakuroVariables = []

        #traversing board in search of empty blocks
        for row in range(numOfRows):
            for column in range(numOfColumns):
                currentBlock = self.board[row][column]
                if(self.isNumBlock(currentBlock)):
                    kakuroVariables.append((row + 1, column + 1))
        #kakuro variables as list
        return kakuroVariables

    #producing a dictionary pointing to set of neighbors for each variable
    def getNeighbors(self, variables):
        allNeighbors = dict()

        for var in variables:
            varNeighbors = self.getVarNeighbors(self.getVariableGroups(var))
            #removing var from its neighbours
            varNeighbors.discard(var)
            allNeighbors[var] = varNeighbors

        return allNeighbors


    def groupToSet(self, group):
        start = group[1]
        end = group[2]
        groupAsList = []

        #same row, getting all the points between start and end of group
        if(start[0] == end[0]):

            for i in range(start[1] + 1, end[1]):
                groupAsList.append((start[0], i))

            groupAsSet = set(groupAsList)
        else:
            for i in range(start[0] + 1, end[0]):
                groupAsList.append((i, start[1]))

            groupAsSet = set(groupAsList)

        return groupAsSet

    def getVarNeighbors(self, variableGroups):
        rowGroup = variableGroups[0]
        columnGroup = variableGroups[1]

        #special case when there is not row group
        if(len(variableGroups[0]) != 0):
            tempRowGroup = rowGroup[:]
            set1 = self.groupToSet(tempRowGroup)
        else:
            set1 = {}

        if(len(variableGroups[1]) != 0):
            tempColumnGroup = columnGroup[:]
            set2 = self.groupToSet(tempColumnGroup)
        else:
            set2 = {}

        return set1.union(set2)




    #returns the two groups that contain variable
    def getVariableGroups(self, variable):
        #getting variable's coordinates
        varRow = variable[0] - 1
        varColumn = variable[1] - 1
        variableGroups = []

        #getting the two sublists of the general group list
        rowGroups = self.groups[0][varRow]
        columnGroups = self.groups[1][varColumn]

        #looking for variable's row group
        found = False
        for rowGroup in rowGroups:
            if(self.isInGroup(variable, rowGroup)):
                found = True
                variableGroups.append(rowGroup)
                break
        #no group in row
        if(not found):
            variableGroups = []

        #looking for variable's column group
        found = False
        for columnGroup in columnGroups:
            if(self.isInGroup(variable, columnGroup)):
                found = True
                variableGroups.append(columnGroup)
                break

        #no group in column
        if(not found):
            variableGroups.append([])

        return variableGroups

    #checks if variable is contained in the group
    def isInGroup(self, variable, group):
        xAxis = variable[0]
        yAxis = variable[1]

        #no variable in empty group
        if(len(group) == 0):
            return False

        #first and last point of group
        start = group[1]
        end = group[2]

        #a row group
        if(start[0] == end[0]):
            if(start[1] < yAxis < end[1]):
                return True
            else:
                return False
        else:#a column group
            if(start[0] < xAxis < end[0]):
                return True
            else:
                return False

    #initializing row and column groups
    def setGroups(self):
        self.groups = []
        numOfRows = len(self.board)
        numOfColumns = len(self.board[0])
        lastRow = numOfRows - 1
        lastColumn = numOfColumns - 1
        groupsList = []
        currentGroup = []
        currentRowList = []
        currentColumnList = []

        #getting all constraint groups for each row
        for row in range(numOfRows):
            currentRowList = []
            for column in range(numOfColumns):
                currentBlock = self.board[row][column]
                #found a constraint block, new group initialized
                if(self.isRowConstraintBlock(currentBlock) and not currentGroup):
                    currentGroup.append(self.getSecondConstraintFromBlock(currentBlock))
                    currentGroup.append((row + 1, column + 1))

                #found a wall, got to the end of a group
                elif(self.isWallBlock(currentBlock) and len(currentGroup) == 2):
                    currentGroup.append((row + 1, column + 1))
                    currentRowList.append(currentGroup)
                    currentGroup = []
                #found a new constraint block, got to the end of a group, initializing a new one
                elif(self.isConstraintBlock(currentBlock) and len(currentGroup) == 2):
                    #adding new constraint block as the last point of the group
                    currentGroup.append((row + 1, column + 1))
                    currentRowList.append(currentGroup)
                    currentGroup = []
                    if(self.isRowConstraintBlock(currentBlock)):
                        #setting new constraint block as the first point of the group
                        currentGroup.append(self.getSecondConstraintFromBlock(currentBlock))
                        currentGroup.append((row + 1, column + 1))
                #got to the end of the row ending with an empty slot
                elif(self.isNumBlock(currentBlock) and column == lastColumn and len(currentGroup) == 2):
                    #adding the last point of row into the last group
                    currentGroup.append((row + 1, column + 2))
                    currentRowList.append(currentGroup)
                    currentGroup = []
            #adding the groups of the row, into the general list of the rows groups
            groupsList.append(currentRowList)

        #rows groups added into the general list of groups at position 0
        self.groups.append(groupsList)

        #same procedure for columns
        groupsList = []
        currentGroup = []

        for column in range(numOfColumns):
            currentColumnList = []
            for row in range(numOfRows):
                currentBlock = self.board[row][column]
                #self.printType(currentBlock)

                if(self.isColumnConstraintBlock(currentBlock) and not currentGroup):
                    currentGroup.append(self.getFirstConstraintFromBlock(currentBlock))
                    currentGroup.append((row + 1, column + 1))

                elif(self.isWallBlock(currentBlock) and len(currentGroup) == 2):
                    currentGroup.append((row + 1, column + 1))
                    currentColumnList.append(currentGroup)
                    currentGroup = []
                #found a new constraint block, end of group, new group if column constraint block
                elif(self.isConstraintBlock(currentBlock) and len(currentGroup) == 2):
                    currentGroup.append((row + 1, column + 1))
                    currentColumnList.append(currentGroup)
                    currentGroup = []
                    #current block is a column constraint block, initializing a new group
                    if(self.isColumnConstraintBlock(currentBlock)):
                        currentGroup.append(self.getFirstConstraintFromBlock(currentBlock))
                        currentGroup.append((row + 1, column + 1))
                elif(self.isNumBlock(currentBlock) and row == lastRow and len(currentGroup) == 2):
                    currentGroup.append((row + 2, column + 1))
                    currentColumnList.append(currentGroup)
                    currentGroup = []


            groupsList.append(currentColumnList)
        #adding the groups of columns into the general set of groups
        self.groups.append(groupsList)

    def getBlockTypeID(self, block):
        if(isinstance(block, list)):
            return 1
        elif(block == '_'):
            return 2
        else:
            return 3

    def printType(self, block):
        if(isinstance(block, list)):
            return 1
        elif(block == '_'):
            return 2
        else:
            return 3

    def isConstraintBlock(self, block):
        return self.getBlockTypeID(block) == 1

    def isNumBlock(self, block):
        return self.getBlockTypeID(block) == 2

    def isWallBlock(self, block):
        return self.getBlockTypeID(block) == 3

    def isRowConstraintBlock(self, block):
        if(self.isConstraintBlock(block)):
            if(isinstance(block[1], int)):
                return True
            else:
                return False
        return False

    def isColumnConstraintBlock(self, block):
        if(self.isConstraintBlock(block)):
            if(isinstance(block[0], int)):
                return True
            else:
                return False
        return False

    def getFirstConstraintFromBlock(self, block):
        return block[0]

    def getSecondConstraintFromBlock(self, block):
        return block[1]
