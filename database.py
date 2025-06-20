import sqlite3
import datetime
import random
from config import DATABASE_NAME, INITIAL_CREDITS

class Database:
    def __init__(self):
        self.db_name = DATABASE_NAME
        self.init_database()
        # self.populate_sample_data()  # Eliminado para no poblar datos de ejemplo
    
    def init_database(self):
        """Inicializar la base de datos con todas las tablas necesarias excepto la tabla de datos de ejemplo"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                credits INTEGER DEFAULT 5,
                role TEXT DEFAULT 'FREE',
                plan TEXT DEFAULT 'FREE',
                registration_date TEXT,
                expiration_date TEXT,
                total_queries INTEGER DEFAULT 0,
                today_queries INTEGER DEFAULT 0,
                last_query_time TEXT,
                referral_code TEXT,
                referred_by INTEGER,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Tabla de consultas (historial)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                dni TEXT,
                query_type TEXT,
                query_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Tabla de historial de recargas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recargas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                cantidad INTEGER,
                fecha TEXT,
                admin_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id):
        """Obtener información de un usuario"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def create_user(self, user_id, username, first_name, last_name, referred_by=None):
        """Crear un nuevo usuario"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        registration_date = datetime.datetime.now().strftime("%Y-%m-%d")
        expiration_date = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        referral_code = f"REF{user_id}"
        
        cursor.execute('''
            INSERT INTO users 
            (user_id, username, first_name, last_name, credits, registration_date, expiration_date, referral_code, referred_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, INITIAL_CREDITS, registration_date, expiration_date, referral_code, referred_by))
        
        # Si fue referido, dar créditos al referidor
        if referred_by:
            cursor.execute("UPDATE users SET credits = credits + 2 WHERE user_id = ?", (referred_by,))
        
        conn.commit()
        conn.close()
    
    def update_credits(self, user_id, credits):
        """Actualizar créditos de un usuario"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET credits = ? WHERE user_id = ?", (credits, user_id))
        conn.commit()
        conn.close()
    
    def get_dni_data(self, dni):
        """Obtener datos de un DNI desde la tabla reniec_data"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reniec_data WHERE dni = ?", (dni,))
        data = cursor.fetchone()
        conn.close()
        return data
    
    def log_query(self, user_id, dni, query_type):
        """Registrar una consulta"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO queries (user_id, dni, query_type, query_date)
            VALUES (?, ?, ?, ?)
        ''', (user_id, dni, query_type, query_date))
        
        # Actualizar estadísticas del usuario
        cursor.execute("UPDATE users SET total_queries = total_queries + 1, today_queries = today_queries + 1, last_query_time = ? WHERE user_id = ?", (query_date, user_id))
        
        conn.commit()
        conn.close()
    
    def get_user_queries(self, user_id):
        """Obtener historial de consultas de un usuario"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM queries WHERE user_id = ? ORDER BY query_date DESC LIMIT 10", (user_id,))
        queries = cursor.fetchall()
        conn.close()
        return queries
    
    def reset_daily_queries(self):
        """Resetear consultas diarias (ejecutar diariamente)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET today_queries = 0")
        conn.commit()
        conn.close()
    
    def get_user_history(self, user_id, limit=10):
        """Obtener historial de consultas del usuario"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT query_param, command_type, timestamp 
                FROM query_history 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (user_id, limit))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting user history: {e}")
            return []
    
    def registrar_recarga(self, user_id, cantidad, admin_id=None):
        """Registrar una recarga de créditos"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO recargas (user_id, cantidad, fecha, admin_id)
            VALUES (?, ?, ?, ?)
        ''', (user_id, cantidad, fecha, admin_id))
        conn.commit()
        conn.close()

    def obtener_recargas(self, user_id, limit=10):
        """Obtener historial de recargas de un usuario"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT cantidad, fecha, admin_id FROM recargas WHERE user_id = ? ORDER BY fecha DESC LIMIT ?
        ''', (user_id, limit))
        recargas = cursor.fetchall()
        conn.close()
        return recargas 