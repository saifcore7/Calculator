from simple_calculator import SimpleCalculator
from stack import Stack


class AdvancedCalculator(SimpleCalculator):
    def __init__(self):
        """
        Call super().__init__()
        Instantiate any additional data attributes
        """
        super().__init__()

    def evaluate_expression(self, input_expression):
        """
        Evaluate the input expression and return the output as a float
        Return a string "Error" if the expression is invalid
        """
        list_tokens = self.tokenize(input_expression)
        if not self.check_brackets(list_tokens):
            self.history.insert(0, (input_expression, "Error"))
            return "Error"

        result = self.evaluate_list_tokens(list_tokens)
        if result == "Error":
            self.history.insert(0, (input_expression, "Error"))
            return "Error"

        self.history.insert(0, (input_expression, result))
        return result

    def tokenize(self, input_expression):
        """
        Convert the input string expression to tokens, and return this list
        Each token is either an integer operand or a character operator or bracket
        """
        tokens = []
        current_token = ""
        for char in input_expression:
            if char == " ":
                continue
            elif char.isdigit():
                current_token += char
            elif char in ("+", "-", "*", "/", "(", ")"):
                if current_token:
                    tokens.append(int(current_token))
                    current_token = ""
                tokens.append(char)
            elif char in ("{", "}"):
                if current_token:
                    tokens.append(int(current_token))
                    current_token = ""
                tokens.append("(" if char == "{" else ")")
        if current_token:
            tokens.append(int(current_token))
        return tokens

    def check_brackets(self, list_tokens):
        """
        Check if brackets are valid, that is, all open brackets are closed by the same type
        of brackets. Also, () contains only () brackets.
        Return True if brackets are valid, False otherwise
        """
        stack = Stack()
        for token in list_tokens:
            if token in ("(", "{"):
                stack.push(token)
            elif token in (")", "}"):
                if stack.is_empty():
                    return False  # Unmatched closing bracket
                opening_bracket = stack.pop()
                if (token == ")" and opening_bracket != "(") or (token == "}" and opening_bracket != "{"):
                    return False  # Mismatched brackets
        return stack.is_empty()

    def evaluate_list_tokens(self, list_tokens):
        """
        Evaluate the expression passed as a list of tokens
        Return the final answer as a float, and "Error" in case of division by zero and other errors
        """
        operator_stack = Stack()
        operand_stack = Stack()

        for token in list_tokens:
            if isinstance(token, int):
                operand_stack.push(float(token))
            elif token in ("+", "-", "*", "/"):
                while (
                    not operator_stack.is_empty()
                    and operator_stack.peek() != "("
                    and self.has_precedence(operator_stack.peek(), token)
                ):
                    result = self.apply_operator(
                        operator_stack.pop(), operand_stack.pop(), operand_stack.pop())
                    if result == "Error":
                        return "Error"
                    operand_stack.push(float(result))
                operator_stack.push(token)
            elif token in ("(", "{"):
                operator_stack.push(token)
            elif token in (")", "}"):
                while not operator_stack.is_empty() and operator_stack.peek() not in ("(", "{"):
                    result = self.apply_operator(
                        operator_stack.pop(), operand_stack.pop(), operand_stack.pop())
                    if result == "Error":
                        return "Error"
                    operand_stack.push(float(result))
                if not operator_stack.is_empty() and operator_stack.peek() in ("(", "{"):
                    opening_bracket = operator_stack.pop()
                    if opening_bracket == "{" and token == "}":
                        continue
                    elif opening_bracket == "(" and token == ")":
                        continue
                    else:
                        return "Error"  # Mismatched Brackets

        while not operator_stack.is_empty():
            result = self.apply_operator(
                operator_stack.pop(), operand_stack.pop(), operand_stack.pop())
            if result == "Error":
                return "Error"
            operand_stack.push(float(result))

        return operand_stack.pop()

    def has_precedence(self, op1, op2):
        """
        Check if op1 has higher or equal precedence to op2
        """
        return self.get_precedence(op1) >= self.get_precedence(op2)

    def get_precedence(self, operator):
        """
        Get the precedence value of an operator
        """
        if operator in ("+", "-"):
            return 1
        elif operator in ("*", "/"):
            return 2
        else:
            return 0

    def get_matching_bracket(self, bracket):
        """
        Get the matching closing bracket for the given opening bracket
        """
        if bracket == "(":
            return ")"
        elif bracket == "{":
            return "}"

    def apply_operator(self, operator, operand2, operand1):
        """
        Apply the given operator to the operands and return the result
        """
        try:
            if operator == "+":
                return operand1 + operand2
            elif operator == "-":
                return operand1 - operand2
            elif operator == "*":
                return operand1 * operand2
            elif operator == "/":
                if operand2 == 0:
                    return "Error"  # Division by zero
                return operand1 / operand2
        except Exception:
            return "Error"  # Handle other errors

    def get_history(self):
        """
        Return history of expressions evaluated as a list of (expression, output) tuples
        The order is such that the most recently evaluated expression appears first
        """
        return self.history
