def analizar_sintactico(tokens):
    errores = []
    pila_bloques = []  # Para validar {} y bloques anidados

    for token in tokens:
        if token["tipo"] == "SYMBOL":
            if token["valor"] == "{":
                pila_bloques.append("{")
            elif token["valor"] == "}":
                if not pila_bloques:
                    errores.append(f"Error en la línea {token['linea']}: '}}' inesperado.")
                else:
                    pila_bloques.pop()
        elif token["tipo"] == "OPERATOR" and token["valor"] == ";":
            continue

    # Validamos la pila de bloques al final
    if pila_bloques:
        errores.append(f"Error: faltan '{len(pila_bloques)}' cierre(s) de bloque(s) '}}'.")
    return errores
