def analizar_semantico(tokens):
    """
    Analiza semánticamente el código para verificar:
    - Declaración de variables (y tipos).
    - Operaciones entre tipos incompatibles.
    - Uso de variables no declaradas.
    """
    tabla_simbolos = {}  # Diccionario para almacenar variables y sus tipos
    errores = []
    ultima_variable = None  # Almacena la última variable vista (para operaciones)

    for i, token in enumerate(tokens):
        if token["tipo"] == "KEYWORD" and token["valor"] in {"int", "float"}:
            # Declaración de tipo detectada
            tipo_actual = token["valor"]
            if i + 1 < len(tokens) and tokens[i + 1]["tipo"] == "IDENTIFIER":
                nombre_variable = tokens[i + 1]["valor"]
                if nombre_variable in tabla_simbolos:
                    errores.append(f"Error en la línea {token['linea']}: La variable '{nombre_variable}' ya fue declarada.")
                else:
                    # Guardamos la variable con su tipo
                    tabla_simbolos[nombre_variable] = tipo_actual

        elif token["tipo"] == "IDENTIFIER":
            # Verificamos si la variable está declarada
            if token["valor"] not in tabla_simbolos:
                errores.append(f"Error en la línea {token['linea']}: La variable '{token['valor']}' no ha sido declarada.")
            else:
                ultima_variable = token["valor"]  # Guardamos la última variable usada

        elif token["tipo"] == "OPERATOR" and token["valor"] in {"+", "-", "*", "/"}:
            # Validación de tipos en operaciones aritméticas
            if ultima_variable is not None:
                tipo_ultima = tabla_simbolos.get(ultima_variable)
                if i + 1 < len(tokens) and tokens[i + 1]["tipo"] == "IDENTIFIER":
                    siguiente_variable = tokens[i + 1]["valor"]
                    if siguiente_variable in tabla_simbolos:
                        tipo_siguiente = tabla_simbolos[siguiente_variable]
                        if tipo_ultima != tipo_siguiente:
                            errores.append(
                                f"Error en la línea {token['linea']}: Operación entre tipos incompatibles "
                                f"({tipo_ultima} y {tipo_siguiente})."
                            )
    return errores
