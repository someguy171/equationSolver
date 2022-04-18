# prototype 1-1: collecting like terms

# a class for Term objects
class Term():
    # each Term has a sign and value
    def __init__(self, sign, value):
        self.sign = sign
        self.value = value

# a function to collect like terms within a set of brackets
def combineTerms(termList):
    # create a counter for the sum
    count = 0
    # add or subtract as needed
    for term in termList:
        if term.sign == "+":
            count += term.value
        elif term.sign == "-":
            count -= term.value
    
    # return a positive or negative term as needed
    if count >= 0:
        return Term("+", count)
    elif count < 0:
        return Term("-", count*-1)
            
# a function to simplify a side of the equation as much as possible
def cleanSide(inputSide):
    index = -1
    # cycle through the side of the equation
    for item in inputSide:
        index +=1
        # if the item is a single term...
        if len(item) == 1:
            # remove the brackets, leaving just that term
            inputSide[index] = item[0]
            
        # if the item is another bracket (multiple terms)...
        else:
            # collect the terms within this bracket
            inputSide[index] = combineTerms(item)
    
    # combine the terms of the final side
    finalSide = combineTerms(inputSide)
    
    return finalSide
            
            

# side of the equation, where each terms has been wrapped with brackets
inputSide = [[Term("+", 67)], [Term("+", 54)], [Term("-", 98)]]
# equivalent to (67 + 54 - 98)

# the goal is to create a version of this side with as few brackets as possible
finalSide = cleanSide(inputSide)

print(finalSide.sign, finalSide.value)