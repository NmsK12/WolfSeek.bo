import logging
import datetime
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from database import Database
from config import BOT_TOKEN, CREDIT_COST_PER_QUERY, ANTI_SPAM_DELAY, INITIAL_CREDITS

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inicializar base de datos
db = Database()

class RENIECBot:
    def __init__(self):
        self.db = db
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        user = update.effective_user
        user_id = user.id
        
        # Verificar si el usuario ya existe
        existing_user = self.db.get_user(user_id)
        
        if not existing_user:
            # Crear nuevo usuario
            self.db.create_user(
                user_id=user_id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            
            welcome_message = f"""
[✅] Hola {user.first_name or user.username},

Te has registrado correctamente y se te han otorgado {INITIAL_CREDITS} monedas.

¡Bienvenido y disfruta de nuestro bot!

[📋] Comandos disponibles:
/dni <DNI> - Consultar Por Medio De DNI
/register - Registrarse (ya estás registrado)
/info - Ver tu perfil
/cred <cantidad> - Administrar créditos
/historial - Ver historial de consultas
/girar - Girar la ruleta de premios
            """
        else:
            welcome_message = f"""
[✅] ¡Hola de nuevo {user.first_name or user.username}!

Ya estás registrado en nuestro sistema.

[📋] Comandos disponibles:
/dni <DNI> - Consultar datos completos
/info - Ver tu perfil
/cred <cantidad> - Administrar créditos
/historial - Ver historial de consultas
/girar - Girar la ruleta de premios
            """
        
        await update.message.reply_text(welcome_message)
    
    async def register(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /register"""
        user = update.effective_user
        user_id = user.id
        
        existing_user = self.db.get_user(user_id)
        
        if existing_user:
            await update.message.reply_text("Ya estás registrado en el sistema.")
            return
        
        # Crear nuevo usuario
        self.db.create_user(
            user_id=user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        welcome_message = f"""
[✅] Hola {user.first_name or user.username},

Te has registrado correctamente y se te han otorgado {INITIAL_CREDITS} monedas.

¡Bienvenido y disfruta de nuestro bot!
        """
        
        await update.message.reply_text(welcome_message)
    
    async def dni_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /dni"""
        user = update.effective_user
        user_id = user.id
        
        # Verificar si el usuario está registrado
        user_data = self.db.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ Primero debes registrarte. Usa /register")
            return
        
        # Verificar argumentos
        if not context.args:
            await update.message.reply_text("❌ Uso: /dni <DNI>\nEjemplo: /dni 12345678")
            return
        
        dni = context.args[0]
        
        # Validar formato DNI
        if not dni.isdigit() or len(dni) != 8:
            await update.message.reply_text("❌ El DNI debe tener 8 dígitos numéricos.")
            return
        
        # Verificar créditos
        if user_data[4] < CREDIT_COST_PER_QUERY:
            await update.message.reply_text("❌ No tienes suficientes créditos. Necesitas 1 crédito por consulta.")
            return
        
        # Verificar anti-spam
        if user_data[11]:  # last_query_time
            last_query = datetime.datetime.strptime(user_data[11], "%Y-%m-%d %H:%M:%S")
            time_diff = (datetime.datetime.now() - last_query).total_seconds()
            if time_diff < ANTI_SPAM_DELAY:
                remaining = int(ANTI_SPAM_DELAY - time_diff)
                await update.message.reply_text(f"⏰ Espera {remaining} segundos antes de hacer otra consulta.")
                return
        
        # Buscar datos
        dni_data = self.db.get_dni_data(dni)
        if not dni_data:
            await update.message.reply_text("❌ DNI no encontrado en la base de datos.")
            return
        
        # Descontar crédito
        new_credits = user_data[4] - CREDIT_COST_PER_QUERY
        self.db.update_credits(user_id, new_credits)
        
        # Registrar consulta
        self.db.log_query(user_id, dni, "DNI_FULL")
        
        # Formatear respuesta
        response = f"""
[#NOISEv1.3_BOT] ➾ RENIEC ONLINE - GRATIS

DOCUMENTO ➾ {dni_data[0]} - 1
NOMBRES ➾ {dni_data[1]}
APELLIDOS ➾ {dni_data[2]}
GENERO ➾ {dni_data[5]}

[🎂] NACIMIENTO

FECHA NACIMIENTO ➾ {dni_data[3]}
EDAD ➾ {dni_data[4]} AÑOS
PADRE ➾ {dni_data[6]}
MADRE ➾ {dni_data[7]}

[🏠] DOMICILIO

DEPARTAMENTO ➾ {dni_data[8]}
PROVINCIA ➾ {dni_data[9]}
DISTRITO ➾ {dni_data[10]}
DIRECCION ➾ {dni_data[11]}

🔎 ¿Necesitas más información?
Utiliza el comando /dni para acceder a datos completos y detallados.

[⚡] ESTADO DE CUENTA

CREDITOS ➾ {new_credits} - 7838557493
USUARIO ➾ {user_data[1] or user_data[2] or 'Usuario'}
        """
        
        await update.message.reply_text(response)
    
    async def dni_preview(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /dnix (previsualización)"""
        user = update.effective_user
        user_id = user.id
        
        # Verificar si el usuario está registrado
        user_data = self.db.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ Primero debes registrarte. Usa /register")
            return
        
        # Verificar argumentos
        if not context.args:
            await update.message.reply_text("❌ Uso: /dnix <DNI>\nEjemplo: /dnix 12345678")
            return
        
        dni = context.args[0]
        
        # Validar formato DNI
        if not dni.isdigit() or len(dni) != 8:
            await update.message.reply_text("❌ El DNI debe tener 8 dígitos numéricos.")
            return
        
        # Buscar datos (sin descontar créditos)
        dni_data = self.db.get_dni_data(dni)
        if not dni_data:
            await update.message.reply_text("❌ DNI no encontrado en la base de datos.")
            return
        
        # Formatear respuesta de previsualización
        response = f"""
[#NOISEv1.3_BOT] ➾ RENIEC NOMBRES - GRATIS

DNI ➾ {dni_data[0]}
NOMBRES ➾ {dni_data[1]}
APELLIDOS ➾ {dni_data[2]}
EDAD ➾ {dni_data[4]} años

➾ Ahora puedes previsualizar la foto de una coincidencia antes de usar /dni

[⚡] ESTADO DE CUENTA

CREDITOS ➾ {user_data[4]} - 7838557493
USUARIO ➾ {user_data[1] or user_data[2] or 'Usuario'}

{dni_data[0]}

/dnix {dni_data[0]}
/register
        """
        
        await update.message.reply_text(response)
    
    async def info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /info"""
        user = update.effective_user
        user_id = user.id
        
        # Verificar si el usuario está registrado
        user_data = self.db.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ Primero debes registrarte. Usa /register")
            return
        
        # Calcular días restantes
        expiration_date = datetime.datetime.strptime(user_data[8], "%Y-%m-%d")
        days_remaining = (expiration_date - datetime.datetime.now()).days
        days_remaining = max(0, days_remaining)
        
        # Formatear respuesta
        response = f"""
[#NOISEv1.3_BOT] ➾ ME - PERFIL

PERFIL DE ➾ {user_data[2]} {user_data[3] or ''}

INFORMACIÓN PERSONAL

[🆔] ID ➾ {user_data[0]}
[👨🏻‍💻] USER ➾ @{user_data[1] or 'Sin username'}
[🚨] ESTADO ➾ LIBRE
[📅] F. REGISTRO ➾ {user_data[7]}

ESTADO DE CUENTA

[〽️] ROL ➾ {user_data[5]}
[📈] PLAN ➾ {user_data[6]}
[⏱] ANTI-SPAM ➾ {ANTI_SPAM_DELAY}'
[💰] CREDITOS ➾ {user_data[4]}
[📅] DÍAS RESTANTES ➾ {days_remaining}
[📅] F. EXPIRACION ➾ {user_data[8]}

USO DEL SERVICIO

[📊] CONSULTAS ➾ {user_data[9]}
[📅] CONSULTAS DE HOY ➾ {user_data[10]}
[🔎] HISTORIAL DE CMDS ➾ /historial

PROGRAMA DE REFERIDOS

[👥] REFERIDOS ➾ 0
[🔗] TU ENLACE ➾
https://t.me/wolfseek_bot?start={user_data[0]}
[🎟] INFO DE REFERIDOS ➾ /referido

SERVICIOS Y OPCIONES

[🛒] Verifica tus compras ➾ /compras
[🎰] Gira la ruleta ➾ /girar
        """
        
        await update.message.reply_text(response)
    
    async def credits(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /cred"""
        user = update.effective_user
        user_id = user.id
        
        # Verificar si el usuario está registrado
        user_data = self.db.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ Primero debes registrarte. Usa /register")
            return
        
        # Verificar argumentos
        if not context.args:
            await update.message.reply_text(f"💰 Tus créditos actuales: {user_data[4]}")
            return
        
        try:
            amount = int(context.args[0])
            if amount <= 0:
                await update.message.reply_text("❌ La cantidad debe ser mayor a 0.")
                return
            
            # Actualizar créditos
            new_credits = user_data[4] + amount
            self.db.update_credits(user_id, new_credits)
            
            await update.message.reply_text(f"✅ Créditos actualizados: {new_credits}")
            
        except ValueError:
            await update.message.reply_text("❌ La cantidad debe ser un número válido.")
    
    async def historial(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /historial"""
        user = update.effective_user
        user_id = user.id
        
        # Verificar si el usuario está registrado
        user_data = self.db.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ Primero debes registrarte. Usa /register")
            return
        
        # Obtener historial
        queries = self.db.get_user_queries(user_id)
        
        if not queries:
            await update.message.reply_text("📋 No tienes consultas en tu historial.")
            return
        
        response = "📋 HISTORIAL DE CONSULTAS:\n\n"
        for i, query in enumerate(queries[:10], 1):
            response += f"{i}. DNI: {query[2]} - {query[3]} - {query[4]}\n"
        
        await update.message.reply_text(response)
    
    async def girar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /girar (ruleta)"""
        user = update.effective_user
        user_id = user.id
        
        # Verificar si el usuario está registrado
        user_data = self.db.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ Primero debes registrarte. Usa /register")
            return
        
        # Simular ruleta
        import random
        prizes = [
            ("🎉 ¡FELICIDADES! Ganaste 5 créditos", 5),
            ("🎊 ¡EXCELENTE! Ganaste 3 créditos", 3),
            ("🎯 ¡MUY BIEN! Ganaste 2 créditos", 2),
            ("🎪 ¡BUENO! Ganaste 1 crédito", 1),
            ("😔 ¡Ups! No ganaste nada esta vez", 0),
            ("🎲 ¡Casi! Ganaste 1 crédito", 1)
        ]
        
        prize_text, prize_amount = random.choice(prizes)
        
        # Actualizar créditos
        new_credits = user_data[4] + prize_amount
        self.db.update_credits(user_id, new_credits)
        
        response = f"""
🎰 RUEDA DE LA FORTUNA

{prize_text}

💰 Créditos actuales: {new_credits}

¡Vuelve a girar mañana!
        """
        
        await update.message.reply_text(response)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes que no son comandos"""
        await update.message.reply_text("""
🤖 Bot de Consulta RENIEC

Comandos disponibles:
/dni <DNI> - Consultar datos completos
/dnix <DNI> - Previsualizar datos
/register - Registrarse
/info - Ver perfil
/cred <cantidad> - Administrar créditos
/historial - Ver historial
/girar - Girar ruleta

Para empezar, usa /register
        """)

def main():
    """Función principal"""
    # Crear aplicación
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Crear instancia del bot
    bot = RENIECBot()
    
    # Agregar handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("register", bot.register))
    application.add_handler(CommandHandler("dni", bot.dni_query))
    application.add_handler(CommandHandler("dnix", bot.dni_preview))
    application.add_handler(CommandHandler("info", bot.info))
    application.add_handler(CommandHandler("cred", bot.credits))
    application.add_handler(CommandHandler("historial", bot.historial))
    application.add_handler(CommandHandler("girar", bot.girar))
    
    # Handler para mensajes que no son comandos
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Iniciar bot
    print("🤖 Bot iniciado...")
    application.run_polling()

if __name__ == '__main__':
    main() 