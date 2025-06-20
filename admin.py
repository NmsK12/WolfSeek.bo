#!/usr/bin/env python3
"""
Script de Administración para el Bot RENIEC
Permite gestionar usuarios, créditos y ver estadísticas
"""

import sqlite3
import datetime
from config import DATABASE_NAME

class AdminPanel:
    def __init__(self):
        self.db_name = DATABASE_NAME
    
    def show_menu(self):
        """Mostrar menú principal"""
        print("""
🤖 PANEL DE ADMINISTRACIÓN - BOT RENIEC
========================================

1. Ver estadísticas generales
2. Listar usuarios
3. Buscar usuario por ID
4. Agregar créditos a usuario
5. Ver historial de consultas
6. Agregar datos de ejemplo
7. Resetear consultas diarias
8. Salir

Selecciona una opción (1-8): """)
    
    def get_stats(self):
        """Obtener estadísticas generales"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Total de usuarios
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        # Usuarios activos hoy
        cursor.execute("SELECT COUNT(*) FROM users WHERE today_queries > 0")
        active_today = cursor.fetchone()[0]
        
        # Total de consultas
        cursor.execute("SELECT COUNT(*) FROM queries")
        total_queries = cursor.fetchone()[0]
        
        # Consultas de hoy
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor.execute("SELECT COUNT(*) FROM queries WHERE DATE(query_date) = ?", (today,))
        queries_today = cursor.fetchone()[0]
        
        # Total de créditos en el sistema
        cursor.execute("SELECT SUM(credits) FROM users")
        total_credits = cursor.fetchone()[0] or 0
        
        conn.close()
        
        print(f"""
📊 ESTADÍSTICAS GENERALES
=========================

👥 Usuarios totales: {total_users}
🟢 Usuarios activos hoy: {active_today}
🔍 Total de consultas: {total_queries}
📅 Consultas de hoy: {queries_today}
💰 Total de créditos en el sistema: {total_credits}
        """)
    
    def list_users(self, limit=10):
        """Listar usuarios"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id, username, first_name, last_name, credits, 
                   total_queries, today_queries, registration_date
            FROM users 
            ORDER BY registration_date DESC 
            LIMIT ?
        """, (limit,))
        
        users = cursor.fetchall()
        conn.close()
        
        print(f"\n👥 ÚLTIMOS {len(users)} USUARIOS REGISTRADOS")
        print("=" * 60)
        
        for user in users:
            print(f"""
ID: {user[0]}
Username: @{user[1] or 'Sin username'}
Nombre: {user[2]} {user[3] or ''}
Créditos: {user[4]}
Consultas totales: {user[5]}
Consultas hoy: {user[6]}
Registro: {user[7]}
{'-' * 40}""")
    
    def find_user(self, user_id):
        """Buscar usuario por ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ Usuario con ID {user_id} no encontrado.")
            conn.close()
            return
        
        print(f"""
👤 INFORMACIÓN DEL USUARIO
==========================

ID: {user[0]}
Username: @{user[1] or 'Sin username'}
Nombre: {user[2]} {user[3] or ''}
Créditos: {user[4]}
Rol: {user[5]}
Plan: {user[6]}
Fecha de registro: {user[7]}
Fecha de expiración: {user[8]}
Consultas totales: {user[9]}
Consultas hoy: {user[10]}
Última consulta: {user[11] or 'Nunca'}
Código de referido: {user[12]}
Referido por: {user[13] or 'Nadie'}
        """)
        
        conn.close()
    
    def add_credits(self, user_id, amount):
        """Agregar créditos a un usuario"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Verificar si el usuario existe
        cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        
        if not result:
            print(f"❌ Usuario con ID {user_id} no encontrado.")
            conn.close()
            return
        
        current_credits = result[0]
        new_credits = current_credits + amount
        
        cursor.execute("UPDATE users SET credits = ? WHERE user_id = ?", (new_credits, user_id))
        conn.commit()
        conn.close()
        
        print(f"✅ Créditos actualizados para usuario {user_id}")
        print(f"   Antes: {current_credits}")
        print(f"   Después: {new_credits}")
        print(f"   Agregados: +{amount}")
    
    def show_query_history(self, user_id=None, limit=10):
        """Mostrar historial de consultas"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute("""
                SELECT q.dni, q.query_type, q.query_date, u.username
                FROM queries q
                JOIN users u ON q.user_id = u.user_id
                WHERE q.user_id = ?
                ORDER BY q.query_date DESC
                LIMIT ?
            """, (user_id, limit))
        else:
            cursor.execute("""
                SELECT q.dni, q.query_type, q.query_date, u.username
                FROM queries q
                JOIN users u ON q.user_id = u.user_id
                ORDER BY q.query_date DESC
                LIMIT ?
            """, (limit,))
        
        queries = cursor.fetchall()
        conn.close()
        
        if user_id:
            print(f"\n📋 HISTORIAL DE CONSULTAS - USUARIO {user_id}")
        else:
            print(f"\n📋 ÚLTIMAS {len(queries)} CONSULTAS")
        
        print("=" * 50)
        
        for query in queries:
            print(f"""
DNI: {query[0]}
Tipo: {query[1]}
Fecha: {query[2]}
Usuario: @{query[3] or 'Sin username'}
{'-' * 30}""")
    
    def add_sample_data(self):
        """Agregar más datos de ejemplo"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Datos adicionales de ejemplo
        additional_data = [
            ("11111111", "ALEJANDRO MIGUEL", "CASTILLO RIVERA", "03/12/1983", 40, "MASCULINO", "MIGUEL CASTILLO", "ROSA RIVERA", "LIMA", "LIMA", "CHORRILLOS", "AV. HUAYLAS 456"),
            ("22222222", "VANESSA PATRICIA", "SOTO MENDOZA", "19/05/1996", 27, "FEMENINO", "PATRICIO SOTO", "GLORIA MENDOZA", "LIMA", "LIMA", "VILLA EL SALVADOR", "CALLE LOS ROSALES 789"),
            ("33333333", "RICARDO ALBERTO", "VARGAS HUAMAN", "07/09/1981", 42, "MASCULINO", "ALBERTO VARGAS", "MARIA HUAMAN", "LIMA", "LIMA", "SAN JUAN DE MIRAFLORES", "AV. PACHACUTEC 321"),
            ("44444444", "DIANA CAROLINA", "QUISPE TORRES", "25/11/1993", 30, "FEMENINO", "CARLOS QUISPE", "ANA TORRES", "LIMA", "LIMA", "VILLA MARIA DEL TRIUNFO", "CALLE LOS JAZMINES 654"),
            ("55555555", "MARTIN EDUARDO", "ZAPATA FLORES", "14/02/1987", 36, "MASCULINO", "EDUARDO ZAPATA", "LUCIA FLORES", "LIMA", "LIMA", "SAN JUAN DE LURIGANCHO", "AV. GRAN CHIMU 987")
        ]
        
        try:
            cursor.executemany('''
                INSERT INTO sample_data 
                (dni, nombres, apellidos, fecha_nacimiento, edad, genero, padre, madre, departamento, provincia, distrito, direccion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', additional_data)
            
            conn.commit()
            print(f"✅ Se agregaron {len(additional_data)} nuevos registros de ejemplo.")
            
        except sqlite3.IntegrityError:
            print("⚠️ Algunos registros ya existen en la base de datos.")
        
        conn.close()
    
    def reset_daily_queries(self):
        """Resetear consultas diarias"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE users SET today_queries = 0")
        conn.commit()
        conn.close()
        
        print("✅ Consultas diarias reseteadas para todos los usuarios.")
    
    def run(self):
        """Ejecutar el panel de administración"""
        while True:
            self.show_menu()
            
            try:
                option = input().strip()
                
                if option == "1":
                    self.get_stats()
                
                elif option == "2":
                    limit = input("Número de usuarios a mostrar (default 10): ").strip()
                    limit = int(limit) if limit.isdigit() else 10
                    self.list_users(limit)
                
                elif option == "3":
                    user_id = input("Ingresa el ID del usuario: ").strip()
                    if user_id.isdigit():
                        self.find_user(int(user_id))
                    else:
                        print("❌ ID debe ser un número.")
                
                elif option == "4":
                    user_id = input("ID del usuario: ").strip()
                    amount = input("Cantidad de créditos a agregar: ").strip()
                    
                    if user_id.isdigit() and amount.isdigit():
                        self.add_credits(int(user_id), int(amount))
                    else:
                        print("❌ ID y cantidad deben ser números.")
                
                elif option == "5":
                    user_id = input("ID del usuario (dejar vacío para todos): ").strip()
                    limit = input("Número de consultas a mostrar (default 10): ").strip()
                    limit = int(limit) if limit.isdigit() else 10
                    
                    if user_id.isdigit():
                        self.show_query_history(int(user_id), limit)
                    else:
                        self.show_query_history(limit=limit)
                
                elif option == "6":
                    self.add_sample_data()
                
                elif option == "7":
                    confirm = input("¿Estás seguro? (s/n): ").strip().lower()
                    if confirm == 's':
                        self.reset_daily_queries()
                    else:
                        print("Operación cancelada.")
                
                elif option == "8":
                    print("👋 ¡Hasta luego!")
                    break
                
                else:
                    print("❌ Opción no válida. Intenta de nuevo.")
                
                input("\nPresiona Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Presiona Enter para continuar...")

if __name__ == "__main__":
    admin = AdminPanel()
    admin.run() 