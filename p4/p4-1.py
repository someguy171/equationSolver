from copy import deepcopy
from tokenize import Triple

from numpy import diff
from classes import *

def full(equationString):
    if determineType(equationString) == "Equation":
        equationString = normalise(equationString)
        equation = convertEquation(equationString)
        lhs = Bracket(genTerms(equation[0]))
        rhs = Bracket(genTerms(equation[1]))
        return Equation(lhs, rhs)

def determineType(equationString):
    if "=" in equationString:
        return "Equation"
    elif "=" not in equationString:
        return "Bracket"

def normalise(equationString):
    return equationString.replace(" ", "")

def convertEquation(equationString):
    split = equationString.split("=")
    equation = []
    for side in split:
        side = list(side)
        differences = [0]
        while len(differences) > 0:
            bracketsTracker = countBracket(side)
            if bracketsTracker == []:
                differences = []
                convert = True
                while convert == True:
                    convert = False
                    for index, item in enumerate(side):
                        if isinstance(item, list):
                            if item[-1] == "bracket":
                                side[index] = side[index][0]
                                convert = True
                    if convert == True:
                        side = convertBracket(side)
            else:
                differences = []
                for index, item in enumerate(bracketsTracker):
                    differences.append(item[1] - item[0])
                
                targetIndex = min(range(len(differences)), key=differences.__getitem__)
                expandedBracket = [convertBracket(side[bracketsTracker[targetIndex][0]:bracketsTracker[targetIndex][1]-1]), "bracket"]
                side[bracketsTracker[targetIndex][0]:bracketsTracker[targetIndex][1]-1] = [expandedBracket]
        equation.append(side)
    return equation

def convertBracket(bracketList):
    if (not isinstance(bracketList[0], list)) and (bracketList[0] != "-"):
        bracketList.insert(0, "+")
    
    termList = []
    term = []
    finding = False
    
    for index, character in enumerate(list(bracketList)):
        if character in ["-", "+"]:
            if finding:
                termList.append(term)
                term = []
                finding = False
            if not finding:
                term.append(character)
                finding = True
        if isinstance(character, list) and finding:
            tagCheck = False
            if character[-1] == "bracket":
                tagCheck = True
                character = character[:-1]
            
            toInsert = []
            for item in character:
                generatedTerms = genTerms(item)
                for item in generatedTerms:
                    toInsert.append(item)

            toAppend = Bracket(toInsert, genTerms([term])[0].value)
            
            if tagCheck:
                toAppend = [toAppend]
                toAppend.append("bracket")
                
            termList.append(toAppend)
            term = []
            finding = False
        elif isinstance(character, Bracket):
            termList.append(character)
        elif character.isalnum() or character == ".":
            term.append(character)
    
    if term != []:
        termList.append(term)
    return termList

def countBracket(bracketList):
    bracketTracker = []
    deleted = False
    prev = []
    current = []
    while True:
        if (bracketList.count("(") > 0) or (bracketList.count(")") > 0):
            bracketIndex = countBracketProcess(bracketList, deleted)
            bracketTracker.append(bracketIndex)
            deleted = True
        
        current = bracketTracker
        if current == prev:
            return bracketTracker
        else:
            prev = current
    

def countBracketProcess(bracketList, deleted):
    foundPair = False
    for index, character in enumerate(bracketList):
        if not foundPair:
            if character == "(":
                bracketStart = index
            elif character == ")":
                bracketEnd = index
                foundPair = True
                if not deleted:
                    del bracketList[bracketStart]
                    del bracketList[bracketEnd - 1]
                return [bracketStart, bracketEnd]
        
def delBracketTag(bracketList):
    for index, item in enumerate(bracketList):
        if item == "bracket":
            del bracketList[index]
        elif isinstance(item, list):
            bracketList[index] = delBracketTag(item)
    return bracketList

def genTerms(equationSide):
    termList = []
    
    equationSide = delBracketTag(equationSide)
    
    for item in equationSide:
        if not isinstance(item, (Term, Variable, Bracket)):
            for index, innerItem in enumerate(item):
                if isinstance(innerItem, list):
                    item[index] = genTerms(innerItem)
    
    for item in equationSide:
        if isinstance(item, (Term, Variable, Bracket)):
            termList.append(item)
        else:
            termList.append(genTermsProcess(item))
    return termList

def genTermsProcess(termBracket):
    unknown = ""
    sign = termBracket.pop(0)
    if termBracket == []:
        termBracket = ["1"]
    value = "".join(termBracket)
    
    testVal = value
    testVal = testVal.replace("(", "")
    testVal = testVal.replace(")", "")
    testVal = testVal.replace(".", "")
    
    if not testVal.isnumeric():
        value = list(value)
        for index, character in enumerate(value):
            if character.isalpha():
                unknown = value.pop(index)
        
        # no coefficient (just x means x got taken out on line176, so set coefficient to 1)
        if value == []:
            value = ["1"]
        
        value = "".join(value)
        if sign == "-":
            value = "-" + value
        
        return Variable(float(value), unknown)
    else:
        if sign == "-":
            value = "-" + value
        
        return Term(float(value))

equation = str(input("Enter your equation: "))
# 3x +5 =87 - 5(5x -6)

full(equation).display()
