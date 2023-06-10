class Stack:
    def __init__(self):
        """
        Initialize the stack's data attributes
        """
        self.stack = []

    def push(self, item):
        """
        Push an item to the stack
        """
        self.stack.append(item)

    def peek(self):
        """
        Return the element at the top of the stack
        Return a string "Error" if the stack is empty
        """
        if self.is_empty():
            return "Error"
        return self.stack[-1]

    def pop(self):
        """
        Pop an item from the stack if non-empty
        """
        if self.is_empty():
            return "Error"
        return self.stack.pop()

    def is_empty(self):
        """
        Return True if the stack is empty, False otherwise
        """
        return len(self.stack) == 0

    def __str__(self):
        """
        Return a string containing elements of the current stack in top-to-bottom order, separated by spaces
        """
        return " ".join(str(item) for item in self.stack[::-1])

    def __len__(self):
        """
        Return the current number of elements in the stack
        """
        return len(self.stack)
