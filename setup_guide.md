# 🚀 Guía Rápida de Configuración

## ⚡ Configuración en 5 minutos

### 1. Obtener Token de Telegram
1. Ve a [@BotFather](https://t.me/botfather) en Telegram
2. Envía `/newbot`
3. Sigue las instrucciones:
   - Nombre del bot: `Mi Bot RENIEC`
   - Username: `mi_bot_reniec_bot` (debe terminar en 'bot')
4. Copia el token que te da (algo como: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Configurar el Bot
Abre el archivo `config.py` y reemplaza la línea:
```python
BOT_TOKEN = "TU_TOKEN_AQUI"
```
Con tu token real:
```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### 3. Instalar Dependencias
```bash
pip install python-telegram-bot==20.7
```

### 4. Ejecutar el Bot
```bash
python bot.py
```

### 5. Probar el Bot
1. Ve a tu bot en Telegram
2. Envía `/start`
3. ¡Listo! Ya puedes usar todos los comandos

## 📋 Comandos de Prueba

Una vez que el bot esté funcionando, prueba estos comandos:

```
/start          - Iniciar y registrarse
/dnix 12345678  - Previsualizar datos (gratis)
/dni 12345678   - Consultar datos completos (cuesta 1 crédito)
/info           - Ver tu perfil
/cred 10        - Agregar 10 créditos
/girar          - Girar ruleta de premios
/historial      - Ver historial de consultas
```

## 🗄️ Datos de Ejemplo Disponibles

El bot viene con 10 DNIs de ejemplo para probar:

- `12345678` - JUAN CARLOS GARCIA LOPEZ
- `23456789` - MARIA ELENA RODRIGUEZ SANCHEZ
- `34567890` - PEDRO ANTONIO MARTINEZ DIAZ
- `45678901` - ANA LUCIA TORRES VARGAS
- `56789012` - CARLOS EDUARDO FLORES RUIZ
- `67890123` - SOFIA ALEJANDRA HERRERA MENDIETA
- `78901234` - ROBERTO JOSE SILVA CASTRO
- `89012345` - PATRICIA CARMEN MORALES VELASQUEZ
- `90123456` - FERNANDO RAUL CABRERA ORTIZ
- `01234567` - DANIELA GABRIELA PEREZ GONZALES

## 🛠️ Herramientas Adicionales

### Panel de Administración
```bash
python admin.py
```
- Ver estadísticas
- Gestionar usuarios
- Agregar créditos
- Ver historial

### Ejecutar Pruebas
```bash
python test_bot.py
```
- Verifica que todo funcione correctamente

## ⚠️ Solución de Problemas

### Error: "No module named 'telegram'"
```bash
pip install python-telegram-bot==20.7
```

### Error: "Invalid token"
- Verifica que el token en `config.py` sea correcto
- Asegúrate de que el bot esté activo en BotFather

### El bot no responde
- Verifica que esté ejecutándose: `python bot.py`
- Revisa que no haya errores en la consola

## 🎯 Próximos Pasos

1. **Personalizar**: Modifica los mensajes en `bot.py`
2. **Agregar datos**: Usa `admin.py` para agregar más DNIs de ejemplo
3. **Configurar**: Ajusta créditos, anti-spam, etc. en `config.py`
4. **Desplegar**: Sube el bot a un servidor para que funcione 24/7

---

**¡Tu bot está listo para usar! 🤖✨** 