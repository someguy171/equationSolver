# prototype 3-3: solving for variables

import copy


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
    
    def fullPrepare(self):
        self.fullExpand()
        self.clean()
    
    
    def fullPrepareVar(self):
        self.fullExpand()
        self.simplifyVar()
    
    
    # a function to print the equation in a readable format
    def display(self, rec=False):
        # create an empty string for the equation
        output = ""
        multiBracket = (self.id == "Bracket") and (self.multiplier != 1)
        if multiBracket:
            if self.multiplier >= 0:
                output += "+"
            if (self.multiplier - int(self.multiplier)) == 0:
                output += str(int(self.multiplier))
            else:
                output += str(self.multiplier)
            output += "("
        
        if rec and not multiBracket:
            output += "("
             
        for item in self.terms:
            # if the item is a term, append the sign and value
            if item.id == "Term":
                if item.value >= 0:
                    if len(output) == 0:
                        pass
                    elif output[-1] != "(":
                        output += "+"
                if (item.value - int(item.value)) == 0:
                    output += str(int(item.value))
                else:
                    output += str(item.value)
            elif item.id == "Variable":
                if item.multiplier != 1:
                    if item.multiplier >= 0:
                        if len(output) == 0:
                            pass
                        elif output[-1] != "(":
                            output += "+"
                    if (item.multiplier - int(item.multiplier)) == 0:
                        output += str(int(item.multiplier))
                    else:
                        output += str(item.multiplier)
                output += str(item.terms[0].value)
            # if the item is a bracket, display everything inside and wrap it in brackets
            elif item.id == "Bracket":
                output += item.display(True)
            
            output += " "
        
        if output[-1] == " ":
            output = output[:-1]
        if multiBracket or rec:
            output += ")"
        if output[0] == "+" and not multiBracket:
            output = output[1:]
        return output
    
    # a function to expand the bracket, multiplying each term by the multiplier
    def expand(self):
        index = -1
        # for each Term object in the bracket, extract the sign and value to form a temporary number
        for item in self.terms:
            index += 1
            if item.id == "Term":
                # multiply the term by the multiplier
                self.terms[index] = Term(item.value*self.multiplier)
            elif item.id in ["Bracket", "Variable"]:
                self.terms[index].multiplier *= self.multiplier
        
        # set the multiplier to 1 (expanded bracket)
        self.multiplier = 1
    
    def fullExpand(self):
        self.expand()
        for item in self.terms:
            if item.id == "Bracket":
                item.fullExpand()
    
    def simplify(self, termList, varSearch=False):
        foundNum = False
        foundVar = not varSearch
        for item in termList:
            if item.id == "Bracket":
                item.simplify()
        
        for item in termList:
            tempList = []
            numIndex = 0
            varIndex = 0
            index = 0
            while foundNum == False or foundVar == False:
                tempList.append(termList[index])
                if tempList[-1].id == "Term" and foundNum == False:
                    termList.pop(index)
                    foundNum = True
                    numIndex = len(tempList) - 1
                    index -= 1
                if tempList[-1].id == "Variable" and foundVar == False:
                    termList.pop(index)
                    foundVar = True
                    varIndex = len(tempList) - 1
                    index -= 1
                index += 1
            
            for item in termList:
                if item.id == "Term":
                    tempList[numIndex].value += item.value
                elif item.id == "Variable":
                    tempList[varIndex].multiplier += item.multiplier
            
            return tempList


    def simplifyVar(self):
        if self.checkSigns():
            self.terms = self.extract()
            self.clean(True)
    
    def checkSigns(self):
        for item in self.terms:
            if item.id == "Bracket":
                if item.multiplier != 1:
                    return False
        return True
    
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
        # cycle through the bracket
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
                    self.terms.extend(index-1, item.simplify(item.terms, varSearch))
        
        self.terms = self.simplify(self.terms, varSearch)


# a child class for Variable objects
# variables are a pair of brackets, containing one term (the unknown)
class Variable(Bracket):
    def __init__(self, multiplier, value):
        super().__init__([Term(value)], multiplier)
        self.id = "Variable"


class Equation():
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.id = "Equation"
    
    def sidesPrepare(self):
        self.lhs.fullPrepareVar()
        self.rhs.fullPrepareVar()
        
    def display(self):
        print(self.lhs.display() + " = " + self.rhs.display())
    
    def rearrange(self):
        for item in self.lhs.terms:
            if item.id == "Term":
                self.rhs.terms.append(Term(-item.value))
            elif item.id == "Variable":
                self.rhs.terms.append(Variable(-item.multiplier, item.terms[0].value))
            elif item.id == "Bracket":
                self.rhs.terms.append(Bracket(item.termList, -item.multiplier))
        self.rhs.simplifyVar()
        self.lhs = Bracket([Term(0)])
    
    def solve(self):
        diff = 0.000000001
        increase = 10
        lb = -100
        ub = 100
        mid = (lb + ub)/2
        answer1 = 0
        answer2 = 0.1
        while True:
            rhsCopy = copy.deepcopy(self.rhs)
            lb_answer = self.replaceVar(rhsCopy, lb) #13432
            rhsCopy = copy.deepcopy(self.rhs)
            ub_answer = self.replaceVar(rhsCopy, ub) #-15368
            if (lb_answer > 0 and ub_answer > 0) or (lb_answer < 0 and ub_answer < 0):
                lb *= increase
                ub *= increase
                mid = (lb + ub)/2
            else:
                print("pass")
                rhsCopy = copy.deepcopy(self.rhs)
                mid_answer = self.replaceVar(rhsCopy, mid) #-968
                
                print(abs(lb_answer - ub_answer))
                if abs(lb_answer - ub_answer) < diff:
                    return mid
                
                if lb_answer < 0 < ub_answer:
                    if mid_answer > 0:
                        lb = mid
                    elif mid_answer < 0:
                        ub = mid
                elif lb_answer > 0 > ub_answer:
                    if mid_answer > 0:
                        lb = mid
                    elif mid_answer < 0:
                        ub = mid
                mid = (lb + ub)/2
                print(f"lb: {lb}, mid: {mid}, ub: {ub}")
    
    def adjustBounds(self, lb, mid, ub, answer, increase):
        if lb < answer < mid:
            return [lb, (lb + mid)/2, mid]
        elif mid < answer < ub:
            return [mid, (mid + ub)/2, ub]
        elif answer < lb or answer > ub:
            return [lb*increase, (lb*increase + ub*increase)/2, ub*increase]
            
    
    def replaceVar(self, bracket, sub):
        index = 0
        for item in bracket.terms:
            if item.id == "Bracket":
                item.replaceVar(item.terms, sub)
            elif item.id == "Variable":
                bracket.terms[index] = Term(sub*item.multiplier)
            index += 1
        print(bracket.display())
        bracket.fullPrepare()
        print("value = " + str(bracket.terms[0].value))
        print("")
        return bracket.terms[0].value