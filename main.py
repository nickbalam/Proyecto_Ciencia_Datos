import tkinter as tk

ventana = tk.Tk()
ventana.title("Proyecto Ciencia de Datos")
ventana.geometry("800x600")

titulo = tk.Label(
    ventana,
    text="Proyecto Ciencia de Datos",
    font=("Arial", 20)
)
titulo.pack(pady=20)

ventana.mainloop()