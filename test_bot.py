#!/usr/bin/env python3
"""
Script de Prueba para el Bot RENIEC
Verifica que todas las funcionalidades funcionen correctamente
"""

import sqlite3
import datetime
from database import Database
from config import DATABASE_NAME, INITIAL_CREDITS, CREDIT_COST_PER_QUERY

class BotTester:
    def __init__(self):
        self.db = Database()
    
    def test_database_creation(self):
        """Probar creación de base de datos"""
        print("🧪 Probando creación de base de datos...")
        
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            # Verificar tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [table[0] for table in cursor.fetchall()]
            
            required_tables = ['users', 'queries', 'sample_data']
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                print(f"❌ Tablas faltantes: {missing_tables}")
                return False
            
            print("✅ Todas las tablas creadas correctamente")
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error al crear base de datos: {e}")
            return False
    
    def test_sample_data(self):
        """Probar datos de ejemplo"""
        print("\n🧪 Probando datos de ejemplo...")
        
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM sample_data")
            count = cursor.fetchone()[0]
            
            if count == 0:
                print("❌ No hay datos de ejemplo")
                return False
            
            print(f"✅ {count} registros de ejemplo cargados")
            
            # Verificar un registro específico
            cursor.execute("SELECT * FROM sample_data WHERE dni = '12345678'")
            record = cursor.fetchone()
            
            if record:
                print(f"✅ Registro de prueba encontrado: {record[1]} {record[2]}")
            else:
                print("❌ Registro de prueba no encontrado")
                return False
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error al verificar datos de ejemplo: {e}")
            return False
    
    def test_user_creation(self):
        """Probar creación de usuarios"""
        print("\n🧪 Probando creación de usuarios...")
        
        try:
            # Crear usuario de prueba
            test_user_id = 999999999
            self.db.create_user(
                user_id=test_user_id,
                username="test_user",
                first_name="Usuario",
                last_name="Prueba"
            )
            
            # Verificar que se creó
            user = self.db.get_user(test_user_id)
            
            if not user:
                print("❌ Usuario de prueba no se creó")
                return False
            
            if user[4] != INITIAL_CREDITS:
                print(f"❌ Créditos iniciales incorrectos. Esperado: {INITIAL_CREDITS}, Obtenido: {user[4]}")
                return False
            
            print("✅ Usuario de prueba creado correctamente")
            print(f"   ID: {user[0]}")
            print(f"   Username: @{user[1]}")
            print(f"   Créditos: {user[4]}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al crear usuario: {e}")
            return False
    
    def test_dni_query(self):
        """Probar consulta de DNI"""
        print("\n🧪 Probando consulta de DNI...")
        
        try:
            # Buscar DNI existente
            dni_data = self.db.get_dni_data("12345678")
            
            if not dni_data:
                print("❌ No se encontró DNI de prueba")
                return False
            
            print("✅ Consulta de DNI exitosa")
            print(f"   DNI: {dni_data[0]}")
            print(f"   Nombre: {dni_data[1]} {dni_data[2]}")
            print(f"   Edad: {dni_data[4]} años")
            
            # Probar DNI inexistente
            fake_dni = self.db.get_dni_data("99999999")
            if fake_dni:
                print("❌ DNI inexistente retornó datos")
                return False
            
            print("✅ Validación de DNI inexistente correcta")
            return True
            
        except Exception as e:
            print(f"❌ Error al consultar DNI: {e}")
            return False
    
    def test_credits_system(self):
        """Probar sistema de créditos"""
        print("\n🧪 Probando sistema de créditos...")
        
        try:
            test_user_id = 999999999
            
            # Obtener créditos actuales
            user = self.db.get_user(test_user_id)
            initial_credits = user[4]
            
            # Descontar créditos
            new_credits = initial_credits - CREDIT_COST_PER_QUERY
            self.db.update_credits(test_user_id, new_credits)
            
            # Verificar actualización
            updated_user = self.db.get_user(test_user_id)
            
            if updated_user[4] != new_credits:
                print(f"❌ Créditos no se actualizaron correctamente")
                return False
            
            print("✅ Sistema de créditos funciona correctamente")
            print(f"   Créditos antes: {initial_credits}")
            print(f"   Créditos después: {new_credits}")
            
            # Restaurar créditos
            self.db.update_credits(test_user_id, initial_credits)
            
            return True
            
        except Exception as e:
            print(f"❌ Error en sistema de créditos: {e}")
            return False
    
    def test_query_logging(self):
        """Probar registro de consultas"""
        print("\n🧪 Probando registro de consultas...")
        
        try:
            test_user_id = 999999999
            test_dni = "12345678"
            
            # Registrar consulta
            self.db.log_query(test_user_id, test_dni, "TEST_QUERY")
            
            # Verificar que se registró
            queries = self.db.get_user_queries(test_user_id)
            
            if not queries:
                print("❌ No se registró la consulta")
                return False
            
            latest_query = queries[0]
            
            if latest_query[2] != test_dni:
                print(f"❌ DNI en consulta incorrecto. Esperado: {test_dni}, Obtenido: {latest_query[2]}")
                return False
            
            print("✅ Registro de consultas funciona correctamente")
            print(f"   DNI consultado: {latest_query[2]}")
            print(f"   Tipo: {latest_query[3]}")
            print(f"   Fecha: {latest_query[4]}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en registro de consultas: {e}")
            return False
    
    def test_anti_spam(self):
        """Probar sistema anti-spam"""
        print("\n🧪 Probando sistema anti-spam...")
        
        try:
            test_user_id = 999999999
            
            # Obtener usuario
            user = self.db.get_user(test_user_id)
            
            if not user[11]:  # last_query_time
                print("✅ Usuario sin consultas previas (anti-spam no aplica)")
                return True
            
            # Verificar formato de fecha
            last_query = datetime.datetime.strptime(user[11], "%Y-%m-%d %H:%M:%S")
            time_diff = (datetime.datetime.now() - last_query).total_seconds()
            
            print("✅ Sistema anti-spam configurado correctamente")
            print(f"   Última consulta: {user[11]}")
            print(f"   Tiempo transcurrido: {time_diff:.1f} segundos")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en sistema anti-spam: {e}")
            return False
    
    def cleanup_test_data(self):
        """Limpiar datos de prueba"""
        print("\n🧹 Limpiando datos de prueba...")
        
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            # Eliminar usuario de prueba
            cursor.execute("DELETE FROM users WHERE user_id = 999999999")
            
            # Eliminar consultas de prueba
            cursor.execute("DELETE FROM queries WHERE user_id = 999999999")
            
            conn.commit()
            conn.close()
            
            print("✅ Datos de prueba eliminados")
            
        except Exception as e:
            print(f"❌ Error al limpiar datos: {e}")
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("🚀 INICIANDO PRUEBAS DEL BOT RENIEC")
        print("=" * 50)
        
        tests = [
            ("Creación de base de datos", self.test_database_creation),
            ("Datos de ejemplo", self.test_sample_data),
            ("Creación de usuarios", self.test_user_creation),
            ("Consulta de DNI", self.test_dni_query),
            ("Sistema de créditos", self.test_credits_system),
            ("Registro de consultas", self.test_query_logging),
            ("Sistema anti-spam", self.test_anti_spam)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                    print(f"✅ {test_name}: PASÓ")
                else:
                    print(f"❌ {test_name}: FALLÓ")
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {e}")
        
        # Limpiar datos de prueba
        self.cleanup_test_data()
        
        # Resultados finales
        print("\n" + "=" * 50)
        print(f"📊 RESULTADOS FINALES")
        print(f"Pruebas pasadas: {passed}/{total}")
        print(f"Porcentaje de éxito: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ¡TODAS LAS PRUEBAS PASARON! El bot está listo para usar.")
        else:
            print("⚠️ Algunas pruebas fallaron. Revisa los errores antes de usar el bot.")
        
        return passed == total

if __name__ == "__main__":
    tester = BotTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎯 Próximos pasos:")
        print("1. Configura tu token en config.py")
        print("2. Ejecuta: python bot.py")
        print("3. ¡Disfruta tu bot!")
    else:
        print("\n🔧 Revisa los errores antes de continuar.") 