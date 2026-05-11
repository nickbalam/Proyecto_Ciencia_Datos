import tkinter as tk
from tkinter import messagebox

ventana = tk.Tk()
ventana.title("Proyecto Ciencia de Datos")
ventana.geometry("800x600")

titulo = tk.Label(
    ventana,
    text="Proyecto Ciencia de Datos",
    font=("Arial", 20)
)
titulo.pack(pady=20)

def cargar_csv():
    messagebox.showinfo("Cargar","Aquí carga el csv")

def generar_grafica():
    messagebox.showinfo("Gráfica", "Aquí se carga la gráfica")

def exportar_excel():
    messagebox.showinfo("Excel", "Aquí se exportará el reporte")

def acerca_de():
    messagebox.showinfo(
        "Acerca de",
        "Proyecto realizado por Victoria Balam"
    )

def salir():
    respuesta = messagebox.askyesmo(
        "Salir",
        "¿Deseas salir?"
    )
    if respuesta:
        ventana.destroy()


btn_csv=tk.Button(
    ventana,
    text="Cargar CSV",
    width=20,
    command=cargar_csv
)
btn_csv.pack(pady=10)

btn_grafica = tk.Button(
    ventana,
    text="Generar gráfica",
    width=20,
    command=generar_grafica
)
btn_grafica.pack(pady=10)

btn_excel = tk.Button(
    ventana,
    text="Exportar Excel",
    width=20,
    command=exportar_excel
)
btn_excel.pack(pady=10)

btn_acerca = tk.Button(
    ventana,
    text="Acerca de",
    width=20,
    command=acerca_de
)
btn_acerca.pack(pady=10)

btn_salir = tk.Button(
    ventana,
    text="Salir",
    width=20,
    command=salir
)
btn_salir.pack(pady=10)
ventana.mainloop()