# prototype 2-1: bracket class

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
                

equation = Bracket( [Bracket( [Term("+", 1), Term("+", 1)], 1 ), Bracket( [Term("+", 3)], 1) ], 1 )
# equivalent to ( (1 + 2) + 3 )

testMulti = Bracket([Term("+", 6)], 7)
# equivalent to 7(6)

testMulti.expand()
print(testMulti.terms[0].value)