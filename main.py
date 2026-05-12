import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt

df = None

ventana = tk.Tk()
ventana.title("Proyecto Ciencia de Datos")
ventana.geometry("800x600")

titulo = tk.Label(
    ventana,
    text="Proyecto Ciencia de Datos",
    font=("Arial", 20)
)
titulo.pack(pady=20)

label_region = tk.Label(
    ventana,
    text="Selecciona una región:"
)

label_region.pack()

# ComboBox
combo_region = ttk.Combobox(
    ventana,
    state="readonly",
    width=30
)

combo_region.pack(pady=10)

def cargar_csv():
    global df

    try:
        df = pd.read_csv("datos.csv")

        regiones = sorted(
            df["region"].unique()
        )

        combo_region["values"] = regiones

        filas = len(df)
        columnas = len(df.columns)

        messagebox.showinfo(
            "CSV cargado",
            f"Archivo cargado correctamente\n\n"
            f"Filas: {filas}\n"
            f"Columnas: {columnas}"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"No se pudo cargar el archivo\n\n{e}"
        )

def generar_grafica():

    try:

        region = combo_region.get()

        # Filtrar región
        datos_filtrados = df[
            df["region"] == region
        ]

        top_paises = datos_filtrados.groupby(
            "country"
        )["gdp_per_capita_usd"].mean().sort_values(
            ascending=False
        ).head(10)

        plt.figure(figsize=(10,5))

        top_paises.plot(kind="bar")

        plt.title(
            f"Top 10 PIB per cápita - {region}"
        )

        plt.xlabel("País")
        plt.ylabel("PIB per cápita USD")

        plt.tight_layout()

        plt.show()

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"No se pudo generar la gráfica\n\n{e}"
        )
def grafica_circular():

    try:
        # Contar categorías
        conteo = df.iloc[:, 0].value_counts().head(5)

        # Crear gráfica circular
        plt.figure(figsize=(7,7))

        plt.pie(
            conteo,
            labels=conteo.index,
            autopct='%1.1f%%'
        )

        plt.title("Distribución de categorías")

        plt.show()

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"No se pudo generar la gráfica circular\n\n{e}"
        )

def exportar_excel():

    try:
        # Exportar dataframe
        df.to_excel(
            "reporte.xlsx",
            index=False
        )

        messagebox.showinfo(
            "Exportación exitosa",
            "El reporte se exportó correctamente"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"No se pudo exportar el archivo\n\n{e}"
        )

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

btn_circular = tk.Button(
    ventana,
    text="Gráfica circular",
    width=20,
    command=grafica_circular
)

btn_circular.pack(pady=10)
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