# -*- coding: utf-8 -*-
from utils import *
from utils import *

def solveSudoku(values):
    #The method keys() returns a list of all the available keys in the dictionary.
    
    #we create a list [..] of all the box ["A1"] etc. that value of (which is a list) has length of 1
    #havling that list we just fint length od that list and so we know how many fields are solved
    stuck = False; #boolean
    while not stuck: #while function
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1]) #length of the list of all the boxes(lists[]) that has only 1 value - the solution 
        values = eliminate(values) #use elimination strategy and assign the result to variable values
        values = only_choice(values) #the same but only 1 choice strategy
        solved_values_after = len([box for box in values.keys() if len(values[box])==1]) #check if any solution where resolved
        stuck = solved_values_before == solved_values_after #if nothing was solved stop iterating
        #print(stuck) 
        if len([box for box in values.keys() if len(values[box]) == 0]): #"SANITY CHECK" if there is a box with no solution avaliable
            return False #returns False since we cant get the solution without the value for this box        
    return values #if no solution was equal to 0 or nothing return the solved values


def search1(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = solveSudoku(values)
    if values is False: #???????
        print("FALES returned")
        return False ## Failed earlier
    # Choose one of the unfilled squares with the fewest possibilities
    boxMinList = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)  
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[boxMinList[0]]: #take each value from lowest length list
        new_sudoku = values.copy() #copy sudoku
        new_sudoku[boxMinList[0]] = value #put our temp va;lue to new sudoku
        attempt = search1(new_sudoku) #apparently python recognises any value as true and only False as false
        if attempt: #False is only returned if nothing was solved - in that case stop recursion and go to the next key from minLengthList aand try again
            return attempt #if something was solved return attempt = redu the function search
        
def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = solveSudoku(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1) #returns tuple (val and key)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy() #copy sudoku
        new_sudoku[s] = value #put our temp va;lue to new sudoku
        attempt = search(new_sudoku) #False is only returned if nothing was solved - in that case stop recursion and go to the next key from minLengthList aand try again
        #recusrsion
        if attempt: #False is only returned if nothing was solved - in that case stop recursion and go to the next key from minLengthList aand try again
            return attempt #if something was solved return attempt = redu the function search
