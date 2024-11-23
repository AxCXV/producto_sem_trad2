import re

def analizar_lexico(codigo):
    """
    Analiza léxicamente el código fuente y devuelve una lista de tokens.
    """
    # Definir los patrones para los diferentes tipos de tokens
    patrones = [
        ("KEYWORD", r"\b(int|float|char|if|else|return|for|while|main)\b"),
        ("IDENTIFIER", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
        ("NUMBER", r"\b\d+(\.\d+)?\b"),
        ("SYMBOL", r"[{}()\[\];]"),
        ("OPERATOR", r"[=+\-*/]"),
        ("WHITESPACE", r"\s+"),  # Espacios y saltos de línea
    ]

    # Combinar todos los patrones en una sola expresión regular
    patron_general = "|".join(f"(?P<{nombre}>{patron})" for nombre, patron in patrones)
    regex = re.compile(patron_general)

    tokens = []
    linea_actual = 1

    for match in regex.finditer(codigo):
        tipo = match.lastgroup
        valor = match.group(tipo)

        if tipo == "WHITESPACE":
            # Contar líneas en saltos de línea y omitir los espacios
            linea_actual += valor.count("\n")
            continue  # No agregar los espacios ni los saltos como tokens

        tokens.append({"linea": linea_actual, "tipo": tipo, "valor": valor})

    return tokens
