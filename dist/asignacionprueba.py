import pg8000

# Configuración de la base de datos
db_config = {
    'database': 'Bienes',
    'user': 'postgres',
    'password': 'admin',
    'host': '175.16.0.83',  # Cambia esto si tu base de datos está en otro servidor
    'port': 5432          # Puerto por defecto de PostgreSQL
}

# Leer la imagen como binario
ruta_imagen = r"C:\Users\advps_local\Downloads\prueba.png"
with open(ruta_imagen, "rb") as archivo:
    imagen_binaria = archivo.read()

# Insertar los datos en la base de datos
def insertar_datos(ubicacion, producto, fecha, imagen_binaria):
    try:
        conexion = pg8000.connect(**db_config)
        cursor = conexion.cursor()
        query = """
        INSERT INTO asignaciones (ubicacion, producto, fecha_asignacion, codigo_qr)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (ubicacion, producto, fecha, pg8000.Binary(imagen_binaria)))
        conexion.commit()
        cursor.close()
        conexion.close()
        print("Datos insertados correctamente.")
    except Exception as e:
        print(f"Error al insertar datos: {e}")

# Datos a insertar
ubicacion = "Ubicación de Prueba"
producto = "Producto de Prueba"
fecha = "2024-11-28"

# Insertar los datos incluyendo la imagen binaria
insertar_datos(ubicacion, producto, fecha, imagen_binaria)
