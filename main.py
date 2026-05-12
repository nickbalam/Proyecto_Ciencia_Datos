import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import time

df = None

splash = tk.Tk()

splash.title("Bienvenido")
splash.geometry("500x300")
splash.config(bg="#1e3a8a")

mensaje = tk.Label(
    splash,
    text="Sistema de Análisis Socioeconómico",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="#1e3a8a"
)

mensaje.pack(expand=True)

submensaje = tk.Label(
    splash,
    text="Cargando aplicación...",
    font=("Arial", 12),
    fg="white",
    bg="#1e3a8a"
)

submensaje.pack(pady=20)

splash.update()

time.sleep(3)

splash.destroy()

ventana = tk.Tk()

ventana.title("Sistema de Análisis Socioeconómico")
ventana.geometry("800x600")
ventana.config(bg="#dbeafe")

titulo = tk.Label(
    ventana,
    text="Sistema de Análisis Socioeconómico",
    font=("Arial", 24, "bold"),
    bg="#dbeafe",
    fg="#1e3a8a"
)

titulo.pack(pady=20)

label_region = tk.Label(
    ventana,
    text="Selecciona una región:",
    font=("Arial", 12, "bold"),
    bg="#dbeafe"
)

label_region.pack()

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

        region = combo_region.get()

        datos_filtrados = df[
            df["region"] == region
        ]

        top_internet = datos_filtrados.groupby(
            "country"
        )["internet_penetration_pct"].mean().sort_values(
            ascending=False
        ).head(5)

        plt.figure(figsize=(7,7))

        plt.pie(
            top_internet,
            labels=top_internet.index,
            autopct='%1.1f%%'
        )

        plt.title(
            f"Top 5 acceso a internet - {region}"
        )

        plt.show()

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"No se pudo generar la gráfica\n\n{e}"
        )

def exportar_excel():

    try:

        region = combo_region.get()

        datos_filtrados = df[
            df["region"] == region
        ]

        datos_filtrados.to_excel(
            "reporte_filtrado.xlsx",
            index=False
        )

        messagebox.showinfo(
            "Exportación exitosa",
            "Reporte exportado correctamente"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"No se pudo exportar\n\n{e}"
        )

def acerca_de():

    messagebox.showinfo(
        "Acerca de",
        "Sistema de Análisis Socioeconómico\n\n"
        "Desarrollado por: Victoria Balam\n\n"
        "Librerías utilizadas:\n"
        "- tkinter\n"
        "- pandas\n"
        "- matplotlib\n"
        "- openpyxl"
    )


def salir():
    respuesta = messagebox.askyesmo(
        "Salir",
        "¿Deseas salir?"
    )
    if respuesta:
        ventana.destroy()

btn_csv = tk.Button(
    ventana,
    text="Cargar CSV",
    width=25,
    height=2,
    bg="#2563eb",
    fg="white",
    font=("Arial", 11, "bold"),
    command=cargar_csv
)

btn_csv.pack(pady=10)

btn_grafica = tk.Button(
    ventana,
    text="Generar gráfica",
    width=25,
    height=2,
    bg="#16a34a",
    fg="white",
    font=("Arial", 11, "bold"),
    command=generar_grafica
)

btn_grafica.pack(pady=10)

btn_circular = tk.Button(
    ventana,
    text="Gráfica circular",
    width=25,
    height=2,
    bg="#9333ea",
    fg="white",
    font=("Arial", 11, "bold"),
    command=grafica_circular
)

btn_circular.pack(pady=10)

btn_excel = tk.Button(
    ventana,
    text="Exportar Excel",
    width=25,
    height=2,
    bg="#ea580c",
    fg="white",
    font=("Arial", 11, "bold"),
    command=exportar_excel
)

btn_excel.pack(pady=10)

btn_acerca = tk.Button(
    ventana,
    text="Acerca de",
    width=25,
    height=2,
    bg="#0f172a",
    fg="white",
    font=("Arial", 11, "bold"),
    command=acerca_de
)

btn_salir = tk.Button(
    ventana,
    text="Salir",
    width=25,
    height=2,
    bg="#dc2626",
    fg="white",
    font=("Arial", 11, "bold"),
    command=salir
)

btn_salir.pack(pady=10)
ventana.mainloop()