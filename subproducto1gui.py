import tkinter as tk
from tkinter import scrolledtext
from lexer_config import is_keyword, is_operator, is_symbol, is_primitive_type

class TokenType:
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    OPERATOR = 'OPERATOR'
    KEYWORD = 'KEYWORD'
    SYMBOL = 'SYMBOL'
    COMMENT = 'COMMENT'
    WHITESPACE = 'WHITESPACE'
    PRIMITIVE_TYPE = 'PRIMITIVE_TYPE'
    UNKNOWN = 'UNKNOWN'

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return f"Token(type={self.type}, value='{self.value}')"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.variables = set()

    def next_token(self):
        while self.pos < len(self.text):
            current_char = self.text[self.pos]

            # Skip whitespace
            if current_char.isspace():
                self.pos += 1
                continue

            # Handle comments (simple case with `//`)
            if current_char == '/' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '/':
                start = self.pos
                while self.pos < len(self.text) and self.text[self.pos] != '\n':
                    self.pos += 1
                return Token(TokenType.COMMENT, self.text[start:self.pos])

            # Handle primitive types and keywords
            if current_char.isalpha() or current_char == '_':
                start = self.pos
                while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
                    self.pos += 1
                identifier = self.text[start:self.pos]
                if is_keyword(identifier):
                    return Token(TokenType.KEYWORD, identifier)
                if is_primitive_type(identifier):
                    return Token(TokenType.PRIMITIVE_TYPE, identifier)
                self.variables.add(identifier)  # Track variables
                return Token(TokenType.IDENTIFIER, identifier)

            # Numbers (integers and real numbers)
            if current_char.isdigit():
                start = self.pos
                while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
                    self.pos += 1
                number = self.text[start:self.pos]
                return Token(TokenType.NUMBER, number)

            # Operators and Symbols
            if current_char in '+-*/%$&|!':
                start = self.pos
                while self.pos < len(self.text) and (self.text[self.pos] in '+-*/%$&|!'):
                    self.pos += 1
                op = self.text[start:self.pos]
                if is_operator(op):
                    return Token(TokenType.OPERATOR, op)
                if is_symbol(op):
                    return Token(TokenType.SYMBOL, op)
                return Token(TokenType.UNKNOWN, op)

            if current_char in '(){};,':
                self.pos += 1
                return Token(TokenType.SYMBOL, current_char)

            # Unknown character
            self.pos += 1
            return Token(TokenType.UNKNOWN, current_char)

        return Token(TokenType.UNKNOWN, '')

class LexerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico")

        # Setup GUI components
        self.setup_widgets()

    def setup_widgets(self):
        # Create Text widgets for input and output
        self.input_text = scrolledtext.ScrolledText(self.root, height=10, width=80)
        self.input_text.pack()

        self.output_text = scrolledtext.ScrolledText(self.root, height=10, width=80)
        self.output_text.pack()

        # Button to start analysis
        self.analyze_button = tk.Button(self.root, text="Analizar", command=self.analyze)
        self.analyze_button.pack()

        # Text widget for variable tracking
        self.variables_text = tk.Text(self.root, height=5, width=80)
        self.variables_text.pack()
        self.variables_text.insert(tk.END, "Variables encontradas:\n")

    def analyze(self):
        # Get text from input
        code = self.input_text.get("1.0", tk.END)
        lexer = Lexer(code)
        
        # Clear previous output
        self.output_text.delete("1.0", tk.END)
        self.variables_text.delete("2.0", tk.END)
        
        token = lexer.next_token()
        while token.type != TokenType.UNKNOWN:
            if token.type != TokenType.COMMENT:
                self.output_text.insert(tk.END, str(token) + '\n')
            token = lexer.next_token()

        # Display tracked variables
        variables = sorted(lexer.variables)
        for var in variables:
            self.variables_text.insert(tk.END, f"{var}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = LexerApp(root)
    root.mainloop()
