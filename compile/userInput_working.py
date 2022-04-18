from classes import *

# a function to run the whole program (user input, simplifying, solving)
def full():
    # user inputs their equation
    equationString = str(input("Enter your equation: "))
    
    # if it is an equation...
    if determineType(equationString) == "Equation":
        # remove spaces
        equationString = normalise(equationString)
        
        # convert each side, splitting up each term and bracket
        equationList = convertEquation(equationString)
        
        # form a left- and right-hand side from the converted sides
        lhs = Bracket(genTerms(equationList[0]))
        rhs = Bracket(genTerms(equationList[1]))
        
        # form a full Equation using the LHS and RHS
        equation = Equation(lhs, rhs)
        
        # display the final answers to the user
        print("-----------------------------")
        print("Equation:\t" + equation.display())                   # first, display the original equation
        equation.sidesPrepare()
        print("Simplified:\t" + equation.display())                 # second, display the equation with both sides simplified
        equation.rearrange()
        print("Rearranged:\t" + equation.display())                 # third, display the rearranged equation
        print("\nAnswer =\t" + str(round(equation.solve(), 5)))     # lastly, display the answer, rounded to 5dp
        print("-----------------------------")
    
    # if it is an expression
    elif determineType(equationString) == "Bracket":
        # remove spaces
        bracketString = normalise(equationString)
        
        # add an equals sign to the end
        # this makes it appear as an equation, but only one side of it will be converted
        bracketString += "="
        
        # convert the expression, splitting up each term and bracket
        bracketList = convertEquation(bracketString)
        
        # form a bracket from this
        bracket = Bracket(genTerms(bracketList[0]))
        
        # display the final answers to the user
        print("-----------------------------")
        print("Expression:\t" + bracket.display())                  # first, display the original expression
        bracket.fullPrepare()
        print("Simplified:\t" + bracket.display())                  # then, display the simplified expression
        print("-----------------------------")

# a function to determine whether the user's input was an expression or equation
def determineType(equationString):
    if "=" in equationString:
        return "Equation"
    elif "=" not in equationString:
        return "Bracket"

# a function to remove whitespace from the user's input
def normalise(equationString):
    return equationString.replace(" ", "")

# a function to convert the user's input to separate terms and brackets
def convertEquation(equationString):
    # create a list of two elements (everything before =, and everything after)
    split = equationString.split("=")
    equation = []
    # if the second element is blank (input was an expression), discard it
    if split[-1] == "":
        split = split[:-1]
    for side in split:
        # split the side into a list of all the characters
        side = list(side)
        differences = [0]
        # while there are still brackets to convert...
        while len(differences) > 0:
            # find where all the bracket pairs are
            bracketsTracker = countBracket(side)
            # if there are no more brackets to convert...
            if bracketsTracker == []:
                differences = []
                convert = True
                while convert == True:
                    convert = False
                    for index, item in enumerate(side):
                        if isinstance(item, list):
                            # only if the list is a bracket...
                            # (lists can be terms)
                            if item[-1] == "bracket":
                                # extract that bracket and flag that the side needs to be formatted
                                side[index] = side[index][0]
                                convert = True
                    # if the side is flagged, format it
                    if convert == True:
                        side = convertBracket(side)
            # if there is at least one pair of brackets...
            else:
                differences = []
                # calculate the range of each pair of brackets
                for index, item in enumerate(bracketsTracker):
                    differences.append(item[1] - item[0])
                
                # find the smallest of the differences
                # the aim is to extract the smallest brackets first, then the larger ones
                targetIndex = min(range(len(differences)), key=differences.__getitem__)
                
                # using the indexes found in countBracket(), convert the bracket into a list
                # tag the list with "bracket" to signify that it is a bracket, not a term
                expandedBracket = [convertBracket(side[bracketsTracker[targetIndex][0]:bracketsTracker[targetIndex][1]-1]), "bracket"]
                
                # replace the brackets in the original list with the converted bracket
                side[bracketsTracker[targetIndex][0]:bracketsTracker[targetIndex][1]-1] = [expandedBracket]
        # once the side is formatted, append it to a list
        equation.append(side)
    # return a list with two sides in it
    # (or one if it's an expression)
    return equation

# a function to collect characters and objects in a bracket, and separate them into terms
def convertBracket(bracketList):
    # if the first item isn't a list and doesn't have a sign, add a plus sign to the start of the bracket
    if (not isinstance(bracketList[0], list)) and (bracketList[0] != "-"):
        bracketList.insert(0, "+")
    
    termList = []
    term = []
    
    # decides if a term is currently being compiled
    finding = False
    
    for index, character in enumerate(list(bracketList)):
        # if the character is a sign, this signifies the start of a term
        if character in ["-", "+"]:
            # if a term is currently being compiled...
            if finding:
                # take what has been compiled, and append it to the termList as a finished term
                termList.append(term)
                # clear the term
                term = []
                # no longer compiling a term
                finding = False
            # if a term is not currently being compiled...
            if not finding:
                # add the sign to the term
                term.append(character)
                # start compiling a term
                finding = True
        # if the character is a list, it needs to be converted to a bracket
        if isinstance(character, list) and finding:
            # remove the "bracket" tag if it's there
            tagCheck = False
            if character[-1] == "bracket":
                tagCheck = True
                character = character[:-1]
            
            # convert each item inside the list to the corresponding object
            toInsert = []
            for item in character:
                generatedTerms = genTerms(item)
                for item in generatedTerms:
                    toInsert.append(item)

            # create a bracket from the list of items, using the current value being compiled as the multiplier
            toAppend = Bracket(toInsert, genTerms(term)[0].value)
            
            # if it was there originally, add the "bracket" tag again
            if tagCheck:
                toAppend = [toAppend]
                toAppend.append("bracket")
            
            termList.append(toAppend)
            # clear the term and start searching again
            term = []
            finding = False
        # if the character is already a Bracket object, append it to the termList
        elif isinstance(character, Bracket):
            termList.append(character)
        # if the character is a letter, number or decimal point, append it to the term being compiled
        elif character.isalnum() or character == ".":
            term.append(character)
    
    # if a term is being compiled and hasn't already been added to the list, add it
    if term != []:
        termList.append(term)
    return termList

# a function to find where the bracket pairs are in a bracket
def countBracket(bracketList):
    bracketTracker = []
    deleted = False
    prev = []
    current = []
    while True:
        if (bracketList.count("(") > 0) or (bracketList.count(")") > 0):
            # get the starting and closing indexes of one pair of brackets
            # for the first time, this will delete the bracket characters
            bracketIndex = countBracketProcess(bracketList, deleted)
            # add this pair of indexes to the tracker
            bracketTracker.append(bracketIndex)
            # after the first pass, stop deleting brackets
            deleted = True
        
        # record the current tracker
        current = bracketTracker
        # if the tracker hasn't changed from the previous pass, no brackets remain; return the list of pairs
        if prev == current:
            return bracketTracker
        # if it has changed, move on to the next pass
        else:
            prev = current

# a function to find the start and end of one pair of brackets
def countBracketProcess(bracketList, deleted):
    foundPair = False
    for index, character in enumerate(bracketList):
        if not foundPair:
            # find where the latest bracket starts
            if character == "(":
                bracketStart = index
            # once this bracket ends, return the indexes of the start and end
            elif character == ")":
                bracketEnd = index
                foundPair = True
                # if it's the first pass, delete these characters
                if not deleted:
                    del bracketList[bracketStart]
                    del bracketList[bracketEnd - 1]
                return [bracketStart, bracketEnd]

# a function to remove the "bracket" tag
def delBracketTag(bracketList):
    for index, item in enumerate(bracketList):
        if item == "bracket":
            del bracketList[index]
        elif isinstance(item, list):
            bracketList[index] = delBracketTag(item)
    return bracketList

# a function to generate Term or Variable objects from lists of characters
def genTerms(equationSide):
    termList = []
    # remove the "bracket" tag if it's there
    equationSide = delBracketTag(equationSide)
    
    for index, item in enumerate(equationSide):
        # if the bracket passed in has nested functions...
        if isinstance(item, list):
            tempIndex = index
            # generate terms for everything inside, and replace the nested function with the generated terms
            generatedTerms = genTerms(item)
            equationSide.pop(index)
            for term in generatedTerms:
                equationSide.insert(tempIndex, term)
                tempIndex +=1
    
    delList = []
    
    for index, item in enumerate(equationSide):
        # if the item is a Term, Variable or Bracket...
        if isinstance(item, (Term, Variable, Bracket)):
            # add it to the term list
            termList.append(equationSide[index])
            
            # add it to the list of items to delete from the original
            delList.append(equationSide[index])
        
    
    for delItem in delList:
        # delete all items needed
        while delItem in equationSide:
            equationSide.remove(delItem)

    # if anything is left, form a term out of it
    if equationSide != []:
        termList.append(genTermsProcess(equationSide))
    return termList
        
# a function to form the objects from characters
def genTermsProcess(termBracket):
    unknown = ""
    # extract the sign from the term
    sign = termBracket.pop(0)
    # if nothing is left (because +1 is written as just +, so removing the sign leaves nothing)...
    if termBracket == []:
        # put a 1 in its place
        termBracket = ["1"]
    # form a string from all the characters in the term
    value = "".join(termBracket)
    
    # remove brackets and decimal points (these count as non-numeric, but we only want to check for unknowns/letters)
    testVal = value
    testVal = testVal.replace("(", "")
    testVal = testVal.replace(")", "")
    testVal = testVal.replace(".", "")
    
    # if there is a letter...
    if not testVal.isnumeric():
        # convert the string back into a list
        value = list(value)
        for index, character in enumerate(value):
            # find the unknown
            if character.isalpha():
                unknown = value.pop(index)
        
        # if nothing is left (because the term was just x, so there isn't a coefficient written)...
        if value == []:
            # put a 1 in its place
            value = ["1"]
        
        # make the value a string again
        value = "".join(value)
        # make the value negative if the sign was -
        if sign == "-":
            value = "-" + value
        
        # return a Variable object, with the unknown letter as the value, and the number value as the multiplier
        return Variable(float(value), unknown)
    # if there isn't a letter
    else:
        # make the value negative if the sign was -
        if sign == "-":
            value = "-" + value
        
        # return a Term object
        return Term(float(value))



# run the whole program
# full()
