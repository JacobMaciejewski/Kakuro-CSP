#import kakuro
import csp
import kakuro
import time
import search

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

def getProperKakuroBoard(complexity):
    if(complexity == 2):
        return kakuro2
    elif(complexity == 3):
        return kakuro3
    elif(complexity == 4):
        return kakuro4
    else:
        return kakuro1

if __name__ == "__main__":
    print("Choose between two algorithms:")
    print("Insert 'F' for forward checking with MRV heuristic")
    print("Insert 'M' for MAC algorithm (default)")
    algorithm = input()
    print("Choose between 4 levels of complexity (1 is the default):")
    complexity = int(input())

    #getting the one of the 4 boards
    myKakuroBoard = getProperKakuroBoard(complexity)
    myProblem = kakuro.Kakuro(myKakuroBoard)

    if(algorithm == 'F'):
        start_time = time.time()
        csp.backtracking_search(myProblem, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
        elapsed_time = time.time() - start_time
        #time and number of assignments are the best metric methods
        print("Elapsed time for FC with MRV: ",elapsed_time)
        print("Number of assigns: ", myProblem.nassigns)
    else:
        start_time = time.time()
        csp.backtracking_search(myProblem, inference = csp.mac)
        elapsed_time = time.time() - start_time
        #time and number of assignments are the best metric methods
        print("Elapsed time for MAC: ",elapsed_time)
        print("Number of assigns: ", myProblem.nassigns)

    print("Display of the board:")
    myProblem.display()
