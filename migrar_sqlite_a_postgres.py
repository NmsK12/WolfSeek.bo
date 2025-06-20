import sqlite3
import psycopg2

# Tu URL de Railway aquí:
POSTGRES_URL = "postgresql://postgres:boPXUBmrigkjsXdNZUxrNVZBEnmMWVnI@caboose.proxy.rlwy.net:34752/railway"

# Conexión a SQLite
sqlite_conn = sqlite3.connect('wolfseek_bot.db')
sqlite_cursor = sqlite_conn.cursor()

# Conexión a PostgreSQL
pg_conn = psycopg2.connect(POSTGRES_URL)
pg_cursor = pg_conn.cursor()

# Crea las tablas en PostgreSQL (ajusta según tu modelo)
pg_cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    credits INTEGER,
    role TEXT,
    plan TEXT,
    registration_date TEXT,
    expiration_date TEXT,
    total_queries INTEGER,
    today_queries INTEGER,
    last_query_time TEXT,
    referral_code TEXT,
    referred_by BIGINT,
    is_active BOOLEAN
);
''')
pg_cursor.execute('''
CREATE TABLE IF NOT EXISTS reniec_data (
    dni TEXT PRIMARY KEY,
    apellido_paterno TEXT,
    apellido_materno TEXT,
    nombres TEXT,
    fecha_nacimiento TEXT,
    fch_inscripcion TEXT,
    fch_emision TEXT,
    fch_caducidad TEXT,
    ubigeo_nac TEXT,
    ubigeo_dir TEXT,
    direccion TEXT,
    sexo TEXT,
    estado_civil TEXT,
    dig_ruc TEXT,
    madre TEXT,
    padre TEXT
);
''')
# Si tienes más tablas, repite el proceso aquí...

# MIGRAR USUARIOS
sqlite_cursor.execute("SELECT * FROM users")
for row in sqlite_cursor.fetchall():
    # Convierte el último campo (is_active) a booleano
    row = list(row)
    if isinstance(row[-1], int):
        row[-1] = bool(row[-1])
    pg_cursor.execute("""
        INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING
    """, row)