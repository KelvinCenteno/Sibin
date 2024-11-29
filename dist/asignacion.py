import tkinter as tk
from tkinter import Canvas, Menu, ttk, messagebox
import cv2, subprocess
from PIL import Image, ImageTk, ImageDraw, ImageFont
from rounded_rectangle_drawer import RoundedRectangleDrawer
import qrcode, pg8000, os
from pathlib import Path

db_config = {
    'database': 'Bienes',
    'user': 'postgres',
    'password': 'admin',
    'host': '175.16.0.83',  # Cambia esto si tu base de datos está en otro servidor
    'port': 5432          # Puerto por defecto de PostgreSQL
}

# Función para establecer la conexión
def conectar():
    try:
        conexion = pg8000.connect(**db_config)
        return conexion
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Configuración de la ventana principal
root = tk.Tk()
root.title("Reproductor de Vídeo")
# Definir el tamaño de la ventana
ancho_ventana = root.winfo_screenwidth() - 200
alto_ventana = root.winfo_screenheight() - 120

def cerrar():
    root.destroy()
    
# Obtener el tamaño de la pantalla
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()

# Calcular la posición x, y para centrar la ventana
posicion_x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
posicion_y = int((alto_pantalla / 2) - (alto_ventana / 1.9))

# Ajustar las dimensiones y la posición de la ventana
root.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")
root.resizable(False, False)
root.overrideredirect(True)

# Crear el Canvas en la ventana principal
canvas = tk.Canvas(root, width=ancho_ventana, height=alto_ventana, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Cargar y redimensionar la imagen de fondo
Img_f = Image.open("Imagen1.jpg")
Img_f = Img_f.resize((ancho_pantalla, alto_pantalla))
fondo = ImageTk.PhotoImage(Img_f)
canvas.create_image(0, 0, image=fondo, anchor="nw")

text_Tit = Image.new("RGBA", (800, 60), (255, 255, 255, 0))
drawTit = ImageDraw.Draw(text_Tit)
fontTit = ImageFont.truetype("arialbd.ttf", 40)
drawTit.text((10, 10), "ASIGNACIÓN DE BIENES NACIONALES", font=fontTit, fill=(255, 255, 255, 255))
Tit_photo2 = ImageTk.PhotoImage(text_Tit)
canvas.create_image(ancho_ventana/2, 70, anchor=tk.CENTER, image=Tit_photo2)

# Crear imagen de texto "X" para cerrar la ventana
text_image40 = Image.new("RGBA", (60, 50), (255, 255, 255, 0))
draw40 = ImageDraw.Draw(text_image40)
font40 = ImageFont.truetype("arialbd.ttf", 16)
draw40.text((10, 10), "X", font=font40, fill=(255, 255, 255, 255))
text_photo40 = ImageTk.PhotoImage(text_image40)
imagen_id = canvas.create_image(ancho_ventana - 40, 5, anchor="nw", image=text_photo40)
canvas.tag_bind(imagen_id, "<Button-1>", lambda event: root.destroy())

text_Ger = Image.new("RGBA", (220, 60), (255, 255, 255, 0))
draw22 = ImageDraw.Draw(text_Ger)
fontGer = ImageFont.truetype("arialbd.ttf", 20)
draw22.text((10, 10), "GERENCIA:", font=fontGer, fill=(255, 255, 255, 255))
Ger_photo2 = ImageTk.PhotoImage(text_Ger)
canvas.create_image(320, 300, anchor=tk.CENTER, image=Ger_photo2)

# Función para cargar las opciones desde un archivo .txt
def cargar_opciones(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        opciones = [linea.strip() for linea in f]
    return opciones

# Cargar las opciones desde el archivo
opciones = cargar_opciones("gerencias.txt")

    #Caja de Texto Usuario
caja_usuario = ttk.Combobox(root, width=30, values=opciones, state="readonly")
caja_usuario.place(x=360, y=281, height=25)

    # Crear imagen de texto "CONTRASEÑA"
text_image = Image.new("RGBA", (220, 70), (255, 255, 255, 0))
draw = ImageDraw.Draw(text_image)
font = ImageFont.truetype("arialbd.ttf", 20)
draw.text((10, 10), "PRODUCTO A\n ASIGNAR:", font=font, fill=(255, 255, 255, 255))
text_photo = ImageTk.PhotoImage(text_image)
canvas.create_image(320, 380, anchor=tk.CENTER, image=text_photo)

    #Caja de Texto Usuario
#caja_contra = tk.Entry(root, font=("arial", "12"))
#buscar = canvas.create_window(480, 375, window=caja_contra, height=25)
# Cargar las opciones desde el archivo
opciones2 = cargar_opciones("Productos_disponibles.txt")

    #Caja de Texto Usuario
caja_prod = ttk.Combobox(root, width=30, values=opciones2,  state="readonly")
caja_prod.place(x=365, y=364, height=25)

Img_lup = Image.open("Lupa.png")
Img_lup = Img_lup.resize((20, 25))
lupa = ImageTk.PhotoImage(Img_lup)
canvas.create_image(578, 375, image=lupa)

    #Texto de fecha
text_image23 = Image.new("RGBA", (220, 70), (255, 255, 255, 0))
draw23 = ImageDraw.Draw(text_image23)
font23 = ImageFont.truetype("arialbd.ttf", 20)
draw23.text((10, 10), "FECHA DE\nASIGNACIÓN:", font=font23, fill=(255, 255, 255, 255))
text_photo23 = ImageTk.PhotoImage(text_image23)
canvas.create_image(720, 300, anchor=tk.CENTER, image=text_photo23)

    #Caja de Fecha
caja_fecha = tk.Entry(root, font=("arial", "12"))
canvas.create_window(ancho_ventana-300, 293, window=caja_fecha, height=25)

Img_Cal = Image.open("Calendario.png")
Img_Cal = Img_Cal.resize((20, 25))
calend = ImageTk.PhotoImage(Img_Cal)
canvas.create_image(ancho_ventana-195, 293, image=calend)

    #Texto de fecha
text_image24 = Image.new("RGBA", (220, 40), (255, 255, 255, 0))
draw24 = ImageDraw.Draw(text_image24)
font24 = ImageFont.truetype("arialbd.ttf", 12)
draw24.text((10, 10), "CODIGO QR ", font=font24, fill=(255, 255, 255, 255))
text_photo24 = ImageTk.PhotoImage(text_image24)
canvas.create_image(ancho_ventana-250, 600, anchor=tk.CENTER, image=text_photo24)

    #numeros = list(range(1, 100))
    #caja_usuario = ttk.Spinbox(root, width=30, values= numeros, state="readonly")
    #caja_usuario.place(x=900, y=281, height=25)
global Cod_qr
Cod_qr = tk.Canvas(root, width=220, height=220, highlightthickness=0)
canvas.create_window(ancho_ventana-300, 480, window=Cod_qr)

def crear_text_image(width, height, color):
    text_image = Image.new("RGBA", (width, height), color)
    return ImageTk.PhotoImage(text_image)

text_photo5 = crear_text_image(235, 235, (255, 225, 225, 80))
canvas.create_image(ancho_ventana-417, 364, anchor="nw", image=text_photo5)

text_image100 = Image.new("RGBA", (200, 120), (255, 255, 255, 0))
draw100 = ImageDraw.Draw(text_image100)
font100 = ImageFont.truetype("arialbd.ttf", 16)
draw100.text((10, 10), "SISTEMA DE\nINVENTARIO PARA\nBIENES NACIONALES\n(SIBIN)", font=font100, fill=(255, 255, 255, 255), align="center")
text_photo100 = ImageTk.PhotoImage(text_image100)
canvas.create_image(102, 200, anchor=tk.CENTER, image=text_photo100)

# Crear imagen del logo
Img_Co = Image.open("logo2.jpg")
Img_Co = Img_Co.resize((100, 100))
ConterTitle = ImageTk.PhotoImage(Img_Co)
canvas.create_image(100, 80, image=ConterTitle)


def Generar_codigo():
    # Datos para generar el QR
    if caja_fecha.get() == "" or caja_prod.get()=="" or caja_usuario.get()=="":
        messagebox.showerror("CAMPOS VACIOS", "NO PUEDE HABER NINGUN CAMPO EN BLANCO")
    else:
            datos = f"Ubicación: {caja_usuario.get()}\nProducto: {caja_prod.get()}"
            
            # Crear el código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(datos)
            qr.make(fit=True)

            #import os
            # Crear la imagen QR
            imagen_qr = qr.make_image(fill_color="black", back_color="white")

            # Obtener la ruta del directorio de Documentos del usuario
            documentos_path = Path.home() / "Documents"

            # Crear la carpeta "codigos_qr" en el directorio de Documentos si no existe
            folder_path = documentos_path / "codigos_qr"
            if not folder_path.exists():
                folder_path.mkdir(parents=True)

            # Guardar la imagen QR en la carpeta "codigos_qr"
            name = f"Ubicación{caja_usuario.get()}Producto{caja_prod.get()}"
            qr_path = folder_path / (name + ".png")
            imagen_qr.save(qr_path)
            print(qr_path)

            global Img_Co2
            global ConterTitle2
            Img_Co2 = Image.open(qr_path)
            Img_Co2 = Img_Co2.resize((220, 220))
            ConterTitle2 = ImageTk.PhotoImage(Img_Co2)
            #canvas.create_image(60, 80, image=ConterTitle2)
            Cod_qr.create_image(0, 0, anchor="nw", image=ConterTitle2)

# Crear botón "INGRESAR"
btn_asignar = tk.Button(root, text="ASIGNAR", font=("arialbd","10"), bg="red4", fg="white", relief="raised", width=8, padx=15, pady=2, cursor="hand2",
                    highlightcolor="black", highlightbackground="white", borderwidth=5, highlightthickness=2, command=Generar_codigo)
canvas.create_window(320, 480, window=btn_asignar)


def Limpiar():
    caja_usuario.set("")
    caja_prod.set("")
    caja_fecha.delete(0, tk.END)
    Cod_qr.delete("all")


btn_limpiar = tk.Button(root, text="LIMPIAR", font=("arialbd.ttf","10"), bg="red4", fg="white", relief="raised", width=8, padx=15, pady=2, cursor="hand2",
                    highlightcolor="black", highlightbackground="white", borderwidth=5, highlightthickness=2, command=Limpiar)
canvas.create_window(500, 480, window=btn_limpiar)
# Crear imagen de texto "USUARIO"
root.mainloop()

