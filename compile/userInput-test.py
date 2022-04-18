from classes import *

def full():
    equationString = str(input("Enter your equation: "))
    
    if determineType(equationString) == "Equation":
        equationString = normalise(equationString)
        equationList = convertEquation(equationString)
        lhs = Bracket(genTerms(equationList[0]))
        rhs = Bracket(genTerms(equationList[1]))
        equation = Equation(lhs, rhs)
        
        print("-----------------------------")
        print("Equation:\t" + equation.display())
        equation.sidesPrepare()
        print("Simplified:\t" + equation.display())
        equation.rearrange()
        print("Rearranged:\t" + equation.display())
        print("\nAnswer =\t" + str(round(equation.solve(), 5)))
        print("-----------------------------")
    elif determineType(equationString) == "Bracket":
        bracketString = normalise(equationString)
        bracketString += "="
        bracketList = convertEquation(bracketString)
        bracket = Bracket(genTerms(bracketList[0]))
        
        print("-----------------------------")
        print("Expression:\t" + bracket.display())
        bracket.fullPrepare()
        print("Simplified:\t" + bracket.display())
        print("-----------------------------")

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
    if split[-1] == "":
        split = split[:-1]
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

            toAppend = Bracket(toInsert, genTerms(term)[0].value)
            
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

def countBracket(bracket):
    bracketTracker = []
    deleted = False
    bracketList = copy.deepcopy(bracket)
    prev = []
    current = []
    count = 0
    for item in bracketList:
        if item == "(":
            count += 1
    while True:
        if (bracketList.count("(") > 0) or (bracketList.count(")") > 0):
            if not deleted:
                bracketIndex = countBracketProcess(bracket, deleted)
            bracketIndex = countBracketProcess(bracketList, deleted)
            bracketTracker.append(bracketIndex)
            deleted = True
        
        if len(bracketTracker) == count:
            return bracketTracker


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
                else:
                    bracketList[bracketStart] = " "
                    bracketList[bracketEnd] = " "
                    
                return [bracketStart, bracketEnd]
    return False
        
def delBracketTag(bracketList):
    for index, item in enumerate(bracketList):
        if item == "bracket":
            del bracketList[index]
        elif isinstance(item, list):
            bracketList[index] = delBracketTag(item)
    return bracketList

"""
def genTerms(equationSide):
    termList = []
    
    equationSide = delBracketTag(equationSide)
    
    hasBracket = False
    for item in equationSide:
        if not isinstance(item, (Term, Variable, Bracket)):
            for index, innerItem in enumerate(item):
                if isinstance(innerItem, list):
                    hasBracket = True
                    item[index] = genTerms(innerItem)
    
    if not hasBracket:
        if isinstance(item, (Term, Variable, Bracket)):
            termList.append(item)
        else:
            termList.append(genTermsProcess(equationSide))
    else:
        for item in equationSide:
            if isinstance(item, (Term, Variable, Bracket)):
                termList.append(item)
            else:
                termList.append(genTermsProcess(item))
    return termList#
"""

def genTerms(equationSide): # [+, 6]
    termList = []
    equationSide = delBracketTag(equationSide)
    
    for index, item in enumerate(equationSide):
        if isinstance(item, list):
            tempIndex = index
            generatedTerms = genTerms(item)
            equationSide.pop(index)
            for term in generatedTerms:
                equationSide.insert(tempIndex, term)
                tempIndex +=1
      
    delList = []
      
    for index, item in enumerate(equationSide):
        if isinstance(item, (Term, Variable, Bracket)):
            termList.append(equationSide[index])
            delList.append(equationSide[index])
    for delItem in delList:
        while delItem in equationSide:
            equationSide.remove(delItem)
    if equationSide != []:
        termList.append(genTermsProcess(equationSide))
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

full()
