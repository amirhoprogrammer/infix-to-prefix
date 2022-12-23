from structures.stack import Stack

class Converter:
    precedence1 = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    def preHasPrecedent(self, opator1: str, opator2: str):
        if opator2 == "(":
            return True
        if(opator1=="^" and opator2=="^"):
            return False
        return (self.precedence1[opator1] <= self.precedence1[opator2])
    def postHasPrecedent(self, operator1: str, operator2: str):
        if operator2 == "(":
            return True
        if(operator1=="^" and operator2=="^"):
            return True
        return (self.precedence1[operator1] > self.precedence1[operator2])

    def reverse(self, string: str) -> str:
        ser = ""
        for cap in reversed(string):
            if cap == "(":
                ser += ")"
            elif cap == ")":
                ser += "("
            else:
                ser += cap
        return ser


    def infix_to_postfix(self, infix):
        postfix = ""
        stack = Stack()
        for c1 in infix:
            if(c1.isalnum()):
                postfix += c1
            elif c1 == "(":
                stack.push(c1)
            elif c1 == ")":
                while True:
                    operator = stack.pop()
                    if operator == "(":
                        break
                    else:
                        postfix += operator
            else:
                while((not stack.isEmpty()) and (not self.postHasPrecedent(c1, stack.getTop()))):
                    postfix += stack.pop()
                stack.push(c1)
        while(not stack.isEmpty()):
            postfix += stack.pop()
        return postfix


    def infix_to_prefix(self, infix):
        # prefix = self.reverse(infix)
        # prefix = self.infix_to_postfix(prefix)
        # prefix = self.reverse(prefix)
        operators = Stack()
        operands = Stack()
        for c2 in infix:
            if c2 == "(":
                operators.push(c2)
            elif c2 == ")":
                while (not operators.isEmpty() and (operators.getTop()!="(")):
                    operand1 = operands.pop()
                    operand2 = operands.pop()
                    operator = operators.pop()
                    operands.push(operator+operand2+operand1)
                operators.pop() # removing "("
            elif c2.isalnum():
                operands.push(c2)
            else:
                while (not operators.isEmpty() and self.preHasPrecedent(c2, operators.getTop()) and (operators.getTop()!="(")):
                    operand1 = operands.pop()
                    operand2 = operands.pop()
                    operator = operators.pop()
                    operands.push(operator+operand2+operand1)
                operators.push(c2)
        while not operators.isEmpty():
            operand1 = operands.pop()
            operand2 = operands.pop()
            operator = operators.pop()
            operands.push(operator+operand2+operand1)
        return operands.pop()

    def postfix_to_infix(self, postfix: str) -> str:
        stack = Stack()
        for c3 in postfix:
            if c3.isalnum():
                stack.push(c3)
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()
                stack.push("("+operand1+c3+operand2+")")
        return stack.pop()
    def postfix_to_prefix(self, postfix: str) -> str:
        stack = Stack()
        for c4 in postfix:
            if c4.isalnum():
                stack.push(c4)
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()
                stack.push(c4+operand1+operand2)
        return stack.pop()

    def prefix_to_infix(self, prefix: str) -> str:
        infix = self.reverse(prefix)
        infix = self.postfix_to_infix(infix)
        infix = self.reverse(infix)
        return infix

    def prefix_to_postfix(self, prefix: str) -> str:
        stack = Stack()
        prefix = self.reverse(prefix)
        for c5 in prefix:
            # if c is an operand
            if(c5.isalnum()):
                stack.push(c5)
            else:
                operand1 = stack.pop()
                operand2 = stack.pop()
                stack.push(operand1+operand2+c5)
        return stack.pop()


'''
abcd^e-fgh*+^*+i-
-+a*b^-^cde+f*ghi
a+b*(c^d-e)^(f+g*h)-i
'''