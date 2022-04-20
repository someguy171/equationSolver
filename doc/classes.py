# used for making deep copies of objects, so the original isn't affected
import copy

# a class for Term objects
class Term():
    # each Term has a sign and value
    def __init__(self, value):
        self.value = value
        self.id = "Term"

# a class for Bracket objects
class Bracket():
    # each Bracket has a list of the terms, and how much it has been multiplied by (default to 1)
    def __init__(self, termList, multiplier=1):
        self.terms = termList
        self.multiplier = multiplier
        self.id = "Bracket"
    
    # a function to fully expand and simplify a bracket
    def fullPrepare(self):
        self.fullExpand()
        if self.checkVar():
            self.simplifyVar()
        else:
            self.clean()
    
    # a function to print the equation in a readable format
    def display(self, rec=False):
        # create an empty string for the equation
        output = ""
        
        # decide if the bracket has a coefficient to write (any coefficient other than 1)
        multiBracket = (self.id == "Bracket") and (self.multiplier != 1)
        if multiBracket:
            # write "+" if 0 or positive
            if self.multiplier >= 0:
                output += "+"
            # round if possible
            if (self.multiplier - int(self.multiplier)) == 0:
                output += str(int(self.multiplier))
            else:
                output += str(self.multiplier)
            # write the opening bracket
            output += "("
        
        # if the function is run recursively (needs surrounding brackets) and there isn't a coefficient, write the opening bracket
        if rec and not multiBracket:
            output += "("
         
        for item in self.terms:
            # if the item is a term...
            if item.id == "Term":
                # write the sign
                if item.value >= 0:
                    if len(output) == 0:
                        pass
                    elif output[-1] != "(":
                        output += "+"
                # round if possible
                if (item.value - int(item.value)) == 0:
                    output += str(int(item.value))
                else:
                    output += str(item.value)
            # if the item is a variable...
            elif item.id == "Variable":
                if item.multiplier != 1:
                    # write the coefficient
                    if item.multiplier >= 0:
                        if len(output) == 0:
                            pass
                        elif output[-1] != "(":
                            output += "+"
                    # round if possible
                    if (item.multiplier - int(item.multiplier)) == 0:
                        output += str(int(item.multiplier))
                    else:
                        output += str(item.multiplier)
                # write the value (letter)
                output += str(item.terms[0].value)
            # if the item is a bracket, display everything inside and wrap it in brackets
            elif item.id == "Bracket":
                output += item.display(True)
            
            # space to separate terms
            output += " "
        
        # if the output string ends in a space, remove it
        if output[-1] == " ":
            output = output[:-1]
        # if a bracket was being written, write a closing bracket
        if multiBracket or rec:
            output += ")"
        # if the output string starts with a plus sign, remove it
        if output[0] == "+" and not multiBracket:
            output = output[1:]
        return output
    
    # a function to expand the bracket, multiplying each term by the multiplier
    def expand(self):
        index = -1
        # for each item in the bracket...
        for item in self.terms:
            index += 1
            # if the item is a term...
            if item.id == "Term":
                # multiply the term by the bracket's multiplier
                self.terms[index] = Term(item.value*self.multiplier)
            # if the item is a bracket or variable...
            elif item.id in ["Bracket", "Variable"]:
                # multiply its multiplier by the surrounding bracket's multiplier
                self.terms[index].multiplier *= self.multiplier
        
        # set the multiplier to 1 (as the bracket has now been expanded)
        self.multiplier = 1
    
    # a function to expand the bracket, and expand any nested brackets
    def fullExpand(self):
        self.expand()
        for item in self.terms:
            if item.id == "Bracket":
                item.fullExpand()
    
    # a function to collect like terms
    def simplify(self, termList, varSearch=False):
        # determines whether the base term has been found
        foundNum = False
        # determines whether the base variable has been found
        # by default, this function is used for brackets with no variables; it assumes the variable has already been found
        foundVar = not varSearch
        # if the bracket has any nested brackets, simplify those first
        for item in termList:
            if item.id == "Bracket":
                item = item.simplify(item.terms)
        
        # find a "base" term and variable; all other terms and variables will be added to this base
        for item in termList:
            tempList = []
            numIndex = 0
            varIndex = 0
            index = 0
            while foundNum == False or foundVar == False:
                tempList.append(termList[index])
                # if the item is a term, and one hasn't been found yet, mark it as the base
                if tempList[-1].id == "Term" and foundNum == False:
                    termList.pop(index)
                    foundNum = True
                    numIndex = len(tempList) - 1
                    index -= 1
                # if the item is a variable, and one hasn't been found yet, mark it as the base
                if tempList[-1].id == "Variable" and foundVar == False:
                    termList.pop(index)
                    foundVar = True
                    varIndex = len(tempList) - 1
                    index -= 1
                index += 1
            
            # add each term or variable to the respective base
            for item in termList:
                if item.id == "Term":
                    # terms add value
                    tempList[numIndex].value += item.value
                elif item.id == "Variable":
                    # variables add multipliers
                    tempList[varIndex].multiplier += item.multiplier
            
            return tempList

    # a function to simplify brackets with variables
    def simplifyVar(self):
        if self.checkSigns():
            self.terms = self.extract()
            # clean, looking for variables in simplify()
            self.clean(True)
    
    # a function to check for brackets with coefficients other than 1
    def checkSigns(self):
        for item in self.terms:
            if item.id == "Bracket":
                if item.multiplier != 1:
                    return False
        return True
    
    # a function to check if a bracket (or any of its nested brackets) have a variable
    def checkVar(self):
        for item in self.terms:
            if item.id == "Variable":
                return True
            if item.id == "Bracket":
                return item.checkVar()
        return False
    
    # a function to replace brackets with their contents (remove the brackets)
    def extract(self):
        output = []
        for item in self.terms:
            if item.id == "Bracket":
                extracted = item.extract()
                for exItem in extracted:
                    output.append(exItem)
            elif item.id in ["Term", "Variable"]:
                output.append(item)
        return output
    
    # a function to simplify a bracket as much as possible
    def clean(self, varSearch=False):
        index = -1
        for item in self.terms:
            index +=1
            if item.id == "Bracket":
                # if the bracket has a single term...
                if len(item.terms) == 1:
                    # expand the brackets, leaving just that term
                    item.fullExpand()
                    self.terms[index] = item.terms[0]
                # if the item is another bracket (multiple terms)...
                else:
                    # collect the terms within this bracket
                    item.fullExpand()
                    tempIndex = index
                    expandedBracket = item.simplify(item.terms, varSearch)
                    # remove the bracket, and replace it with its contents
                    self.terms.pop(index)
                    for term in expandedBracket:
                        self.terms.insert(tempIndex, term)
                        tempIndex += 1
        # once everything has been extracted from any nested brackets, simplify the bracket
        self.terms = self.simplify(self.terms, varSearch)


# a child class for Variable objects
# variables are a pair of brackets, containing one term (the unknown)
class Variable(Bracket):
    def __init__(self, multiplier, value):
        super().__init__([Term(value)], multiplier)
        self.id = "Variable"

# a class for Equation objects
# Equations have two Bracket objects for left- and right-hand sides
class Equation():
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.id = "Equation"
    
    # a function to prepare both sides of the equation
    def sidesPrepare(self):
        self.lhs.fullPrepare()
        self.rhs.fullPrepare()
    
    # a function to display the equation
    def display(self):
        return self.lhs.display() + " = " + self.rhs.display()
    
    # a function to move all terms, variables and/or brackets from the LHS to the RHS
    def rearrange(self):
        # remove from LHS, and perform the opposite action on RHS
        for item in self.lhs.terms:
            if item.id == "Term":
                self.rhs.terms.append(Term(-item.value))
            elif item.id == "Variable":
                self.rhs.terms.append(Variable(-item.multiplier, item.terms[0].value))
            elif item.id == "Bracket":
                self.rhs.terms.append(Bracket(item.termList, -item.multiplier))
        # once everything has moved over, simplify the RHS
        self.rhs.simplifyVar()
        # LHS = 0
        self.lhs = Bracket([Term(0)])
    
    # a function to solve a rearranged equation
    def solve(self):
        # error margin
        diff = 0.000000001
        
        # amount to multiply bounds by if scope needs to increase
        increase = 10
        
        # initial bounds and midpoint
        lb = -10
        ub = 10
        mid = (lb + ub)/2
        
        # initial answers 
        lb_answer = -1
        ub_answer = -1
        
        # 0 must lie between the answers
        # if both answers are below or over 0...
        while (lb_answer > 0 and ub_answer > 0) or (lb_answer < 0 and ub_answer < 0):
            # increase the scope
            lb *= increase
            ub *= increase
            mid = (lb + ub)/2
            
            # recalculate answers
            rhsCopy = copy.deepcopy(self.rhs)
            lb_answer = self.replaceVar(rhsCopy, lb)
            rhsCopy = copy.deepcopy(self.rhs)
            ub_answer = self.replaceVar(rhsCopy, ub)
        while True:
            # calculate the lower bound answer
            rhsCopy = copy.deepcopy(self.rhs)
            lb_answer = self.replaceVar(rhsCopy, lb)
            
            # calculate the upper bound answer
            rhsCopy = copy.deepcopy(self.rhs)
            ub_answer = self.replaceVar(rhsCopy, ub)
            
            # calculate the midpoint answer
            rhsCopy = copy.deepcopy(self.rhs)
            mid_answer = self.replaceVar(rhsCopy, mid)
            
            # if the difference between answers is more than the error margin, return the midpoint of the bounds
            # (answers are close enough to call the estimate accurate)
            if abs(lb_answer - ub_answer) < diff:
                return mid
            
            # if the answers weren't close enough, adjust bounds accordingly
            if lb_answer < ub_answer:
                if mid_answer > 0:
                    ub = mid
                elif mid_answer < 0:
                    lb = mid
            elif lb_answer > ub_answer:
                if mid_answer > 0:
                    lb = mid
                elif mid_answer < 0:
                    ub = mid
            mid = (lb + ub)/2
    
    # a function to substitute a value into the equation and solve it
    def replaceVar(self, bracket, sub):
        index = 0
        for item in bracket.terms:
            # if the item is a bracket, replace all unknowns within it
            if item.id == "Bracket":
                item.replaceVar(item.terms, sub)
            # if the item is a variable, replace the unknown with the value and multiply it by the variable's coefficient
            elif item.id == "Variable":
                bracket.terms[index] = Term(sub*item.multiplier)
            index += 1
        # having replaced all unknowns, simplify the bracket
        bracket.fullPrepare()
        # return the value of the remaning Term
        return bracket.terms[0].value