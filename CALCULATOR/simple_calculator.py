from stack import Stack


class SimpleCalculator:
    def __init__(self):
        """
        Instantiate any data attributes
        """
        self.history = []

    def evaluate_expression(self, input_expression):
        """
        Evaluate the input expression and return the output as a float
        Return a string "Error" if the expression is invalid
        """
        if self.is_valid_expression(input_expression):
            # Remove spaces from the expression
            expression = input_expression.replace(" ", "")
            operator = None
            operands = []
            for char in expression:
                if char.isdigit():
                    operands.append(int(char))
                elif char in ("+", "-", "*", "/"):
                    if operator is not None:
                        # Add the expression and error to history
                        self.history.insert(0, (input_expression, "Error"))
                        return "Error"  # More than one operator found
                    operator = char
                else:
                    # Add the expression and error to history
                    self.history.insert(0, (input_expression, "Error"))
                    return "Error"  # Invalid character found

            if len(operands) != 2 or operator is None:
                # Add the expression and error to history
                self.history.insert(0, (input_expression, "Error"))
                return "Error"  # Invalid number of operands or operator not found

            if operator == "+":
                result = operands[0] + operands[1]
            elif operator == "-":
                result = operands[0] - operands[1]
            elif operator == "*":
                result = operands[0] * operands[1]
            else:  # operator == "/"
                if operands[1] == 0:
                    # Add the expression and error to history
                    self.history.insert(0, (input_expression, "Error"))
                    return "Error"  # Division by zero
                result = operands[0] / operands[1]

            # Add the expression and result to history
            self.history.insert(0, (input_expression, float(result)))
            return float(result)

        # Add the expression and error to history
        self.history.insert(0, (input_expression, "Error"))
        return "Error"  # Invalid expression

    def is_valid_expression(self, expression):
        """
        Check if the expression is valid
        """
        valid_operators = ("+", "-", "*", "/")
        valid_chars = valid_operators + \
            (" ",) + tuple(map(str, range(10)))  # Valid characters

        for char in expression:
            if char not in valid_chars:
                return False

        if expression.count("+") + expression.count("-") + expression.count("*") + expression.count("/") != 1:
            return False  # Invalid number of operators

        return True

    def get_history(self):
        """
        Return history of expressions evaluated as a list of (expression, output) tuples
        The order is such that the most recently evaluated expression appears first
        """
        return self.history.copy()
