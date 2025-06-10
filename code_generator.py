import re
from collections import deque

class CodeGenerator:
    def __init__(self):
        self.temp_count = 0
        
        # Operators with their corresponding mnemonics
        self.operators = {
            # Arithmetic operators
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
            '%': 'MOD',
            '//': 'DIV',  # Integer division
            '**': 'POW',  # Exponentiation
            
            # Relational operators
            '<': 'LT',
            '<=': 'LE',
            '>': 'GT',
            '>=': 'GE',
            '==': 'EQ',
            '!=': 'NE',
            
            # Logical operators
            '&&': 'AND',
            '||': 'OR',
            '!': 'NOT'
        }
        
        # Operator precedences (higher number means higher precedence)
        self.precedence = {
            # Arithmetic operators
            '**': 6,  # Highest precedence
            '*': 5,
            '/': 5,
            '%': 5,
            '//': 5,
            '+': 4,
            '-': 4,
            
            # Relational operators
            '<': 3,
            '<=': 3,
            '>': 3,
            '>=': 3,
            '==': 3,
            '!=': 3,
            
            # Logical operators
            '!': 2,
            '&&': 1,
            '||': 1
        }
        
        # Right-associative operators
        self.right_associative = {'**'}
        
        # Valid variable characters
        self.valid_var_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
        
    def get_next_temp(self):
        self.temp_count += 1
        return f't{self.temp_count}'
    
    def validate_expression(self, expression):
        """Validate the arithmetic expression"""
        if not expression:
            return False, "Expression cannot be empty"
            
        # Check for balanced parentheses
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False, "Unbalanced parentheses"
                stack.pop()
        if stack:
            return False, "Unbalanced parentheses"
            
        # Check for valid characters
        valid_chars = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/%//**<>=!() |&\t\n\r')
        if any(char not in valid_chars for char in expression):
            return False, "Invalid characters in expression"
            
        # Check for valid operators
        operators = set(self.operators.keys())
        for op in operators:
            if op in expression:
                if op in ['&&', '||', '!'] and not self._is_valid_logical_use(expression, op):
                    return False, f"Invalid use of logical operator '{op}'"
                if op in ['<', '<=', '>', '>=', '==', '!='] and not self._is_valid_relational_use(expression, op):
                    return False, f"Invalid use of relational operator '{op}'"
        
        return True, ""
    
    def _is_valid_logical_use(self, expression, op):
        """Check if logical operator is used correctly"""
        pattern = r'\b' + re.escape(op) + r'\b'
        matches = re.finditer(pattern, expression)
        for match in matches:
            start = match.start()
            end = match.end()
            if start > 0 and end < len(expression):
                before = expression[start-1]
                after = expression[end]
                
                # Check if operator is not between numbers
                if (before.isdigit() or before == ')') and (after.isdigit() or after == '('):
                    return False
                    
                # Check if operator is not between operators
                if before in self.operators and after in self.operators:
                    return False
                    
                # Check if operator is not at start or end
                if start == 0 or end == len(expression):
                    return False
        return True
    
    def _is_valid_relational_use(self, expression, op):
        """Check if relational operator is used correctly"""
        pattern = re.escape(op)
        matches = re.finditer(pattern, expression)
        for match in matches:
            start = match.start()
            end = match.end()
            if start > 0 and end < len(expression):
                before = expression[start-1]
                after = expression[end]
                
                # Check if operator is not between numbers
                if (before.isdigit() or before == ')') and (after.isdigit() or after == '('):
                    return False
                    
                # Check if operator is not between operators
                if before in self.operators and after in self.operators:
                    return False
                    
                # Check if operator is not at start or end
                if start == 0 or end == len(expression):
                    return False
        return True
    
    def tokenize(self, expression):
        """Tokenize the expression"""
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
                
            # Handle multi-character operators
            if i < len(expression) - 1:
                next_char = expression[i+1]
                two_char_op = char + next_char
                if two_char_op in self.operators:
                    tokens.append(two_char_op)
                    i += 2
                    continue
                    
            # Handle single character operators
            if char in self.operators:
                tokens.append(char)
                i += 1
                continue
                
            # Handle numbers
            if char.isdigit():
                num = char
                while i + 1 < len(expression) and expression[i+1].isdigit():
                    i += 1
                    num += expression[i]
                tokens.append(num)
                i += 1
                continue
                
            # Handle variables
            if char.isalpha() or char == '_':
                var = char
                while i + 1 < len(expression) and (expression[i+1].isalnum() or expression[i+1] == '_'):
                    i += 1
                    var += expression[i]
                tokens.append(var)
                i += 1
                continue
                
            # Handle parentheses
            if char in '()':
                tokens.append(char)
                i += 1
                continue
                
            raise ValueError(f"Invalid character: {char}")
        
        return tokens
    
    def shunting_yard(self, tokens):
        """Convert infix to postfix using Shunting Yard algorithm"""
        output = []
        operator_stack = []
        
        for token in tokens:
            if token.isnumeric():
                output.append(token)
            elif token in self.operators:
                while (operator_stack and 
                       operator_stack[-1] in self.operators and 
                       ((token not in self.right_associative and 
                         self.precedence[operator_stack[-1]] >= self.precedence[token]) or
                        (token in self.right_associative and 
                         self.precedence[operator_stack[-1]] > self.precedence[token]))):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    if not operator_stack:
                        raise ValueError("Mismatched parentheses")
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Remove the '('
            else:
                output.append(token)
        
        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())
        
        return output
    
    def generate_three_address_code(self, expression):
        """Generate three-address code from expression"""
        try:
            # Validate expression
            is_valid, error = self.validate_expression(expression)
            if not is_valid:
                return [f"Error: {error}"]
                
            # Tokenize
            tokens = self.tokenize(expression)
            
            # Convert to postfix
            postfix = self.shunting_yard(tokens)
            
            # Generate three-address code
            stack = []
            code = []
            temp_count = 0
            
            for token in postfix:
                if token.isnumeric():
                    stack.append(token)
                elif token in self.operators:
                    if len(stack) < 2:
                        return [f"Error: Not enough operands for operator {token}"]
                        
                    op2 = stack.pop()
                    op1 = stack.pop()
                    
                    # Create temporary variable
                    temp = f't{temp_count}'
                    temp_count += 1
                    
                    # Generate code line
                    code.append(f"{temp} = {op1} {self.operators[token]} {op2}")
                    
                    # Push result back to stack
                    stack.append(temp)
                else:
                    stack.append(token)
            
            if len(stack) != 1:
                return ["Error: Invalid expression - multiple values left in stack"]
                
            return code
            
        except Exception as e:
            return [f"Error: {str(e)}"]
    
    def generate_postfix_notation(self, expression):
        """Generate postfix notation from expression"""
        try:
            # Validate expression
            is_valid, error = self.validate_expression(expression)
            if not is_valid:
                return [f"Error: {error}"]
                
            # Tokenize
            tokens = self.tokenize(expression)
            
            # Convert to postfix
            postfix = self.shunting_yard(tokens)
            
            return postfix
            
        except Exception as e:
            return [f"Error: {str(e)}"]
    
    def generate_translation_steps(self, expression):
        """Generate detailed translation steps"""
        try:
            steps = []
            
            # Step 1: Input Expression
            steps.append("Step 1: Input Expression")
            steps.append("----------------------")
            steps.append(f"Expression: {expression}")
            
            # Step 2: Tokenization
            steps.append("\nStep 2: Tokenization")
            steps.append("-------------------")
            tokens = self.tokenize(expression)
            steps.append(f"Tokens: {' '.join(tokens)}")
            
            # Step 3: Operator Precedence Analysis
            steps.append("\nStep 3: Operator Precedence Analysis")
            steps.append("-----------------------------------")
            for token in tokens:
                if token in self.operators:
                    steps.append(f"{token} (Precedence: {self.precedence[token]})")
                else:
                    steps.append(token)
            
            # Step 4: Postfix Conversion
            steps.append("\nStep 4: Postfix Notation")
            steps.append("-----------------------")
            postfix = self.shunting_yard(tokens)
            steps.append(f"Postfix: {' '.join(postfix)}")
            
            # Step 5: Three-Address Code Generation
            steps.append("\nStep 5: Three-Address Code")
            steps.append("-------------------------")
            code = self.generate_three_address_code(expression)
            steps.extend(code)
            
            return steps
            
        except Exception as e:
            return [f"Error: {str(e)}"]
