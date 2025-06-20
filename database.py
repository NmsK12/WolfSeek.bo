import psycopg2
import datetime
import random
from config import INITIAL_CREDITS

POSTGRES_URL = "postgresql://postgres:cYSeddxBzAMpqIFSvWtSvjhUqwdfqkJc@shinkansen.proxy.rlwy.net:28743/railway"

class Database:
    def __init__(self):
        self.db_url = POSTGRES_URL
        # Ya no se inicializan tablas aquí, se asume que existen en PostgreSQL

    def get_user(self, user_id):
        """Obtener información de un usuario"""
        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    def create_user(self, user_id, username, first_name, last_name, referred_by=None):
        """Crear un nuevo usuario"""
        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()
        registration_date = datetime.datetime.now().strftime("%Y-%m-%d")
        expiration_date = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        referral_code = f"REF{user_id}"
        cursor.execute('''
            INSERT INTO users 
            (user_id, username, first_name, last_name, credits, registration_date, expiration_date, referral_code, referred_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING
        ''', (user_id, username, first_name, last_name, INITIAL_CREDITS, registration_date, expiration_date, referral_code, referred_by))
        # Si fue referido, dar créditos al referidor
        if referred_by:
            cursor.execute("UPDATE users SET credits = credits + 2 WHERE user_id = %s", (referred_by,))
        conn.commit()
        cursor.close()
        conn.close()

    def update_credits(self, user_id, credits):
        """Actualizar créditos de un usuario"""
        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET credits = %s WHERE user_id = %s", (credits, user_id))
        conn.commit()
        cursor.close()
        conn.close()

    def get_dni_data(self, dni):
        """Obtener datos de un DNI desde la tabla reniec_data"""
        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reniec_data WHERE dni = %s", (dni,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data

    def log_query(self, user_id, dni, query_type):
        """Registrar una consulta"""
        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()
        query_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO queries (user_id, dni, query_type, query_date)
            VALUES (%s, %s, %s, %s)
        ''', (user_id, dni, query_type, query_date))
        # Actualizar estadísticas del usuario
        cursor.execute("UPDATE users SET total_queries = total_queries + 1, today_queries = today_queries + 1, last_query_time = %s WHERE user_id = %s", (query_date, user_id))
        conn.commit()
        cursor.close()
        conn.close()

    def get_user_queries(self, user_id):
        """Obtener historial de consultas de un usuario"""
        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM queries WHERE user_id = %s ORDER BY query_date DESC LIMIT 10", (user_id,))
        queries = cursor.fetchall()
        cursor.close()
        conn.close()
        return queries

    def reset_daily_queries(self):
        """Resetear consultas diarias (ejecutar diariamente)"""
        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET today_queries = 0")
        conn.commit()
        cursor.close()
        conn.close()

    def registrar_recarga(self, user_id, cantidad, admin_id=None):
        """Registrar una recarga de créditos"""
        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO recargas (user_id, cantidad, fecha, admin_id)
            VALUES (%s, %s, %s, %s)
        ''', (user_id, cantidad, fecha, admin_id))
        conn.commit()
        cursor.close()
        conn.close()

    def obtener_recargas(self, user_id, limit=10):
        """Obtener historial de recargas de un usuario"""
        conn = psycopg2.connect(self.db_url)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT cantidad, fecha, admin_id FROM recargas WHERE user_id = %s ORDER BY fecha DESC LIMIT %s
        ''', (user_id, limit))
        recargas = cursor.fetchall()
        cursor.close()
        conn.close()
        return recargas 