import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import pandas as pd
import matplotlib.pyplot as plt
import random

# ==========================================
# CONFIGURACIÓN DE COLORES (Tema Dashboard)
# ==========================================
COLOR_BG = "#f4f6f9"       # Fondo general
COLOR_CARD = "#ffffff"     # Fondo de tarjetas
COLOR_TEXT = "#333333"     # Texto principal
COLOR_PRIMARY = "#4e73df"  # Azul (Principal)
COLOR_SUCCESS = "#1cc88a"  # Verde (Éxito)
COLOR_INFO = "#36b9cc"     # Cian (Info)
COLOR_WARNING = "#f6c23e"  # Naranja/Amarillo (Advertencia)
COLOR_DANGER = "#e74a3b"   # Rojo (Error)
COLOR_BURBUJA = "#e67e22"  # Naranja oscuro (Nuevo botón)

df = None

# ==========================================
# UTILIDADES DE DISEÑO
# ==========================================
def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (width/2))
    y_cordinate = int((screen_height/2) - (height/2))
    win.geometry("{}x{}+{}+{}".format(width, height, x_cordinate, y_cordinate))

def crear_boton_estilizado(padre, texto, color_fondo, comando, icono=""):
    def on_enter(e):
        btn['background'] = oscurecer_color(color_fondo)
    def on_leave(e):
        btn['background'] = color_fondo

    def oscurecer_color(hex_color, factor=0.85):
        try:
            hex_color = hex_color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            new_rgb = tuple(int(i * factor) for i in rgb)
            return '#%02x%02x%02x' % new_rgb
        except:
            return color_fondo

    btn = tk.Button(
        padre, text=f"{icono} {texto}", bg=color_fondo, fg="white",
        font=("Segoe UI", 10, "bold"), activebackground="white",
        activeforeground=color_fondo, bd=0, relief="flat", cursor="hand2",
        padx=15, pady=12, command=comando
    )
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# ==========================================
# SPLASH SCREEN
# ==========================================
def mostrar_splash():
    splash = tk.Tk()
    splash.title("Cargando...")
    center_window(splash, 500, 350)
    splash.overrideredirect(True)
    splash.config(bg="#2c3e50")

    frame = tk.Frame(splash, bg="#2c3e50")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="📊 Sistema de Análisis", font=("Segoe UI", 24, "bold"), bg="#2c3e50", fg="white").pack(pady=10)
    tk.Label(frame, text="Socioeconómico v3.1", font=("Segoe UI", 18), bg="#2c3e50", fg="#bdc3c7").pack(pady=5)

    progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=30)
    
    def update_progress():
        for i in range(1, 101):
            progress['value'] = i
            splash.update_idletasks()
            splash.after(10)
        splash.destroy()
        iniciar_aplicacion()

    splash.after(500, update_progress)
    splash.mainloop()

# ==========================================
# APLICACIÓN PRINCIPAL
# ==========================================
def iniciar_aplicacion():
    global ventana, combo_region

    ventana = tk.Tk()
    ventana.title("SocioEco Analytics v3.1")
    center_window(ventana, 950, 700)
    ventana.config(bg=COLOR_BG)
    ventana.resizable(False, False)

    # HEADER
    header = tk.Frame(ventana, bg=COLOR_CARD, height=70)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="SocioEco Analytics", font=("Segoe UI", 20, "bold"), bg=COLOR_CARD, fg=COLOR_PRIMARY).pack(side="left", padx=30, pady=15)
    tk.Label(header, text="v3.1", font=("Segoe UI", 10), bg="#e3e6f0", fg="#858796", padx=10).pack(side="right", padx=30, pady=20)

    # CONTENIDO
    content = tk.Frame(ventana, bg=COLOR_BG)
    content.pack(fill="both", expand=True, padx=30, pady=30)

    # --- PANEL DE CONFIGURACIÓN ---
    config_frame = tk.LabelFrame(content, text="  Configuración de Región  ", font=("Segoe UI", 11, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT, bd=1, relief="flat")
    config_frame.pack(fill="x", pady=(0, 20), ipady=15)

    lbl_region = tk.Label(config_frame, text="Región a Analizar:", font=("Segoe UI", 11), bg=COLOR_CARD, fg=COLOR_TEXT)
    lbl_region.grid(row=0, column=0, padx=20, pady=10)

    combo_region = ttk.Combobox(config_frame, state="readonly", width=35, font=("Segoe UI", 10))
    combo_region.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # --- GRID DE BOTONES (3x3) ---
    actions_frame = tk.Frame(content, bg=COLOR_BG)
    actions_frame.pack(expand=True, fill="both")

    # Estilos para que las columnas crezcan equitativamente
    for i in range(3):
        actions_frame.grid_columnconfigure(i, weight=1)

    # === FILA 1: DATOS ===
    btn_demo = crear_boton_estilizado(actions_frame, "Cargar Demo", COLOR_SUCCESS, cargar_datos_demo, "🎲")
    btn_demo.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    btn_csv = crear_boton_estilizado(actions_frame, "Cargar CSV", COLOR_PRIMARY, cargar_csv, "📂")
    btn_csv.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    btn_export = crear_boton_estilizado(actions_frame, "Exportar Excel", COLOR_WARNING, exportar_excel, "📥")
    btn_export.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    # === FILA 2: GRÁFICAS ===
    btn_barras = crear_boton_estilizado(actions_frame, "Gráfica Barras", COLOR_INFO, generar_grafica, "📊")
    btn_barras.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    btn_circular = crear_boton_estilizado(actions_frame, "Gráfica Pastel", "#9b59b6", grafica_circular, "🍕")
    btn_circular.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # === NUEVO BOTÓN ===
    btn_burbujas = crear_boton_estilizado(actions_frame, "Análisis Burbujas", COLOR_BURBUJA, generar_grafica_burbujas, "🫧")
    btn_burbujas.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

    # === FILA 3: SISTEMA ===
    btn_limpiar = crear_boton_estilizado(actions_frame, "Limpiar Filtros", "#34495e", limpiar_datos, "🧹")
    btn_limpiar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    btn_acerca = crear_boton_estilizado(actions_frame, "Acerca de", "#7f8c8d", acerca_de, "ℹ️")
    btn_acerca.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    btn_salir = crear_boton_estilizado(actions_frame, "Salir", COLOR_DANGER, salir, "❌")
    btn_salir.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

    ventana.mainloop()

# ==========================================
# LÓGICA DE DATOS
# ==========================================
def cargar_datos_demo():
    global df
    regiones = ["América Latina", "Europa", "Asia", "África"]
    data = []
    for r in regiones:
        for i in range(20):
            data.append({
                "region": r,
                "country": f"Pais {random.randint(1, 50)} ({r})",
                "gdp_per_capita_usd": random.randint(2000, 65000),
                "internet_penetration_pct": random.randint(10, 98)
            })
    df = pd.DataFrame(data)
    
    combo_region["values"] = sorted(df["region"].unique())
    if combo_region["values"]: combo_region.current(0)
    messagebox.showinfo("Éxito", "¡Datos demo cargados! Puedes probar todas las gráficas.")

def cargar_csv():
    global df
    archivo = filedialog.askopenfilename(title="Seleccionar CSV", filetypes=[("Archivos CSV", "*.csv")])
    if not archivo: return
    try:
        df = pd.read_csv(archivo)
        cols_req = ["region", "country", "gdp_per_capita_usd", "internet_penetration_pct"]
        if not all(c in df.columns for c in cols_req):
            messagebox.showerror("Error", "El CSV necesita columnas: region, country, gdp_per_capita_usd, internet_penetration_pct")
            df = None
            return
        combo_region["values"] = sorted(df["region"].unique())
        if combo_region["values"]: combo_region.current(0)
        messagebox.showinfo("OK", "CSV Cargado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def limpiar_datos():
    global df
    df = None
    combo_region.set('')
    messagebox.showinfo("Limpiado", "Datos filtrados eliminados de memoria.")

def verificar_datos():
    if df is None: messagebox.showwarning("Sin Datos", "Carga datos primero (Demo o CSV)"); return False
    return True

# ==========================================
# GRÁFICAS
# ==========================================

# 1. GRÁFICA DE BARRAS (Existente)
def generar_grafica():
    if not verificar_datos(): return
    try:
        region = combo_region.get()
        datos = df[df["region"] == region]
        top = datos.groupby("country")["gdp_per_capita_usd"].mean().sort_values(ascending=False).head(10)
        
        plt.figure(figsize=(10, 5), facecolor='white')
        plt.bar(top.index, top.values, color=COLOR_PRIMARY, alpha=0.8)
        plt.title(f"Top 10 PIB per Cápita - {region}", fontweight='bold', fontsize=14, color=COLOR_TEXT)
        plt.xlabel("País", color=COLOR_TEXT)
        plt.ylabel("PIB (USD)", color=COLOR_TEXT)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.show()
    except Exception as e: messagebox.showerror("Error", str(e))

# 2. GRÁFICA CIRCULAR (Existente)
def grafica_circular():
    if not verificar_datos(): return
    try:
        region = combo_region.get()
        datos = df[df["region"] == region]
        top = datos.groupby("country")["internet_penetration_pct"].mean().sort_values(ascending=False).head(5)
        
        plt.figure(figsize=(7, 7), facecolor='white')
        colors = [COLOR_PRIMARY, COLOR_SUCCESS, COLOR_INFO, COLOR_WARNING, COLOR_DANGER]
        plt.pie(top, labels=top.index, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
        plt.title(f"Top 5 Internet - {region}", fontweight='bold', fontsize=14)
        plt.tight_layout()
        plt.show()
    except Exception as e: messagebox.showerror("Error", str(e))

# 3. NUEVA GRÁFICA DE BURBUJAS (CREATIVA)
def generar_grafica_burbujas():
    if not verificar_datos(): return
    try:
        region = combo_region.get()
        datos = df[df["region"] == region]
        
        # Tomar una muestra aleatoria si hay demasiados países para que se vea limpio
        if len(datos) > 30:
            datos = datos.sample(30)
            
        x = datos['internet_penetration_pct']
        y = datos['gdp_per_capita_usd']
        
        # Tamaño de la burbuja proporcional al PIB (con factor de escala)
        sizes = y / 1000 * 10 
        
        # Color de las burbujas basado en el PIB (más rico = más oscuro)
        plt.figure(figsize=(12, 8), facecolor='white')
        
        scatter = plt.scatter(
            x, y, 
            s=sizes, 
            c=y, 
            cmap='Blues', # Gradiente de azules
            alpha=0.6,    # Transparencia
            edgecolors='white',
            linewidth=1.5
        )
        
        # Añadir barra de color
        cbar = plt.colorbar(scatter)
        cbar.set_label('PIB per Cápita (USD)', fontsize=10)
        
        # Títulos y Etiquetas
        plt.title(f"Correlación: Internet vs. PIB - {region}", fontsize=16, fontweight='bold', color=COLOR_TEXT, pad=20)
        plt.xlabel("Penetración de Internet (%)", fontsize=12, color=COLOR_TEXT)
        plt.ylabel("PIB per Cápita (USD)", fontsize=12, color=COLOR_TEXT)
        
        # Grilla suave
        plt.grid(True, linestyle='--', alpha=0.4)
        
        # Anotaciones (opcional: nombres de países si no son demasiados)
        for i, txt in enumerate(datos['country']):
            # Solo anotar si es un dato destacado para no saturar
            if y.iloc[i] > y.mean() or x.iloc[i] > x.mean():
                plt.annotate(txt.split(' ')[0], (x.iloc[i], y.iloc[i]), fontsize=8, alpha=0.7)

        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

def exportar_excel():
    if not verificar_datos(): return
    try:
        region = combo_region.get()
        datos = df[df["region"] == region]
        archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if archivo:
            datos.to_excel(archivo, index=False)
            messagebox.showinfo("Éxito", f"Exportado a {archivo}")
    except Exception as e: messagebox.showerror("Error", str(e))

def acerca_de():
    messagebox.showinfo("Acerca de", "SocioEco Analytics v3.1\nDesarrollado por: Victoria Balam\n\nIncluye:\n- Barras\n- Pastel\n- Burbujas (Novedad)")

def salir():
    if messagebox.askyesno("Salir", "¿Cerrar aplicación?"): ventana.destroy()

if __name__ == "__main__":
    mostrar_splash()