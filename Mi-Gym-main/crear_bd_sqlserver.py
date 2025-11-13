import pyodbc

# Conectar al servidor SQL Server (sin especificar base de datos)
try:
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};'
        'Server=DESKTOP-VINM4D7;'
        'Trusted_Connection=yes;',
        autocommit=True
    )
    
    cursor = conn.cursor()
    
    # Crear la base de datos si no existe
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'Mi-Gym') CREATE DATABASE [Mi-Gym];")
    
    print("✅ Base de datos 'Mi-Gym' creada exitosamente")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
