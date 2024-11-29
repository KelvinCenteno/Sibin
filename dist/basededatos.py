import pg8000

# Datos de conexión a la base de datos
db_config = {
    'database': 'postgres',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',  # Cambia esto si tu base de datos está en otro servidor
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

# Función para validar usuario y contraseña
def validar_usuario(usuario, contrasena):
    conexion = conectar()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        query = "SELECT 1 FROM usuarios WHERE usuario = %s AND contrasena = %s"
        cursor.execute(query, (usuario, contrasena))
        result = cursor.fetchone()
        cursor.close()
        conexion.close()
        return result is not None
    except Exception as e:
        print(f"Error al validar usuario: {e}")
        return False

# Ejemplo de uso
usuario = input("Nombre de usuario: ")
contrasena = input("Contraseña: ")

if validar_usuario(usuario, contrasena):
    print("Acceso concedido")
    # Aquí puedes continuar con el acceso
else:
    print("Acceso denegado")
