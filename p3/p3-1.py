# prototype 3-1: variables

class Term():
    # each Term has a sign and value
    def __init__(self, sign, value):
        self.sign = sign
        self.value = value

# a class for Bracket objects
class Bracket():
    # each Bracket has a list of the terms, and how much it has been multiplied by (default to 1)
    def __init__(self, termList, multiplier=1):
        self.terms = termList
        self.multiplier = multiplier
    
    # a function to print the equation in a readable format
    def display(self, rec=False):
        # create an empty string for the equation
        output = ""
        multiBracket = isinstance(self, Bracket) and self.multiplier != 1
        if multiBracket:
            output += str(self.multiplier)
            output += "("
        
        if rec and not multiBracket:
            output += "("
             
        for item in self.terms:
            # if the item is a term, append the sign and value
            if isinstance(item, Term):
                output += str(item.sign) + str(item.value)
            elif isinstance(item, Variable):
                if item.multiplier != 1:
                    if item.terms[0].sign == "+":
                        output += "+"
                    else:
                        output += "-"
                    output += str(item.multiplier)
                output += str(item.terms[0].value)
            # if the item is a bracket, display everything inside and wrap it in brackets
            elif isinstance(item, Bracket):
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
            if isinstance(item, Term):
                self.tempVal = item.value
                if item.sign == "-":
                    self.tempVal *= -1
                
                # multiply the temporary number by the multiplier
                self.tempVal *= self.multiplier

                # convert the temporary number back to a Term object
                if self.tempVal >= 0:
                    self.terms[index] = Term("+", self.tempVal)
                elif self.tempVal < 0:
                    self.terms[index] = Term("-", self.tempVal*-1)
            
            elif isinstance(item, (Bracket, Variable)):
                self.terms[index].multiplier *= self.multiplier
        
        # set the multiplier to 1 (expanded bracket)
        self.multiplier = 1
    
    def fullExpand(self):
        self.expand()
        for item in self.terms:
            if isinstance(item, Bracket) and not isinstance(item, Variable):
                item.fullExpand()
    
    def simplify(self, termList):
        # create a counter for the sum
        count = 0
        # add or subtract as needed
        for item in termList:
            if not isinstance(item, Variable):
                # if the item is a list (a bracket with multiple terms), combine those terms first, then use the result
                if isinstance(item, Bracket):
                    item = self.simplify(item.terms)
                if item.sign == "+":
                    count += item.value
                elif item.sign == "-":
                    count -= item.value

        # return a positive or negative term as needed
        if count >= 0:
            return Term("+", count)
        elif count < 0:
            return Term("-", count*-1)

    
    # a function to simplify a bracket as much as possible
    def clean(self):
        index = -1
        # cycle through the bracket
        for item in self.terms:
            index +=1
            if isinstance(item, Bracket) and not isinstance(item, Variable):
                # if the bracket has a single term...
                if len(item.terms) == 1:
                    # expand the brackets, leaving just that term
                    item.expand()
                    self.terms[index] = item.terms[0]
                    
                # if the item is another bracket (multiple terms)...
                else:
                    # collect the terms within this bracket
                    item.expand()
                    self.terms[index] = self.simplify(item.terms)
        
        self.terms = [self.simplify(self.terms)]

# a child class for Variable objects
# variables are a pair of brackets, containing one term (the unknown)
class Variable(Bracket):
    def __init__(self, sign, value, multiplier=1):
        super().__init__([Term(sign, value)], multiplier)
    

equation = Bracket( [Bracket( [Term("+", 76), Variable("-", "x", 2)], 6), Term("+", 5)], 8 )
# equivalent to 8( 6(76 -2x) +5)

print("\n")

print(equation.display())
equation.fullExpand()

print("\n")