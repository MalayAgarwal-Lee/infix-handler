import re

from expr_parser import parse
from stack import Stack
from operators import OPERATORS, operator_map


class Postfix:
    '''
    Class to represent a postfix expression

    This class is never visible to the user

    Attributes:
        expr: str, the postfix expression
        stack: Stack, a stack for evaluation
        value: numeric, the value obtained by evaluating the expression
    '''

    def __init__(self, expression):
        self.expr = expression
        self.stack = Stack()

        # Use the evaluate() function to update the value of the expression
        self.value = self.evaluate()

    def __repr__(self):
        '''
        Function to pretty-print object as Postfix(expr=<expr>, value=<value>)
        '''
        return f'{self.__class__.__name__}(expr={self.expr}, value={self.value})'

    def __str__(self):
        return self.__repr__()

    def resolve_operator(self, op, exchange=False):
        '''
        Function to evaluate a particular operator
        by popping its two operands from the stack
        and then pushing the result back onto the stack

        Arguments:
            op: str, the operator which needs to be evaluated
            exchange: bool, changes the order of the operands
        '''
        right_opr = self.stack.pop()
        left_opr = self.stack.pop()

        if exchange:
            left_opr, right_opr = right_opr, left_opr

        self.stack.push(operator_map(op, left_opr, right_opr))

    def evaluate(self):
        '''
        Function to evaluate the postfix expression

        Returns:
            The numeric value of the postfix expression
        '''
        for char in self.expr:
            if char not in OPERATORS:
                # Convert character to integer before pushing onto stack
                self.stack.push(int(char))
            else:
                self.resolve_operator(char)
        # In the end, the TOS has the final value
        return self.stack.tos()


class Prefix(Postfix):
    '''
    Class to represent a prefix expression

    Attributes:
        All the attributes of Postfix class
    '''

    def resolve_operator(self, op, exchange=False):
        '''
        Function to evaluate a particular operator
        by popping its two operands from the stack
        and then pushing the result back onto the stack

        Arguments:
            op: str, the operator which needs to be evaluated
            exchange: bool, changes the order of the operands
        '''
        # A prefix expression uses the first pop as left operand
        # And second pop as right operand
        super().resolve_operator(op, exchange=True)

    def evaluate(self):
        '''
        Function to evaluate the prefix expression

        Returns:
            The numeric value of the prefix expression
        '''
        # A prefix expression is evaluated similar to postfix
        # Except starting from the end
        self.expr = self.expr[::-1]
        value = super().evaluate()
        self.expr = self.expr[::-1]
        return value


class Infix:
    '''
    Class to represent an infix expression

    Attributes:
        expr: str, the infix expression
        stack: Stack, a stack for conversions (postfix, prefix)
    '''

    def __init__(self, expression):
        self.expr = expression
        self.tokens = self.parse_expr()
        self.stack = Stack()

    def __repr__(self):
        '''
        Function to pretty-print the object as Infix(expr=<expr>)
        '''
        return f'{self.__class__.__name__}(expr={self.expr})'

    def __str__(self):
        return self.__repr__()

    def parse_expr(self):
        expr = re.sub(r'\( - ((?:\d )+)\)', r'( UMINUS \1)', self.expr)
        parse(expr)

        length, i = len(expr), 0
        tokens = []

        while i < length:
            char = expr[i]

            if char.isspace():
                i += 1
                continue

            if char == 'U':
                end = expr.find(' ', i)
                tokens.append(expr[i:end])
                i = end + 1
            elif char.isdigit():
                end = i + 1
                while expr[end] not in OPERATORS.keys():
                    end += 1
                tokens.append(expr[i:end - 1])
                i = end
            else:
                tokens.append(char)
                i += 1

        return tokens

    def handle_closing_parenthesis(self):
        '''
        Function to add all the elements in the stack
        To the postfix expression until '(' is encountered
        In case of encountering a ')' in the infix expression
        '''
        result = ''
        while not self.stack.isempty() and self.stack.tos() != '(':
            result += self.stack.pop()

        # Pop the '(' because the expression
        # In this bracket has been converted
        self.stack.pop()
        return result

    def handle_operator(self, op):
        '''
        Function to add all higher precedence operators than an operator
        currently in the stack to the postfix expression
        In case the operator is encountered in the infix expression

        Arguments:
            op: str, the operator which is encountered

        Raises:
            KeyError when an unsupported operand is passed
        '''
        result = ''
        while (
            not self.stack.isempty() and
            OPERATORS[op] <= OPERATORS[self.stack.tos()]
        ):
            result += self.stack.pop()

        # Push the encountered operator onto the stack
        self.stack.push(op)
        return result

    def handle_leftovers(self):
        '''
        Function to handle all remaining operators on the stack
        After the infix expression has been scanned completely
        '''
        result = ''
        while not self.stack.isempty():
            result += self.stack.pop()
        return result

    def topostfix(self, expr=None):
        '''
        Function to convert the infix expression to postfix

        Returns:
            A Postfix object representing the postfix expression
        '''
        result = ''

        # Filter out any whitespace
        if expr is None:
            expr = self.expr

        expr = [char for char in expr if not char.isspace()]

        for char in expr:
            if char not in OPERATORS:
                result += char
            elif char == '(':
                self.stack.push(char)
            elif char == ')':
                result += self.handle_closing_parenthesis()
            else:
                result += self.handle_operator(char)

        result += self.handle_leftovers()

        return Postfix(result)

    def reverse_expr(self):
        '''
        Function to correctly reverse an infix expression
        Replacing '(' with ')' and vice-versa
        '''
        result = ''
        for char in self.expr[::-1]:
            if char == '(':
                result += ')'
            elif char == ')':
                result += '('
            else:
                result += char
        return result

    def toprefix(self):
        '''
        Function to convert the infix expression to prefix

        Returns:
            A Prefix object representing the prefix expression
        '''

        # The prefix expression can be obtained by
        # Reversing the infix expression
        # Converting that to postfix
        # And then reversing the postfix expression
        expr = self.reverse_expr()
        postfix = self.topostfix(expr)
        return Prefix(postfix.expr[::-1])
