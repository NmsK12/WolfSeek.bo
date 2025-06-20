import sqlite3
import csv

# Nombres de archivo
TXT_FILE = 'reniec.txt'
DB_FILE = 'wolfseek_bot.db'  # Cambiado para coincidir con config.py

# Conexión a SQLite
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Crear la tabla reniec_data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reniec_data (
        dni TEXT PRIMARY KEY,
        ap_pat TEXT,
        ap_mat TEXT,
        nombres TEXT,
        fecha_nac TEXT,
        fch_inscripcion TEXT,
        fch_emision TEXT,
        fch_caducidad TEXT,
        ubigeo_nac TEXT,
        ubigeo_dir TEXT,
        direccion TEXT,
        sexo TEXT,
        est_civil TEXT,
        dig_ruc TEXT,
        madre TEXT,
        padre TEXT
    )
''')

# Insertar línea por línea para evitar MemoryError
def insertar_linea(row):
    cursor.execute('''
        INSERT OR IGNORE INTO reniec_data (
            dni, ap_pat, ap_mat, nombres, fecha_nac, fch_inscripcion, fch_emision, fch_caducidad,
            ubigeo_nac, ubigeo_dir, direccion, sexo, est_civil, dig_ruc, madre, padre
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['DNI'], row['AP_PAT'], row['AP_MAT'], row['NOMBRES'], row['FECHA_NAC'],
        row['FCH_INSCRIPCION'], row['FCH_EMISION'], row['FCH_CADUCIDAD'],
        row['UBIGEO_NAC'], row['UBIGEO_DIR'], row['DIRECCION'], row['SEXO'],
        row['EST_CIVIL'], row['DIG_RUC'], row['MADRE'], row['PADRE']
    ))

with open(TXT_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='|')
    for i, row in enumerate(reader, 1):
        insertar_linea(row)
        if i % 10000 == 0:
            conn.commit()  # Guardar cada 10,000 registros para eficiencia
            print(f"{i} registros insertados...")

conn.commit()
conn.close()
print("¡Importación completada!") 