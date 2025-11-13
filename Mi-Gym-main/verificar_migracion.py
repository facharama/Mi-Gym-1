import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'migym_registro.settings.local')
django.setup()

from django.db import connection

# Verificar conexión
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'dbo'")
        tabla_count = cursor.fetchone()[0]
        print(f"✅ Conexión a SQL Server exitosa")
        print(f"✅ Tablas creadas en la BD: {tabla_count}")
        
        # Listar tablas
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'dbo' ORDER BY table_name")
        print("\n📋 Tablas en la base de datos:")
        for row in cursor.fetchall():
            print(f"   - {row[0]}")
except Exception as e:
    print(f"❌ Error: {e}")
