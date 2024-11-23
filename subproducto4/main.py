import tkinter as tk
from tkinter import filedialog
from analizador_lexico import analizar_lexico
from analizador_sintactico import analizar_sintactico
from analizador_semantico import analizar_semantico


def cargar_archivo():
    """Carga el contenido de un archivo .txt en el área de código."""
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "r") as f:
            codigo = f.read()
        codigo_fuente.delete("1.0", tk.END)
        codigo_fuente.insert(tk.END, codigo)


def analizar_codigo():
    """Ejecuta los análisis léxico, sintáctico y semántico, y muestra los resultados."""
    codigo = codigo_fuente.get("1.0", tk.END)
    tokens = analizar_lexico(codigo)

    # Mostrar resultados léxicos
    analisis_lexico.delete("1.0", tk.END)
    for token in tokens:
        analisis_lexico.insert(tk.END, f"{token['linea']}\t{token['tipo']}\t{token['valor']}\n")

    # Ejecutar análisis sintáctico
    errores_sintacticos = analizar_sintactico(tokens)
    analisis_sintactico.delete("1.0", tk.END)
    if errores_sintacticos:
        for error in errores_sintacticos:
            analisis_sintactico.insert(tk.END, error + "\n")
    else:
        analisis_sintactico.insert(tk.END, "Análisis sintáctico realizado correctamente.")

    # Ejecutar análisis semántico
    errores_semanticos = analizar_semantico(tokens)
    analisis_semantico.delete("1.0", tk.END)
    if errores_semanticos:
        for error in errores_semanticos:
            analisis_semantico.insert(tk.END, error + "\n")
    else:
        analisis_semantico.insert(tk.END, "Análisis semántico realizado correctamente.")


# Configuración de la GUI
root = tk.Tk()
root.title("Analizador Léxico, Sintáctico y Semántico")
root.geometry("1200x720")  # Tamaño fijo
root.resizable(False, False)

# Etiquetas
tk.Label(root, text="Código Fuente", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=5)
tk.Label(root, text="Análisis Léxico", font=("Arial", 10, "bold")).grid(row=2, column=0, pady=5)
tk.Label(root, text="Análisis Sintáctico", font=("Arial", 10, "bold")).grid(row=2, column=1, pady=5)
tk.Label(root, text="Análisis Semántico", font=("Arial", 10, "bold")).grid(row=2, column=2, pady=5)

# Áreas de texto
codigo_fuente = tk.Text(root, height=15, width=120)
codigo_fuente.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

analisis_lexico = tk.Text(root, height=15, width=40)
analisis_lexico.grid(row=3, column=0, padx=5, pady=5)
analisis_sintactico = tk.Text(root, height=15, width=40)
analisis_sintactico.grid(row=3, column=1, padx=5, pady=5)
analisis_semantico = tk.Text(root, height=15, width=40)
analisis_semantico.grid(row=3, column=2, padx=5, pady=5)

# Botones
btn_cargar = tk.Button(root, text="Cargar Código", command=cargar_archivo)
btn_cargar.grid(row=4, column=0, pady=10)

btn_analizar = tk.Button(root, text="Compilar", command=analizar_codigo)
btn_analizar.grid(row=4, column=1, pady=10)

root.mainloop()
