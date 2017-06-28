# -*- coding: utf-8 -*-
rows = 'ABCDEFGHI' #list of rows
cols = '123456789'#list of cols

def cross(a, b): #dunction definition so it can be used in console (no return type?)
    return [s+t for s in a for t in b]  #concatination of 2 strings by going through every rows/ cols -> ('A1')

boxes = cross(rows, cols) #list returned from cross() -> ['A1','A2',....] = all the possible positions

row_units = [cross(r, cols) for r in rows] #list of rowlists [['A1,'A2',..],['B1','B2',...],[...]]
column_units = [cross(rows, c) for c in cols] #list of columnlists [['A1','B1',..],['A2','B2',...]]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')] #list of [[A1,A2,A3,B1,B2,B3,C1,C2,C3],[A4,A5,...],[..]]
unitlist = row_units + column_units + square_units #list of all places but divided into lists and boxes specifically for sudoku game
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
#creates key-value pairs where key is position symbol eg "A1" and values are row, col and box where A1 is reference to sudoku rules
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
#sum(list1,list22) adds list1 to list2 not caring what is in list2. It adds one by on every position on list1 despite it being multiple lists or so  
#(sum(units[s],[]))-set([s]) removes s from the result list
#dict(..) creates a dictionary so by typing key like "A1" we get values = list of every other position key that has has an impact on the number for solving sudoku

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = [] #create list that will be added as values for ceach key
    for c in grid: #for every character 
        if c in cols: #if character is one of the number represented by cols notation 
            chars.append(c) #append this value as a solution
        if c == '.':
            chars.append(cols) #if character is dot (.) append all possible solutions 
    assert len(chars) == 81 #if entered grid is valid and has 81 characters
    return dict(zip(boxes, chars))#zip() aggragates (joins) values that has the same index from each list into (key, value) pairs where list1[x] = key, list2[x] = value - return tuple 


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
            
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
