class Term:
    def __init__(self, value, sign):
        """Create a new Term object.

        Args:
            value (int): The value of the term.
            sign (string): The sign of the term.
        """
        self.value = value
        self.sign = sign
    
    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value
    
    def getSign(self):
        return self.sign

    def setSign(self, sign):
        self.sign = sign
    
    def collect(self, termList):
        
        for item in termList:
            if item.sign == "+":
                self.value += item.value
            elif item.sign == "-":
                self.value -= item.value
            


class Variable(Term):
    def __init__(self, sign):
        super().__init__(0, sign)


def makeEq():
    print("+1")
    print("-2")
    print("=")
    print("x")
    
    eqInput = []
    
    ended = False
    while not ended:
        current = input("enter: ")
        if current != "0":
            eqInput.append(current)
        else:
            ended = True
    
    print(eqInput)
    return eqInput

def genObj(eqInput):
    eq = []
    
    for item in eqInput:
        if item == "+1":
            eq.append(Term(1, "+"))
        elif item == "-2":
            eq.append(Term(2, "-"))
        elif item == "=":
            eq.append("=")
        elif item == "x":
            eq.append(Variable("+"))
    
    print(eq)
    return eq

def splitEq(eq):
    lhs = []
    rhs = []
    
    current = "lhs"
    for item in eq:
        if item == "=":
            current = "rhs"
        elif current == "lhs":
            lhs.append(item)
        elif current == "rhs":
            rhs.append(item)
    
    print("lhs: ", lhs)
    print("rhs: ", rhs)
    return [lhs, rhs]

def simplify(hs):
    add = []
    for item in hs:
        if item.sign == "+" or item.sign == "-":
            add.append(item)
    
    
            

eqInput = makeEq()
eq = genObj(eqInput)
eqSplit = splitEq(eq)

"""
1 + x = -2

check for x or /
if not:
    check for + or minus
    simplify
"""    