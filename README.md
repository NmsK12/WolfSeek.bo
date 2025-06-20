# 🤖 Bot de Consulta RENIEC - Telegram

Un bot completo de Telegram que simula un sistema de consulta de datos personales con sistema de créditos, similar al ejemplo proporcionado.

## 📋 Características

- ✅ **Sistema de usuarios** con registro automático
- ✅ **Sistema de créditos** con gestión completa
- ✅ **Consulta de DNI** con datos de ejemplo
- ✅ **Anti-spam** con delay configurable
- ✅ **Historial de consultas** por usuario
- ✅ **Ruleta de premios** para ganar créditos
- ✅ **Perfil de usuario** detallado
- ✅ **Base de datos SQLite** integrada
- ✅ **Interfaz idéntica** al ejemplo original

## 🚀 Instalación

### 1. Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 2. Clonar/Descargar el Proyecto
```bash
# Si tienes git:
git clone <url-del-repositorio>
cd reniec-bot

# O simplemente descarga los archivos en una carpeta
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar el Bot

#### Obtener Token de Telegram:
1. Ve a [@BotFather](https://t.me/botfather) en Telegram
2. Envía `/newbot`
3. Sigue las instrucciones para crear tu bot
4. Copia el token que te proporciona

#### Editar Configuración:
Abre el archivo `config.py` y reemplaza:
```python
BOT_TOKEN = "TU_TOKEN_AQUI"  # Reemplaza con tu token real
```

### 5. Ejecutar el Bot
```bash
python bot.py
```

## 📖 Comandos Disponibles

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/start` | Iniciar el bot y registrarse | `/start` |
| `/register` | Registrarse en el sistema | `/register` |
| `/dni <DNI>` | Consultar datos completos | `/dni 12345678` |
| `/dnix <DNI>` | Previsualizar datos (gratis) | `/dnix 12345678` |
| `/info` | Ver perfil de usuario | `/info` |
| `/cred <cantidad>` | Administrar créditos | `/cred 10` |
| `/historial` | Ver historial de consultas | `/historial` |
| `/girar` | Girar ruleta de premios | `/girar` |

## 🗄️ Estructura de la Base de Datos

### Tabla `users`
- `user_id`: ID único del usuario
- `username`: Nombre de usuario de Telegram
- `first_name`: Nombre del usuario
- `last_name`: Apellido del usuario
- `credits`: Créditos disponibles
- `role`: Rol del usuario (FREE/PREMIUM/ADMIN)
- `plan`: Plan actual
- `registration_date`: Fecha de registro
- `expiration_date`: Fecha de expiración
- `total_queries`: Total de consultas realizadas
- `today_queries`: Consultas de hoy
- `last_query_time`: Última consulta realizada
- `referral_code`: Código de referido
- `referred_by`: ID del usuario que lo refirió

### Tabla `queries`
- `id`: ID único de la consulta
- `user_id`: ID del usuario que realizó la consulta
- `dni`: DNI consultado
- `query_type`: Tipo de consulta
- `query_date`: Fecha y hora de la consulta

### Tabla `sample_data`
- `dni`: DNI (clave primaria)
- `nombres`: Nombres completos
- `apellidos`: Apellidos completos
- `fecha_nacimiento`: Fecha de nacimiento
- `edad`: Edad calculada
- `genero`: Género
- `padre`: Nombre del padre
- `madre`: Nombre de la madre
- `departamento`: Departamento
- `provincia`: Provincia
- `distrito`: Distrito
- `direccion`: Dirección completa

## ⚙️ Configuración

### Archivo `config.py`
```python
# Token del bot de Telegram
BOT_TOKEN = "TU_TOKEN_AQUI"

# Configuración de la base de datos
DATABASE_NAME = "reniec_bot.db"

# Configuración de créditos
INITIAL_CREDITS = 5
CREDIT_COST_PER_QUERY = 1
ANTI_SPAM_DELAY = 60  # segundos

# Configuración de roles
ROLES = {
    "FREE": "FREE",
    "PREMIUM": "PREMIUM",
    "ADMIN": "ADMIN"
}

# Configuración de referidos
REFERRAL_BONUS = 2  # créditos por referido
```

## 🔧 Personalización

### Agregar Más Datos de Ejemplo
Edita el archivo `database.py` en la función `populate_sample_data()` para agregar más registros:

```python
sample_data = [
    ("12345678", "JUAN CARLOS", "GARCIA LOPEZ", "15/03/1990", 33, "MASCULINO", "CARLOS GARCIA", "MARIA LOPEZ", "LIMA", "LIMA", "MIRAFLORES", "AV. AREQUIPA 123"),
    # Agrega más datos aquí...
]
```

### Modificar Interfaz
Edita el archivo `bot.py` para cambiar los mensajes y el formato de las respuestas.

### Cambiar Configuración de Créditos
Modifica los valores en `config.py`:
- `INITIAL_CREDITS`: Créditos iniciales para nuevos usuarios
- `CREDIT_COST_PER_QUERY`: Costo por consulta
- `ANTI_SPAM_DELAY`: Tiempo entre consultas

## 🛡️ Seguridad

- ✅ Validación de formato de DNI
- ✅ Sistema anti-spam
- ✅ Verificación de créditos
- ✅ Logs de todas las consultas
- ✅ Base de datos SQLite segura

## 📊 Funcionalidades Avanzadas

### Sistema de Referidos
- Los usuarios pueden referir a otros
- Bonificación de créditos por referidos
- Enlaces de invitación únicos

### Ruleta de Premios
- Sistema de premios aleatorios
- Diferentes cantidades de créditos
- Mensajes motivacionales

### Historial de Consultas
- Registro de todas las consultas
- Estadísticas por usuario
- Consultas diarias y totales

## 🚨 Notas Importantes

⚠️ **Este es un proyecto de ejemplo con datos ficticios**
- Los datos incluidos son completamente ficticios
- Solo para propósitos educativos y de desarrollo
- No contiene información real de personas

⚠️ **Uso Responsable**
- Solo usar para propósitos legítimos
- Respetar las leyes de protección de datos
- No usar para actividades ilegales

## 🐛 Solución de Problemas

### Error: "No module named 'telegram'"
```bash
pip install python-telegram-bot==20.7
```

### Error: "Invalid token"
- Verifica que el token en `config.py` sea correcto
- Asegúrate de que el bot esté activo en BotFather

### Error: "Database is locked"
- Cierra otras instancias del bot
- Verifica permisos de escritura en la carpeta

## 📞 Soporte

Si tienes problemas o preguntas:
1. Revisa la documentación
2. Verifica la configuración
3. Revisa los logs del bot

## 📄 Licencia

Este proyecto es solo para propósitos educativos. Úsalo responsablemente.

---

**¡Disfruta tu bot de Telegram! 🤖✨** 