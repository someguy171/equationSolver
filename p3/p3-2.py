# prototype 3-2: rearranging equations
# also changed term format

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
    
    # a function to print the equation in a readable format
    def display(self, rec=False):
        # create an empty string for the equation
        output = ""
        multiBracket = self.id == "Bracket" and self.multiplier != 1
        if multiBracket:
            output += str(self.multiplier)
            output += "("
        
        if rec and not multiBracket:
            output += "("
             
        for item in self.terms:
            # if the item is a term, append the sign and value
            if item.id == "Term":
                if item.value >= 0:
                    output += "+"
                output += str(item.value)
            elif item.id == "Variable":
                if item.multiplier != 1:
                    if item.multiplier >= 0:
                        output += "+"
                    output += str(item.multiplier)
                output += str(item.terms[0].value)
            # if the item is a bracket, display everything inside and wrap it in brackets
            elif item.id == "Bracket":
                output += item.display(True)
        
        if multiBracket or rec:
            output += ")"
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
        self.lhs = Bracket([Term(0)])


lhsInput = Bracket( [Bracket( [Term(76), Variable(-2, "x")], 6), Term(5)], 8 )
# equivalent to 8( 6(76 -2x) +5)

rhsInput = Bracket( [Bracket( [Term(68), Variable(-6, "x")], 4)], 10)
# equivalent to 10(4(68 -6x))

lhsInput.fullExpand()
print(lhsInput.display())
lhsInput.simplifyVar()
print(lhsInput.display())

print("\n")

rhsInput.fullExpand()
print(rhsInput.display())
rhsInput.simplifyVar()
print(rhsInput.display())
      
print("\n")

eq1 = Equation(lhsInput, rhsInput)
eq1.display()
eq1.rearrange()
eq1.rhs.simplifyVar()
eq1.display()