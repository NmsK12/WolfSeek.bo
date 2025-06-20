import logging
import datetime
import random
import json
import re
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from database import Database
from config import BOT_TOKEN, BOT_NAME, BOT_USERNAME, ADMIN_USERNAME, CREDIT_COST_PER_QUERY, ANTI_SPAM_DELAY, INITIAL_CREDITS, CATEGORIES, REFERRAL_BONUS

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Inicializar base de datos
db = Database()

class WolfSeekBot:
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
⫷ 𝙒𝙀𝙇𝘾𝙊𝙈𝙀, ╰‿╯A҉U҉R҉A҉╰‿╯ | ╰$𝔈𝔑𝔈𝔐ℑ𝔖╯ | T/ ⫸

✦ Bienvenido a 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼
𝘌𝘭 𝘤𝘦𝘯𝘵𝘳𝘰 𝘥𝘰𝘯𝘥𝘦 𝘭𝘢 𝘪𝘯𝘧𝘰𝘳𝘮𝘢𝘤𝘪ó𝘯 𝘴𝘦 𝘷𝘶𝘦𝘭𝘷𝘦 𝘱𝘰𝘥𝘦𝘳.

⟡ 𝐆𝐔𝐈́𝐀 𝐑𝐀́𝐏𝐈𝐃𝐀
⫸ /register — 𝙘𝙧𝙚𝙖 𝙩𝙪 𝙞𝙙𝙚𝙣𝙩𝙞𝙙𝙖𝙙 𝙙𝙞𝙜𝙞𝙩𝙖𝙡
⫸ /cmds — 𝙚𝙭𝙥𝙡𝙤𝙧𝙖 𝙩𝙤𝙙𝙤 𝙡𝙤 𝙦𝙪𝙚 𝙥𝙪𝙚𝙙𝙚𝙨 𝙝𝙖𝙘𝙚𝙧
⫸ /me — 𝙧𝙚𝙫𝙞𝙨𝙖 𝙩𝙪 𝙥𝙚𝙧𝙛𝙞𝙡 𝙮 𝙙𝙖𝙩𝙤𝙨
⫸ /buy — 𝙖𝙘𝙩𝙞𝙫𝙖 𝙩𝙪𝙨 𝙘𝙧é𝙙𝙞𝙩𝙤𝙨

⚠ 𝐃𝐈𝐒𝐂𝐋𝐀𝐈𝐌𝐄𝐑
𝘌𝘭 𝘮𝘢𝘭 𝘶𝘴𝘰 𝘥𝘦 𝘭𝘢 𝘪𝘯𝘧𝘰𝘳𝘮𝘢𝘤𝘪ó𝘯 𝘦𝘴 𝘵𝘢𝘭 𝘳𝘦𝘴𝘱𝘰𝘯𝘢𝘴 𝘲𝘶𝘦 𝘣𝘶𝘴𝘤𝘢𝘯 𝘳𝘢́𝘱𝘪𝘥𝘦𝘻 𝘺 𝘱𝘳𝘦𝘤𝘪𝘴𝘪ó𝘯.

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
        """
        
        # Crear botones de categorías
        keyboard = self.create_category_buttons()
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Enviar con foto del logo
        await self.send_message_with_photo(update, welcome_message, "assets/wolfseek.png", reply_markup)
    
    def create_category_buttons(self):
        """Crear botones de categorías"""
        keyboard = []
        row = []
        
        for i, category in enumerate(CATEGORIES):
            row.append(InlineKeyboardButton(category, callback_data=f"cat_{category}"))
            
            if len(row) == 2:  # 2 botones por fila
                keyboard.append(row)
                row = []
        
        if row:  # Agregar fila incompleta
            keyboard.append(row)
        
        # Agregar botones de utilidad
        keyboard.append([
            InlineKeyboardButton("💰 Comprar Créditos", callback_data="buy_credits"),
            InlineKeyboardButton("👤 Mi Perfil", callback_data="my_profile")
        ])
        
        return keyboard
    
    async def cmds(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /cmds"""
        message = f"""
⟦ 𝙎𝙄𝙎𝙏𝙀𝙈𝘼 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ⟧

✦ 𝙃𝙤𝙡𝙖, ╰‿╯A҉U҉R҉A҉╰‿╯ | ╰$𝔈𝔑𝔈𝔐ℑ𝔖╯ | T/

𝘉𝘪𝘦𝘯𝘷𝘦𝘯𝘪𝘥𝘰 𝘢 𝘶𝘯 𝘴𝘪𝘴𝘵𝘦𝘮𝘢 𝘥𝘦𝘴𝘢𝘳𝘳𝘰𝘭𝘭𝘢𝘥𝘰 𝘱𝘢𝘳𝘢 𝘱𝘦𝘳𝘴𝘰𝘯𝘢𝘴 𝘲𝘶𝘦 𝘣𝘶𝘴𝘤𝘢𝘯 𝘳𝘢́𝘱𝘪𝘥𝘦𝘻 𝘺 𝘱𝘳𝘦𝘤𝘪𝘴𝘪ó𝘯.

⟡ 𝙀𝙭𝙥𝙡𝙤𝙧𝙖 𝙡𝙖𝙨 𝙤𝙥𝙘𝙞𝙤𝙣𝙚𝙨 𝙙𝙞𝙨𝙥𝙤𝙣𝙞𝙗𝙡𝙚𝙨 𝙮 𝙙𝙚𝙨𝙘𝙪𝙗𝙧𝙚 𝙡𝙤 𝙦𝙪𝙚 𝙣𝙚𝙘𝙚𝙨𝙞𝙩𝙖𝙨 𝙚𝙣 𝙘𝙪𝙚𝙨𝙩𝙞𝙤́𝙣 𝙙𝙚 𝙨𝙚𝙜𝙪𝙣𝙙𝙤𝙨.

⫸ 𝙎𝙀𝙇𝙀𝘾𝘾𝙄𝙊𝙉𝘼 𝙐𝙉𝘼 𝙊𝙋𝘾𝙄𝙊́𝙉 𝘿𝙀𝙇 𝙈𝙀𝙉𝙐́ ➾

≋≋≋ [ 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 • 2025 ] ≋≋≋
𝘓𝘢 𝘪𝘯𝘧𝘰𝘳𝘮𝘢𝘤𝘪ó𝘯 𝘦𝘴 𝘱𝘰𝘥𝘦𝘳. 𝘜𝘴𝘢𝘭𝘢 𝘤𝘰𝘯 𝘪𝘯𝘵𝘦𝘭𝘪𝘨𝘦𝘯𝘤𝘪𝘢.
        """
        
        keyboard = self.create_category_buttons()
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup)
    
    async def register(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /register"""
        user = update.effective_user
        user_id = user.id
        
        existing_user = self.db.get_user(user_id)
        
        if existing_user:
            await update.message.reply_text("✅ Ya estás registrado en el sistema.")
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

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
        """
        
        await update.message.reply_text(welcome_message)
    
    async def me(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /me"""
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
        
        # Formatear respuesta con el formato exacto
        response = f"""
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ ME - PERFIL

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
https://t.me/{BOT_USERNAME}?start={user_data[0]}
[🎟] INFO DE REFERIDOS ➾ /referido

SERVICIOS Y OPCIONES

[🛒] Verifica tus compras ➾ /compras
[🎰] Gira la ruleta ➾ /girar
        """
        
        # Enviar con foto del logo
        await self.send_message_with_photo(update, response, "assets/wolfseek.png")
    
    # --- NUEVO: Sistema de roles y privilegios ---
    ROLES_INFO = {
        'FREE': {
            'nombre': '🆓 FREE',
            'creditos': 5,
            'anti_spam': 60,
            'historial': 3,
            'ruleta': '1/día',
            'soporte': 'No',
            'exclusivos': 'No',
            'descripcion': 'Acceso básico, solo comandos esenciales.'
        },
        'BASICO': {
            'nombre': '🔰 BASICO',
            'creditos': 50,
            'anti_spam': 45,
            'historial': 5,
            'ruleta': '2/día',
            'soporte': 'No',
            'exclusivos': 'No',
            'descripcion': 'Más créditos y algunos comandos extra.'
        },
        'STANDARD': {
            'nombre': '⭐ STANDARD',
            'creditos': 100,
            'anti_spam': 15,
            'historial': 10,
            'ruleta': '3/día',
            'soporte': 'Sí',
            'exclusivos': 'No',
            'descripcion': 'Comandos avanzados y soporte.'
        },
        'PREMIUM': {
            'nombre': '💎 PREMIUM',
            'creditos': 200,
            'anti_spam': 5,
            'historial': 20,
            'ruleta': '5/día',
            'soporte': 'Prioridad',
            'exclusivos': 'Sí',
            'descripcion': 'Todos los comandos, soporte prioritario.'
        },
        'VIP': {
            'nombre': '👑 VIP',
            'creditos': 500,
            'anti_spam': 0,
            'historial': 'Ilimitado',
            'ruleta': 'Ilimitado',
            'soporte': 'Directo',
            'exclusivos': 'Sí',
            'descripcion': 'Funciones exclusivas, sin límites.'
        },
        'ADMIN': {
            'nombre': '🏆 ADMIN',
            'creditos': '∞',
            'anti_spam': 0,
            'historial': 'Ilimitado',
            'ruleta': 'Ilimitado',
            'soporte': 'Directo',
            'exclusivos': 'Sí',
            'descripcion': 'Control total y gestión del sistema.'
        }
    }

    def get_user_role(self, user_data):
        if not user_data:
            return 'FREE'
        if user_data[5] == 'ADMIN' or user_data[1] == 'ZekAtwiN12':
            return 'ADMIN'
        return user_data[5].upper() if user_data[5] else 'FREE'

    # --- Mejorar /buy ---
    async def buy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /buy mejorado e interactivo con botón Comprar"""
        user = update.effective_user
        user_id = user.id
        user_data = self.db.get_user(user_id)
        role = self.get_user_role(user_data)

        planes = [
            ('🔰 BASICO', '50 + 20 Créditos ➩ 10 Soles\n100 + 30 Créditos ➩ 15 Soles\n200 + 50 Créditos ➩ 25 Soles\n350 + 80 Créditos ➩ 35 Soles'),
            ('⭐ STANDARD', '500 + 100 Créditos ➩ 40 Soles\n800 + 150 Créditos ➩ 60 Soles\n1000 + 200 Créditos ➩ 75 Soles'),
            ('💎 PREMIUM', '1500 + 200 Créditos ➩ 80 Soles\n2000 + 300 Créditos ➩ 100 Soles\n2800 + 400 Créditos ➩ 130 Soles'),
            ('👑 VIP', '¡Funciones exclusivas! Consultar precio con el admin.')
        ]
        dias = [
            ('🔰 BASICO - NV1', '3 Días ➩ 10 Soles\n7 Días ➩ 15 Soles'),
            ('⭐ STANDARD - NV2', '15 Días ➩ 20 Soles\n30 Días ➩ 35 Soles'),
            ('💎 PREMIUM - NV3', '60 Días ➩ 60 Soles\n90 Días ➩ 90 Soles')
        ]
        mensaje = (
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "✨ <b>PLANES Y TARIFAS</b> ✨\n⚡️ By: @ZekAtwiN12\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "\n💰 <b>PLAN POR CRÉDITOS</b> 💰\n"
        )
        for nombre, detalles in planes:
            mensaje += f"\n⟦{nombre}⟧\n{detalles}\n"
        mensaje += "\n⏳ <b>PLAN POR DÍAS</b> ⏳\n"
        for nombre, detalles in dias:
            mensaje += f"\n⟦{nombre}⟧\n{detalles}\n"
        mensaje += (
            "\n[⚠️] <b>IMPORTANTE</b> ➩ Antes de comprar lee los terminos y condiciones con /rules\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
        )
        mensaje += "\n<b>BENEFICIOS POR ROL:</b>\n"
        for key, info in self.ROLES_INFO.items():
            mensaje += (
                f"\n{info['nombre']}\n• Créditos iniciales: {info['creditos']}\n"
                f"• Anti-spam: {info['anti_spam']}s\n"
                f"• Historial: {info['historial']} consultas\n"
                f"• Ruleta: {info['ruleta']}\n"
                f"• Soporte: {info['soporte']}\n"
                f"• Exclusivos: {info['exclusivos']}\n"
                f"➥ {info['descripcion']}\n"
            )
        mensaje += f"\nTu rol actual: <b>{self.ROLES_INFO[role]['nombre']}</b>\n"
        mensaje += "━━━━━━━━━━━━━━━━━━━━━━━"
        # Botón Comprar
        keyboard = [[InlineKeyboardButton("🛒 Comprar", callback_data="comprar_planes")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.send_message_with_photo(update, mensaje, "assets/wolfseek.png", reply_markup)

    # --- Comando /rules ---
    async def rules(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        reglas = (
            "[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ REGLAS Y CONDICIONES\n\n"
            "1. No compartas tu cuenta ni tus créditos.\n"
            "2. Prohibido el uso para fines ilegales.\n"
            "3. Respeta la privacidad de los datos consultados.\n"
            "4. El mal uso puede llevar a baneo permanente.\n"
            "5. El admin (@ZekAtwiN12) puede suspender cuentas sin previo aviso.\n"
            "6. El bot oficial es #𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1 (@wolfseek_bot).\n"
            "7. Para soporte, contacta solo al admin.\n\n"
            "<b>Lee siempre los términos antes de comprar o usar el bot.</b>\n"
        )
        await self.send_message_with_photo(update, reglas, "assets/wolfseek.png")

    # --- Usar wolfseek.png para todas las respuestas ---
    async def send_message_with_photo(self, update, message, photo_path=None, reply_markup=None):
        """Enviar mensaje con foto (siempre wolfseek.png)"""
        try:
            photo_path = "assets/wolfseek.png"
            if photo_path and os.path.exists(photo_path):
                with open(photo_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption=message,
                        reply_markup=reply_markup,
                        parse_mode='HTML'
                    )
            else:
                await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='HTML')
        except Exception as e:
            await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='HTML')

    # --- Reconocer admin ---
    def is_admin(self, user_data):
        return user_data and (user_data[5] == 'ADMIN' or user_data[1] == 'ZekAtwiN12')

    # --- Ejemplo de comando exclusivo para admin ---
    async def admin_panel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id
        user_data = self.db.get_user(user_id)
        if not self.is_admin(user_data):
            await self.send_message_with_photo(update, "❌ Solo el admin puede usar este comando.")
            return
        await self.send_message_with_photo(update, "[ADMIN] Panel de gestión. Aquí puedes agregar comandos exclusivos para ti.")
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data
        if data == "comprar_planes":
            user = query.from_user
            mensaje_admin = (
                f"🛒 <b>NUEVA SOLICITUD DE COMPRA</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 Usuario: <b>{user.full_name}</b>\n"
                f"🆔 ID: <code>{user.id}</code>\n"
                f"@{user.username if user.username else 'Sin username'}\n"
                f"Solicita información para comprar un plan.\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━"
            )
            # Notificar al admin
            try:
                await update.get_bot().send_message(
                    chat_id=7113848988,  # ID de @ZekAtwiN12
                    text=mensaje_admin,
                    parse_mode='HTML'
                )
            except Exception:
                pass
            await query.edit_message_caption(
                caption="✅ Tu solicitud fue enviada al admin. Pronto te contactará para completar la compra.\n\nPuedes escribirle directamente: @ZekAtwiN12",
                parse_mode='HTML'
            )
            return
        # Resto de callbacks
        if data.startswith("cat_"):
            category = data.replace("cat_", "")
            await self.show_category_commands(query, category)
        elif data == "buy_credits":
            await self.show_buy_options(query)
        elif data == "my_profile":
            await self.show_profile(query)
        elif data.startswith("cmd_"):
            await self.handle_command_callback(query, data)
        elif data == "back_to_main":
            await self.show_main_menu(query)
    
    async def show_category_commands(self, query, category):
        """Mostrar comandos de una categoría"""
        commands = self.get_category_commands(category)
        
        # Formatear comandos para mostrar
        commands_text = ""
        for cmd in commands:
            price_text = "Gratis" if cmd['price'] == 0 else f"{cmd['price']} Créditos"
            commands_text += f"""
{cmd['name']}

Comando ➾ /{cmd['command']} <parámetros>
Precio ➾ {price_text}
Resultado ➾ {cmd['desc']} en (TEXTO).

"""
        
        message = f"""
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ COMANDOS

CATEGORIA ➾ {category}
COMANDOS ➾ {len(commands)} Comandos disponibles
PAGINA ➾ 1/1

{commands_text}

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
        """
        
        # Crear botones para comandos
        keyboard = []
        for cmd in commands[:5]:  # Mostrar primeros 5 comandos
            keyboard.append([InlineKeyboardButton(cmd['name'], callback_data=f"cmd_{cmd['command']}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Volver", callback_data="back_to_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Obtener foto de la categoría
        photo_path = self.get_category_photo(category)
        
        await self.send_callback_with_photo(query, message, photo_path, reply_markup)
    
    def get_category_commands(self, category):
        """Obtener comandos de una categoría"""
        commands = {
            "RENIEC": [
                {"name": "[🪪] RENIEC ONLINE - FREE", "command": "dni", "price": 1, "desc": "Foto e información completa"},
                {"name": "[🪪] RENIEC ONLINE - BASICO", "command": "dnif", "price": 2, "desc": "Foto, Firma e información completa"},
                {"name": "[🪪] RENIEC ONLINE - STANDARD", "command": "dnit", "price": 3, "desc": "Foto, Firma, Huellas e información completa"},
                {"name": "[🪪] NOMBRES DATABASE - BASICO", "command": "nmdb", "price": 1, "desc": "Filtrador de Nombres"},
                {"name": "[📍] DIRECCION ONLINE - STANDARD", "command": "dir", "price": 2, "desc": "Filtrador de Direcciones"}
            ],
            "TELEFONIA": [
                {"name": "[📞] OSIPTEL ONLINE - PREMIUM", "command": "telp", "price": 10, "desc": "Números y titulares desde OSIPTEL"},
                {"name": "[📞] OSIPTEL DATABASE - STANDARD", "command": "cel", "price": 5, "desc": "Números y titulares desde OSIPTEL"},
                {"name": "[📞] CLARO ONLINE - STANDARD", "command": "claro", "price": 5, "desc": "Números y titulares desde CLARO"},
                {"name": "[📞] BITEL ONLINE - PREMIUM", "command": "bitel", "price": 5, "desc": "Números y titulares desde BITEL"}
            ],
            "DELITOS": [
                {"name": "[👮🏻‍♂️] VERIFICADOR ANT PENALES - STANDARD", "command": "antpenv", "price": 2, "desc": "Verifica antecedentes penales"},
                {"name": "[👮🏻‍♂️] VERIFICADOR ANT POLICIALES - STANDARD", "command": "antpolv", "price": 2, "desc": "Verifica antecedentes policiales"},
                {"name": "[👮🏻‍♂️] VERIFICADOR ANT JUDICIALES - STANDARD", "command": "antjudv", "price": 2, "desc": "Verifica antecedentes judiciales"}
            ],
            "SUNARP": [
                {"name": "[🚗] PLACA ONLINE - BASICO", "command": "vec", "price": 3, "desc": "Información sobre dueños de placa"},
                {"name": "[🚗] PLACA ONLINE - BASICO", "command": "pla", "price": 1, "desc": "Información sobre el auto"},
                {"name": "[🚗] PLACA ONLINE - STANDARD", "command": "plat", "price": 3, "desc": "Información completa de la placa"},
                {"name": "[🚗] TIVE ONLINE - STANDARD", "command": "tive", "price": 10, "desc": "Obtén tive en foto"}
            ],
            "GENERADORES": [
                {"name": "[🪪] FICHA C4 AZUL - FREE", "command": "c4", "price": 5, "desc": "Genera una ficha C4 azul"},
                {"name": "[🪪] DNI VIRTUAL - STANDARD", "command": "dniv", "price": 5, "desc": "Genera copia de DNI"},
                {"name": "[🪪] DNI ELECTRONICO - STANDARD", "command": "dnivel", "price": 5, "desc": "Genera copia de DNI electrónico"},
                {"name": "[🪪] ANTECEDENTE PENALES - STANDARD", "command": "antpen", "price": 5, "desc": "Genera ficha antecedentes penales"}
            ],
            "FAMILIARES": [
                {"name": "[👨‍👩‍👧] ARBOL GENEALOGICO - STANDARD", "command": "ag", "price": 5, "desc": "Árbol genealógico de familiares"},
                {"name": "[👨‍👩‍👧] FAMILIARES ONLINE - BASICO", "command": "fam", "price": 3, "desc": "Familiares de la persona"},
                {"name": "[👨‍👩‍👧] HERMANOS ONLINE - BASICO", "command": "her", "price": 3, "desc": "Hermanos de la persona"}
            ],
            "SPAM": [
                {"name": "[☠️] SPM ONLINE - BASICO", "command": "spm", "price": 3, "desc": "Realiza un spm de llamadas"},
                {"name": "[☠️] SPM FUENTE 2 - STANDARD", "command": "spmi", "price": 4, "desc": "Spm de llamadas y whatsapp"},
                {"name": "[☠️] SPM FUENTE 3 - STANDARD", "command": "spmm", "price": 5, "desc": "Verifica spm de llamadas y whatsapp"}
            ],
            "SEEKER": [
                {"name": "[🔎] DATA ONLINE - BASICO", "command": "dnis", "price": 2, "desc": "Información completa de SEEKER"},
                {"name": "[🔎] TELEFONOS ONLINE - STANDARD", "command": "tels", "price": 3, "desc": "Información TELEFONOS de SEEKER"},
                {"name": "[🔎] TRABAJOS ONLINE - STANDARD", "command": "tras", "price": 3, "desc": "Información de TRABAJOS de SEEKER"},
                {"name": "[🔎] SEEKER ONLINE - PREMIUM", "command": "seeker", "price": 10, "desc": "Información Completa de SEEKER"}
            ],
            "BAUCHER": [
                {"name": "[💳] PLIN FAKE - BASICO", "command": "plin", "price": 1, "desc": "Genera un baucher fake"},
                {"name": "[💳] INTERBANK FAKE - STANDARD", "command": "ibk", "price": 2, "desc": "Genera un baucher fake"},
                {"name": "[💳] BCP FAKE - STANDARD", "command": "bcp", "price": 2, "desc": "Genera un baucher fake"}
            ],
            "EXTRAS": [
                {"name": "[🌎] META DATA - STANDARD", "command": "meta", "price": 10, "desc": "Información completa de METADATA"},
                {"name": "[🎓] SUNEDU ONLINE - STANDARD", "command": "sunedu", "price": 5, "desc": "Información brindado por SUNEDU"},
                {"name": "[💼] SUNAT ONLINE - STANDARD", "command": "ruc", "price": 3, "desc": "Información del ruc"},
                {"name": "[🛠] TRABAJOS SUNAT - STANDARD", "command": "tra", "price": 3, "desc": "Información de los trabajos"}
            ],
            "GRATIS": [
                {"name": "[🪪] RENIEC ONLINE - FREE", "command": "dnix", "price": 0, "desc": "Foto e información media"},
                {"name": "[🪪] RENIEC ONLINE - FREE", "command": "nm", "price": 0, "desc": "Filtrador de Nombres"},
                {"name": "[📞] OSIPTEL DATABASE - FREE", "command": "tel", "price": 0, "desc": "Números y titulares desde OSIPTEL"},
                {"name": "[💳] YAPE FAKE - GRATIS", "command": "yape", "price": 0, "desc": "Genera un baucher fake"}
            ],
            "VIP": [
                {"name": "[💎] CERTIFICADO UNICO LABORAL (MTPE) - VIP", "command": "cerjov", "price": 10, "desc": "Ficha (CUL) el certificado MTPE"},
                {"name": "[💎] REGISTRO UNICO DE CONTRIBUYENTES (RUC) - VIP", "command": "sunat", "price": 10, "desc": "Ficha (RUC/DNI) el certificado SUNAT"},
                {"name": "[💎] DONA CREDITOS - VIP/PREMIUM", "command": "donate", "price": 0, "desc": "Dona credito a tus amigos"}
            ],
            "MUNDIAL": [
                {"name": "[🇻🇪] NOMBRES DE CHAMOS - BASICO", "command": "nmv", "price": 2, "desc": "Busca nombre de chamos"},
                {"name": "[🇺🇸] SSN SOCIAL SECURITY NUMBER - STANDARD", "command": "ssn", "price": 3, "desc": "Busca SSN EEUU"},
                {"name": "[🇦🇷] CHE BOLUDO ONLINE - STANDARD", "command": "arg", "price": 3, "desc": "Busca DNI ARGENTINA"}
            ],
            "TEMPORAL": [
                {"name": "[📚] UNIVERSIDAD TECNOLOGICA DE PERU - STANDARD", "command": "utp", "price": 3, "desc": "Información completa del alumno"},
                {"name": "[📚] UNIVERSIDAD SIDERAL CARRION - BASICO", "command": "dpm", "price": 1, "desc": "Obtén tu diploma digital"}
            ]
        }
        
        return commands.get(category, [])
    
    async def show_buy_options(self, query):
        """Mostrar opciones de compra"""
        message = f"""
💰 𝙎𝙄𝙎𝙏𝙀𝙈𝘼 𝘿𝙀 𝘾𝙊𝙈𝙋𝙍𝘼𝙎 - 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆

⫸ 𝙋𝙇𝘼𝙉𝙀𝙎 𝘿𝙄𝙎𝙋𝙊𝙉𝙄𝘽𝙇𝙀𝙎:

[🆓] PLAN FREE
• 5 créditos iniciales
• Consultas básicas
• Sin costo

[💎] PLAN PREMIUM - $10 USD
• 100 créditos
• Todas las consultas
• Soporte prioritario
• 30 días de duración

[👑] PLAN VIP - $25 USD
• 300 créditos
• Consultas ilimitadas
• Funciones exclusivas
• Soporte 24/7
• 90 días de duración

⫸ 𝙋𝘼𝙍𝘼 𝘾𝙊𝙈𝙋𝙍𝘼𝙍:
Contacta a {ADMIN_USERNAME}

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_callback_with_photo(query, message, "assets/buy.jpg", reply_markup)
    
    async def show_profile(self, query):
        """Mostrar perfil del usuario"""
        user_id = query.from_user.id
        user_data = self.db.get_user(user_id)
        
        if not user_data:
            await query.edit_message_text("❌ Primero debes registrarte. Usa /register")
            return
        
        # Calcular días restantes
        expiration_date = datetime.datetime.strptime(user_data[8], "%Y-%m-%d")
        days_remaining = (expiration_date - datetime.datetime.now()).days
        days_remaining = max(0, days_remaining)
        
        response = f"""
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ ME - PERFIL

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

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_callback_with_photo(query, response, "assets/wolfseek.png", reply_markup)
    
    async def show_main_menu(self, query):
        """Mostrar menú principal"""
        message = f"""
⟦ 𝙎𝙄𝙎𝙏𝙀𝙈𝘼 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ⟧

✦ 𝙃𝙤𝙡𝙖, ╰‿╯A҉U҉R҉A҉╰‿╯ | ╰$𝔈𝔑𝔈𝔐ℑ𝔖╯ | T/

𝘉𝘪𝘦𝘯𝘷𝘦𝘯𝘪𝘥𝘰 𝘢 𝘶𝘯 𝘴𝘪𝘴𝘵𝘦𝘮𝘢 𝘥𝘦𝘴𝘢𝘳𝘳𝘰𝘭𝘭𝘢𝘥𝘰 𝘱𝘢𝘳𝘢 𝘱𝘦𝘳𝘴𝘰𝘯𝘢𝘴 𝘲𝘶𝘦 𝘣𝘶𝘴𝘤𝘢𝘯 𝘳𝘢́𝘱𝘪𝘥𝘦𝘻 𝘺 𝘱𝘳𝘦𝘤𝘪𝘴𝘪ó𝘯.

⟡ 𝙀𝙭𝙥𝙡𝙤𝙧𝙖 𝙡𝙖𝙨 𝙤𝙥𝙘𝙞𝙤𝙣𝙚𝙨 𝙙𝙞𝙨𝙥𝙤𝙣𝙞𝙗𝙡𝙚𝙨 𝙮 𝙙𝙚𝙨𝙘𝙪𝙗𝙧𝙚 𝙡𝙤 𝙦𝙪𝙚 𝙣𝙚𝙘𝙚𝙨𝙞𝙩𝙖𝙨 𝙚𝙣 𝙘𝙪𝙚𝙨𝙩𝙞𝙤́𝙣 𝙙𝙚 𝙨𝙚𝙜𝙪𝙣𝙙𝙤𝙨.

⫸ 𝙎𝙀𝙇𝙀𝘾𝘾𝙄𝙊𝙉𝘼 𝙐𝙉𝘼 𝙊𝙋𝘾𝙄𝙊́𝙉 𝘿𝙀𝙇 𝙈𝙀𝙉𝙐́ ➾

≋≋≋ [ 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 • 2025 ] ≋≋≋
𝘓𝘢 𝘪𝘯𝘧𝘰𝘳𝘮𝘢𝘤𝘪ó𝘯 𝘦𝘴 𝘱𝘰𝘥𝘦𝘳. 𝘜𝘴𝘢𝘭𝘢 𝘤𝘰𝘯 𝘪𝘯𝘵𝘦𝘭𝘪𝘨𝘦𝘯𝘤𝘪𝘢.
        """
        
        keyboard = self.create_category_buttons()
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_callback_with_photo(query, message, "assets/wolfseek.png", reply_markup)
    
    async def handle_command_callback(self, query, data):
        """Manejar callbacks de comandos"""
        command = data.replace("cmd_", "")
        
        # Simular respuesta del comando
        response = f"""
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ {command.upper()} - SIMULACIÓN

⚠️ Este es un simulador de consulta
Comando: /{command} <parámetros>
Precio: Variable según comando
Resultado: Datos simulados

Para usar el comando real, escribe:
/{command} <parámetros>

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_callback_with_photo(query, response, "assets/command.jpg", reply_markup)
    
    # Aquí irían todos los comandos específicos (dni, telp, etc.)
    async def dni(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ RENIEC ONLINE - REAL\n\nDOCUMENTO ➾ {dni_data[0]}\nNOMBRES ➾ {dni_data[3]}\nAPELLIDOS ➾ {dni_data[1]} {dni_data[2]}\nSEXO ➾ {dni_data[11]}\n\n[🎂] NACIMIENTO\n\nFECHA NACIMIENTO ➾ {dni_data[4]}\nFCH INSCRIPCION ➾ {dni_data[5]}\nFCH EMISION ➾ {dni_data[6]}\nFCH CADUCIDAD ➾ {dni_data[7]}\n\nPADRE ➾ {dni_data[15]}\nMADRE ➾ {dni_data[14]}\n\n[🏠] DOMICILIO\n\nUBIGEO NAC ➾ {dni_data[8]}\nUBIGEO DIR ➾ {dni_data[9]}\nDIRECCION ➾ {dni_data[10]}\n\nESTADO CIVIL ➾ {dni_data[12]}\nDIG RUC ➾ {dni_data[13]}\n\n[⚡] ESTADO DE CUENTA\n\nCREDITOS ➾ {new_credits}\nUSUARIO ➾ {user_data[1] or user_data[2] or 'Usuario'}\n"""
        await self.send_message_with_photo(update, response, "assets/dni_result.jpg")

    async def dnix(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /dnix (gratis)"""
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
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ RENIEC NOMBRES - REAL\n\nDNI ➾ {dni_data[0]}\nNOMBRES ➾ {dni_data[3]}\nAPELLIDOS ➾ {dni_data[1]} {dni_data[2]}\nSEXO ➾ {dni_data[11]}\n\n[🎂] NACIMIENTO\nFECHA NACIMIENTO ➾ {dni_data[4]}\n\n[🏠] DOMICILIO\nDIRECCION ➾ {dni_data[10]}\n\n[⚡] ESTADO DE CUENTA\nCREDITOS ➾ {user_data[4]}\nUSUARIO ➾ {user_data[1] or user_data[2] or 'Usuario'}\n"""
        await self.send_message_with_photo(update, response, "assets/dni_result.jpg")
    
    async def telp(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /telp"""
        await self.handle_query_command(update, context, "telp", 10, "OSIPTEL ONLINE - PREMIUM")
    
    async def donate(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /donate"""
        user = update.effective_user
        user_id = user.id
        
        # Verificar si el usuario está registrado
        user_data = self.db.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ Primero debes registrarte. Usa /register")
            return
        
        # Verificar argumentos
        if len(context.args) < 2:
            await update.message.reply_text("❌ Uso: /donate <ID_USUARIO> <CREDITOS>\nEjemplo: /donate 123456789 10")
            return
        
        try:
            target_id = int(context.args[0])
            amount = int(context.args[1])
            
            if amount <= 0:
                await update.message.reply_text("❌ La cantidad debe ser mayor a 0.")
                return
            
            if user_data[4] < amount:
                await update.message.reply_text("❌ No tienes suficientes créditos para donar.")
                return
            
            # Verificar si el usuario objetivo existe
            target_user = self.db.get_user(target_id)
            if not target_user:
                await update.message.reply_text("❌ Usuario no encontrado.")
                return
            
            # Realizar la donación
            new_credits_donor = user_data[4] - amount
            new_credits_target = target_user[4] + amount
            
            self.db.update_credits(user_id, new_credits_donor)
            self.db.update_credits(target_id, new_credits_target)
            
            response = f"""
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ DONACIÓN EXITOSA

✅ Has donado {amount} créditos al usuario {target_id}

[💰] ESTADO DE CUENTA

CREDITOS ACTUALES ➾ {new_credits_donor}
CREDITOS DONADOS ➾ {amount}
USUARIO BENEFICIADO ➾ {target_id}

¡Gracias por tu generosidad!

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
            """
            
            await update.message.reply_text(response)
            
        except ValueError:
            await update.message.reply_text("❌ ID y cantidad deben ser números válidos.")
    
    async def handle_query_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, command_type, cost, service_name):
        """Manejar comandos de consulta genéricos"""
        user = update.effective_user
        user_id = user.id
        
        # Verificar si el usuario está registrado
        user_data = self.db.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ Primero debes registrarte. Usa /register")
            return
        
        # Verificar argumentos
        if not context.args:
            await update.message.reply_text(f"❌ Uso: /{command_type} <parámetros>\nEjemplo: /{command_type} 12345678")
            return
        
        # Verificar créditos si no es gratis
        if cost > 0:
            if user_data[4] < cost:
                await update.message.reply_text(f"❌ No tienes suficientes créditos. Necesitas {cost} crédito(s) para esta consulta.")
                return
        
        # Verificar anti-spam
        if user_data[11]:  # last_query_time
            last_query = datetime.datetime.strptime(user_data[11], "%Y-%m-%d %H:%M:%S")
            time_diff = (datetime.datetime.now() - last_query).total_seconds()
            if time_diff < ANTI_SPAM_DELAY:
                remaining = int(ANTI_SPAM_DELAY - time_diff)
                await update.message.reply_text(f"⏰ Espera {remaining} segundos antes de hacer otra consulta.")
                return
        
        # Descontar créditos si no es gratis
        if cost > 0:
            new_credits = user_data[4] - cost
            self.db.update_credits(user_id, new_credits)
        else:
            new_credits = user_data[4]
        
        # Registrar consulta
        self.db.log_query(user_id, context.args[0], command_type.upper())
        
        # Generar respuesta simulada
        response = self.generate_simulated_response(command_type, context.args[0], service_name, new_credits, user_data[1] or user_data[2] or 'Usuario')
        
        # Obtener foto según el tipo de comando
        photo_path = self.get_command_photo(command_type)
        
        await self.send_message_with_photo(update, response, photo_path)
    
    def get_command_photo(self, command_type):
        """Obtener foto para un comando específico"""
        photos = {
            "dni": "assets/dni_result.jpg",
            "dnix": "assets/dni_result.jpg",
            "telp": "assets/phone_result.jpg",
            "cel": "assets/phone_result.jpg",
            "claro": "assets/phone_result.jpg",
            "bitel": "assets/phone_result.jpg",
            "donate": "assets/donate.jpg"
        }
        return photos.get(command_type, "assets/result.jpg")
    
    def generate_simulated_response(self, command_type, query_param, service_name, credits, username):
        """Generar respuesta simulada para cualquier comando"""
        
        # Datos simulados según el tipo de comando
        if command_type in ['dni', 'dnix']:
            return f"""
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ {service_name} - SIMULACIÓN

DOCUMENTO ➾ {query_param} - 1
NOMBRES ➾ JUAN CARLOS
APELLIDOS ➾ GARCIA LOPEZ
GENERO ➾ MASCULINO

[🎂] NACIMIENTO

FECHA NACIMIENTO ➾ 15/03/1990
EDAD ➾ 33 AÑOS
PADRE ➾ CARLOS GARCIA
MADRE ➾ MARIA LOPEZ

[🏠] DOMICILIO

DEPARTAMENTO ➾ LIMA
PROVINCIA ➾ LIMA
DISTRITO ➾ MIRAFLORES
DIRECCION ➾ AV. AREQUIPA 123

⚠️ ESTA ES UNA SIMULACIÓN
Los datos mostrados son ficticios

[⚡] ESTADO DE CUENTA

CREDITOS ➾ {credits} - 7838557493
USUARIO ➾ {username}

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
            """
        
        elif command_type in ['telp', 'cel', 'claro', 'bitel']:
            return f"""
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ {service_name} - SIMULACIÓN

📞 INFORMACIÓN TELEFÓNICA

NÚMERO ➾ {query_param}
OPERADOR ➾ CLARO
TITULAR ➾ JUAN CARLOS GARCIA LOPEZ
DNI ➾ 12345678
ESTADO ➾ ACTIVO
FECHA ACTIVACIÓN ➾ 15/01/2020

⚠️ ESTA ES UNA SIMULACIÓN
Los datos mostrados son ficticios

[⚡] ESTADO DE CUENTA

CREDITOS ➾ {credits} - 7838557493
USUARIO ➾ {username}

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
            """
        
        else:
            return f"""
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ {service_name} - SIMULACIÓN

🔍 CONSULTA REALIZADA

PARÁMETRO ➾ {query_param}
SERVICIO ➾ {service_name}
ESTADO ➾ PROCESADO

⚠️ ESTA ES UNA SIMULACIÓN
Los datos mostrados son ficticios

[⚡] ESTADO DE CUENTA

CREDITOS ➾ {credits} - 7838557493
USUARIO ➾ {username}

꧁ 𝙋��𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏�� ꧂
            """
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes que no son comandos"""
        await update.message.reply_text(f"""
🤖 {BOT_NAME} - Sistema de Consultas

Comandos principales:
/start - Iniciar bot
/cmds - Ver comandos disponibles
/register - Registrarse
/me - Ver perfil
/buy - Comprar créditos

Para ver todas las opciones, usa /cmds

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀�� 𝘿𝘼𝙏𝘼 ꧂
        """)

    async def send_callback_with_photo(self, query, message, photo_path=None, reply_markup=None):
        """Enviar callback con foto"""
        try:
            if photo_path and os.path.exists(photo_path):
                with open(photo_path, 'rb') as photo:
                    await query.edit_message_media(
                        media=InputMediaPhoto(
                            media=photo,
                            caption=message
                        ),
                        reply_markup=reply_markup
                    )
            else:
                # Si no hay foto, editar mensaje normal
                await query.edit_message_text(message, reply_markup=reply_markup)
        except Exception as e:
            # Fallback a mensaje sin foto
            await query.edit_message_text(message, reply_markup=reply_markup)

    async def historial(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /historial"""
        user = update.effective_user
        user_id = user.id
        
        # Verificar si el usuario está registrado
        user_data = self.db.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ Primero debes registrarte. Usa /register")
            return
        
        # Obtener historial de consultas
        history = self.db.get_user_history(user_id, limit=10)
        
        if not history:
            response = """
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ HISTORIAL

📊 No hay consultas en tu historial

¡Comienza a usar los comandos para ver tu historial aquí!

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
            """
        else:
            history_text = ""
            for i, record in enumerate(history, 1):
                history_text += f"""
{i}. {record[2]} ➾ {record[1]}
   📅 {record[3]}
"""
            
            response = f"""
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ HISTORIAL

📊 ÚLTIMAS CONSULTAS:

{history_text}

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
            """
        
        await self.send_message_with_photo(update, response, "assets/wolfseek.png")
    
    async def referido(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /referido"""
        user = update.effective_user
        user_id = user.id
        
        # Verificar si el usuario está registrado
        user_data = self.db.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ Primero debes registrarte. Usa /register")
            return
        
        response = f"""
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ PROGRAMA DE REFERIDOS

🎯 SISTEMA DE REFERIDOS

[👥] REFERIDOS ACTUALES ➾ 0
[💰] CRÉDITOS GANADOS ➾ 0
[🔗] TU ENLACE ➾
https://t.me/{BOT_USERNAME}?start={user_data[0]}

📋 CÓMO FUNCIONA:

1. Comparte tu enlace con amigos
2. Cuando se registren usando tu enlace
3. Recibirás {REFERRAL_BONUS} créditos por cada referido
4. Tus referidos también reciben {REFERRAL_BONUS} créditos extra

🎁 ¡Invita amigos y gana créditos gratis!

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
        """
        
        await self.send_message_with_photo(update, response, "assets/wolfseek.png")
    
    async def compras(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /compras"""
        user = update.effective_user
        user_id = user.id
        
        # Verificar si el usuario está registrado
        user_data = self.db.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ Primero debes registrarte. Usa /register")
            return
        
        response = f"""
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ HISTORIAL DE COMPRAS

🛒 TUS COMPRAS:

📊 No hay compras registradas

💳 Para realizar una compra:
Contacta a {ADMIN_USERNAME}

📋 PLANES DISPONIBLES:
• PLAN PREMIUM - $10 USD (100 créditos)
• PLAN VIP - $25 USD (300 créditos)

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
        """
        
        await self.send_message_with_photo(update, response, "assets/wolfseek.png")
    
    async def girar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /girar - Ruleta de premios"""
        user = update.effective_user
        user_id = user.id
        
        # Verificar si el usuario está registrado
        user_data = self.db.get_user(user_id)
        if not user_data:
            await update.message.reply_text("❌ Primero debes registrarte. Usa /register")
            return
        
        # Verificar anti-spam para la ruleta
        if user_data[11]:  # last_query_time
            last_query = datetime.datetime.strptime(user_data[11], "%Y-%m-%d %H:%M:%S")
            time_diff = (datetime.datetime.now() - last_query).total_seconds()
            if time_diff < 300:  # 5 minutos entre giros
                remaining = int(300 - time_diff)
                await update.message.reply_text(f"⏰ Espera {remaining} segundos antes de girar la ruleta nuevamente.")
                return
        
        # Premios disponibles
        prizes = [
            {"name": "🎉 5 Créditos", "credits": 5, "probability": 0.4},
            {"name": "🎉 10 Créditos", "credits": 10, "probability": 0.3},
            {"name": "🎉 20 Créditos", "credits": 20, "probability": 0.2},
            {"name": "🎉 50 Créditos", "credits": 50, "probability": 0.08},
            {"name": "🎉 100 Créditos", "credits": 100, "probability": 0.02}
        ]
        
        # Seleccionar premio basado en probabilidades
        rand = random.random()
        cumulative = 0
        selected_prize = prizes[0]  # Por defecto
        
        for prize in prizes:
            cumulative += prize["probability"]
            if rand <= cumulative:
                selected_prize = prize
                break
        
        # Actualizar créditos del usuario
        new_credits = user_data[4] + selected_prize["credits"]
        self.db.update_credits(user_id, new_credits)
        
        # Registrar el giro
        self.db.log_query(user_id, "RULETA", "GIRAR")
        
        response = f"""
[#𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1.3_BOT] ➾ RULETA DE PREMIOS

🎰 ¡GIRANDO LA RULETA!

🎉 ¡FELICIDADES!

Has ganado: {selected_prize["name"]}

💰 ESTADO DE CUENTA:
CRÉDITOS ANTERIORES ➾ {user_data[4]}
CRÉDITOS GANADOS ➾ +{selected_prize["credits"]}
CRÉDITOS ACTUALES ➾ {new_credits}

🎁 ¡Vuelve a girar en 5 minutos!

꧁ 𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝘽𝙔: 𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆 𝘿𝘼𝙏𝘼 ꧂
        """
        
        await self.send_message_with_photo(update, response, "assets/wolfseek.png")

    # --- Comando exclusivo para admin: darcreditos ---
    async def darcreditos(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id
        user_data = self.db.get_user(user_id)
        if not self.is_admin(user_data):
            await self.send_message_with_photo(update, "❌ Solo el admin puede usar este comando.")
            return
        if len(context.args) < 2:
            await self.send_message_with_photo(update, "❌ Uso: /darcreditos <user_id> <cantidad>")
            return
        try:
            target_id = int(context.args[0])
            amount = int(context.args[1])
            if amount <= 0:
                await self.send_message_with_photo(update, "❌ La cantidad debe ser mayor a 0.")
                return
            target_user = self.db.get_user(target_id)
            if not target_user:
                await self.send_message_with_photo(update, "❌ Usuario no encontrado.")
                return
            new_credits = target_user[4] + amount
            self.db.update_credits(target_id, new_credits)
            # Notificar al usuario recargado (si está en el chat)
            try:
                await update.get_bot().send_message(
                    chat_id=target_id,
                    text=f"""
🎉 <b>¡RECARGA EXITOSA!</b> 🎉\n\n💸 Has recibido <b>{amount} créditos</b> en tu cuenta.\n\n[🦊] Recargado por: <b>@ZekAtwiN12</b>\n[💰] Créditos actuales: <b>{new_credits}</b>\n\n¡Sigue disfrutando de #𝙒𝙊𝙇𝙁𝙎𝙀𝙀𝙆𝙑1!\n\n✨ Usa /me para ver tu estado de cuenta.\n""",
                    parse_mode='HTML'
                )
            except Exception:
                pass
            await self.send_message_with_photo(update, f"✅ Se recargaron <b>{amount}</b> créditos al usuario <b>{target_id}</b>.")
        except ValueError:
            await self.send_message_with_photo(update, "❌ ID y cantidad deben ser números válidos.")

def main():
    """Función principal"""
    # Crear aplicación
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Crear instancia del bot
    bot = WolfSeekBot()
    
    # Agregar handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("cmds", bot.cmds))
    application.add_handler(CommandHandler("register", bot.register))
    application.add_handler(CommandHandler("me", bot.me))
    application.add_handler(CommandHandler("buy", bot.buy))
    
    # Comandos de consulta
    application.add_handler(CommandHandler("dni", bot.dni))
    application.add_handler(CommandHandler("dnix", bot.dnix))
    application.add_handler(CommandHandler("telp", bot.telp))
    application.add_handler(CommandHandler("donate", bot.donate))
    # Nuevo: handler para darcreditos solo admin
    application.add_handler(CommandHandler("darcreditos", bot.darcreditos))
    
    # Nuevos comandos
    application.add_handler(CommandHandler("historial", bot.historial))
    application.add_handler(CommandHandler("referido", bot.referido))
    application.add_handler(CommandHandler("compras", bot.compras))
    application.add_handler(CommandHandler("girar", bot.girar))
    
    # Handler para callbacks de botones
    application.add_handler(CallbackQueryHandler(bot.handle_callback))
    
    # Handler para mensajes que no son comandos
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Iniciar bot
    print(f"🤖 {BOT_NAME} iniciado...")
    application.run_polling()

if __name__ == '__main__':
    main() 