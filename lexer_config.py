# lexer_config.py

# Palabras reservadas
keywords = {"print", "if", "else", "while", "for"}

# Operadores aritméticos
operators = {"+", "-", "*", "/"}

# Operadores lógicos
logical_operators = {"&&", "||", "!"}

# Símbolos especiales
symbols = {"%", "$", "&", "|", "(", ")", "{", "}", ";", ","}

# Tipos de datos primitivos
primitive_types = {"int", "float"}

def is_keyword(word):
    return word in keywords

def is_operator(op):
    return op in operators or op in logical_operators

def is_symbol(sym):
    return sym in symbols

def is_primitive_type(ptype):
    return ptype in primitive_types
