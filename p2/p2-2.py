# prototype 2-2: adapting p1-2, using the bracket class

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
    
    # a function to expand the bracket, multiplying each term by the multiplier
    def expand(self):
        index = -1
        # for each Term object in the bracket, extract the sign and value to form a temporary number
        for term in self.terms:
            index += 1
            self.tempVal = term.value
            if term.sign == "-":
                self.tempVal * -1
            
            # multiply the temporary number by the multiplier
            self.tempVal *= self.multiplier

            # convert the temporary number back to a Term object
            if self.tempVal >= 0:
                self.terms[index] = Term("+", self.tempVal)
            elif self.tempVal < 0:
                self.terms[index] = Term("-", self.tempVal*-1)
        
        # set the multiplier to 1 (expanded bracket)
        self.multiplier = 1
    
    def simplify(self, termList):
        # create a counter for the sum
        count = 0
        # add or subtract as needed
        for term in termList:
            # if the item is a list (a bracket with multiple terms), combine those terms first, then use the result
            if isinstance(term, Bracket):
                term = self.simplify(term.terms)
            if term.sign == "+":
                count += term.value
            elif term.sign == "-":
                count -= term.value

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
                    # remove the brackets, leaving just that term
                    self.terms[index] = item.terms[0]
                    
                # if the item is another bracket (multiple terms)...
                else:
                    # collect the terms within this bracket
                    self.terms[index] = self.simplify(item.terms)
        
        self.terms = self.simplify(self.terms)
    

equation = Bracket( [Bracket( [Bracket( [Term("+", 1), Term("+", 1)], 1 ), Term("-", 10)], 1), Term("-", 98)], 1)
# equivalent to ( ( (1 +1) -10 ) -98 )

equation.clean()
print(equation.terms.sign, equation.terms.value)