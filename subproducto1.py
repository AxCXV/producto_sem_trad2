import tkinter as tk
from tkinter import scrolledtext

# Definición de tipos de token en español
class TokenType:
    IDENTIFIER = 'IDENTIFICADOR'  # Representa un identificador (como nombres de variables)
    NUMBER = 'NÚMERO'              # Representa un número (entero o decimal)
    OPERATOR = 'OPERADOR'          # Representa operadores (como +, -, *, /)
    KEYWORD = 'PALABRA_CLAVE'      # Representa palabras clave del lenguaje (como int, if, return)
    SYMBOL = 'SÍMBOLO'             # Representa símbolos (como (, ), {, }, ;, ,)
    COMMENT = 'COMENTARIO'         # Representa comentarios (como // comentario)
    WHITESPACE = 'ESPACIO_EN_BLANCO' # Representa espacios, tabulaciones y saltos de línea
    UNKNOWN = 'DESCONOCIDO'        # Representa caracteres desconocidos o no reconocidos

# Clase para representar un token
class Token:
    def __init__(self, type_, value):
        self.type = type_  # Tipo de token
        self.value = value  # Valor del token

    def __str__(self):
        return f"Token(tipo={self.type}, valor='{self.value}')"

# Clase Lexer para el análisis léxico
class Lexer:
    def __init__(self, text):
        self.text = text  # Código fuente como texto
        self.pos = 0  # Posición actual en el texto

    def next_token(self):
        while self.pos < len(self.text):
            current_char = self.text[self.pos]  # Obtener el carácter actual

            # Saltar espacios en blanco
            if current_char.isspace():
                self.pos += 1
                continue

            # Manejar comentarios de línea
            if current_char == '/' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '/':
                start = self.pos
                while self.pos < len(self.text) and self.text[self.pos] != '\n':
                    self.pos += 1
                return Token(TokenType.COMMENT, self.text[start:self.pos])

            # Manejar identificadores y palabras clave
            if current_char.isalpha() or current_char == '_':
                start = self.pos
                while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
                    self.pos += 1
                identifier = self.text[start:self.pos]
                # Considerar algunas palabras clave
                if identifier in {'int', 'float', 'return', 'void', 'if', 'else', 'while'}:
                    return Token(TokenType.KEYWORD, identifier)
                return Token(TokenType.IDENTIFIER, identifier)

            # Manejar números
            if current_char.isdigit():
                start = self.pos
                while self.pos < len(self.text) and self.text[self.pos].isdigit():
                    self.pos += 1
                number = self.text[start:self.pos]
                return Token(TokenType.NUMBER, number)

            # Manejar operadores
            if current_char in {'+', '-', '*', '/', '=', '>', '<', '!', '==', '!='}:
                self.pos += 1
                return Token(TokenType.OPERATOR, current_char)

            # Manejar símbolos
            if current_char in {'(', ')', '{', '}', ';', ','}:
                self.pos += 1
                return Token(TokenType.SYMBOL, current_char)

            # Si se encuentra un carácter desconocido
            self.pos += 1
            return Token(TokenType.UNKNOWN, current_char)

        return Token(TokenType.UNKNOWN, '')  # Fin del texto

# Clase para la interfaz de usuario
class LexerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico")
        self.root.geometry("1280x720")  # Tamaño de la ventana fijada

        # Configurar los componentes de la interfaz
        self.setup_widgets()

    def setup_widgets(self):
        # Etiqueta y cuadro de texto para entrada de código
        tk.Label(self.root, text="Ingrese el código:").pack(pady=5)
        self.input_text = scrolledtext.ScrolledText(self.root, height=15, width=80)
        self.input_text.pack(pady=5)

        # Etiqueta y cuadro de texto para mostrar tokens encontrados
        tk.Label(self.root, text="Tokens encontrados:").pack(pady=5)
        self.output_text = scrolledtext.ScrolledText(self.root, height=15, width=80)
        self.output_text.pack(pady=5)

        # Botón para iniciar el análisis
        tk.Button(self.root, text="Analizar", command=self.analyze).pack(pady=10)

    def analyze(self):
        code = self.input_text.get("1.0", tk.END)  # Obtener el código de entrada
        lexer = Lexer(code)  # Crear una instancia de Lexer

        # Limpiar la salida anterior
        self.output_text.delete("1.0", tk.END)

        # Obtener el siguiente token
        token = lexer.next_token()
        while token.type != TokenType.UNKNOWN:
            self.output_text.insert(tk.END, str(token) + '\n')  # Mostrar el token
            token = lexer.next_token()  # Obtener el siguiente token

# Ejecución de la aplicación
if __name__ == "__main__":
    root = tk.Tk()  # Crear la ventana principal
    app = LexerApp(root)  # Crear la aplicación
    root.mainloop()  # Iniciar el bucle de eventos

# Int void() {
# while (true) {
# if (true)
# return;
# }
# }