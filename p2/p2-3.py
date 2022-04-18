# prototype 2-3: bracket examples

# a class for Term objects
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
                    
            elif isinstance(item, Bracket):
                self.terms[index].multiplier *= self.multiplier
        
        # set the multiplier to 1 (expanded bracket)
        self.multiplier = 1
    
    def fullExpand(self):
        self.expand()
        for item in self.terms:
            if isinstance(item, Bracket):
                item.fullExpand()
    
    def simplify(self, termList):
        # create a counter for the sum
        count = 0
        # add or subtract as needed
        for item in termList:
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
            if isinstance(item, Bracket):
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
    

equation1 = Bracket( [Bracket( [Bracket( [Term("+", 1), Term("+", 1)], 1 ), Term("-", 10)], 1), Term("-", 98)], 1)
# equivalent to ( ( (1 +1) -10 ) -98 )

equation2 = Bracket( [Bracket( [Term("+", 1), Term("-", 1)], 1), Term("+", 54)], 1)
# equivalent to ( (1 -1) +54)

equation3 = Bracket( [Bracket( [Term("+", 76), Term("-", 5)], 6), Term("+", 5)], 8 )
# equivalent to 8( 6(76 -5) +5)

equation4 = Bracket( [Bracket( [Term("+", 0.6), Term("-", 0.2353)], 0.289), Term("+", 0.24)], 2.05 )
# equivalent to 2.05( 0.289(0.6 -0.2353) +0.24)

equation1.clean()
print(equation1.terms[0].sign, equation1.terms[0].value)

print("\n\n")

equation2.clean()
print(equation2.terms[0].sign, equation2.terms[0].value)

print("\n\n")

print(equation3.display())
equation3.fullExpand()
print(equation3.display())
equation3.clean()
print(equation3.terms[0].sign, equation3.terms[0].value)

print("\n\n")

print(equation4.display())
equation4.fullExpand()
print(equation4.display())
equation4.clean()
print(equation4.terms[0].sign, equation4.terms[0].value)