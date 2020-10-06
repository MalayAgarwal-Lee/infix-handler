class Stack:
    '''
    Class which implements a stack using a Python list

    Attributes:
        stack: list, the actual data structure where items are stored
    '''

    def __init__(self):
        self.stack = []

    def isempty(self):
        '''
        Function to check whether the stack is empty or not

        Returns:
            Boolean value which is True when the stack is empty
        '''
        return not self.stack

    def makeempty(self):
        '''
        Function to completely empty the stack
        '''
        self.stack = []

    def tos(self):
        '''
        Function to obtain the element at the top of the stack

        Returns:
            The element at the top of the stack

        Raises:
            ValueError when the stack is empty
        '''
        if not self.isempty():
            return self.stack[-1]
        raise ValueError("The stack is empty")

    def push(self, item):
        '''
        Function to add an item to the top of the stack

        Arguments:
            item: any data type, the item that is to be added
        '''
        self.stack.append(item)

    def pop(self):
        '''
        Function to remove the item at the top of the stack

        Returns:
            The item which as removed from the top of the stack

        Raises:
            ValueError when the stack is empty
        '''
        if not self.isempty():
            item = self.stack.pop()
            return item
        raise ValueError("The stack is empty")
