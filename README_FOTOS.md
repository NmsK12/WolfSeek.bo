# 📸 Sistema de Fotos para WolfSeek Bot

## 🎯 Características Implementadas

### ✅ Fotos Automáticas
- **Mensaje de bienvenida**: Foto principal del bot
- **Categorías**: Cada categoría tiene su foto específica
- **Comandos**: Cada tipo de consulta tiene su foto de resultado
- **Perfil de usuario**: Foto personalizada para el perfil
- **Sistema de compras**: Foto para las opciones de compra

### 📁 Estructura de Archivos

```
assets/
├── welcome.jpg          # Mensaje principal
├── buy.jpg             # Sistema de compras
├── profile.jpg         # Perfil de usuario
├── command.jpg         # Resultados de comandos
├── default.jpg         # Foto por defecto
├── reniec.jpg          # Categoría RENIEC
├── telefonia.jpg       # Categoría TELEFONIA
├── delitos.jpg         # Categoría DELITOS
├── sunarp.jpg          # Categoría SUNARP
├── generadores.jpg     # Categoría GENERADORES
├── familiares.jpg      # Categoría FAMILIARES
├── spam.jpg            # Categoría SPAM
├── seeker.jpg          # Categoría SEEKER
├── baucher.jpg         # Categoría BAUCHER
├── extras.jpg          # Categoría EXTRAS
├── gratis.jpg          # Categoría GRATIS
├── vip.jpg             # Categoría VIP
├── mundial.jpg         # Categoría MUNDIAL
├── temporal.jpg        # Categoría TEMPORAL
├── dni_result.jpg      # Resultados de DNI
├── phone_result.jpg    # Resultados de teléfonos
├── donate.jpg          # Sistema de donaciones
└── result.jpg          # Resultados genéricos
```

## 🔧 Cómo Personalizar las Fotos

### 1. Reemplazar Imágenes Existentes
Simplemente reemplaza cualquier archivo `.jpg` en la carpeta `assets/` con tu imagen personalizada.

**Recomendaciones:**
- **Tamaño**: 800x600 píxeles (o similar)
- **Formato**: JPG o PNG
- **Peso**: Menos de 5MB por imagen
- **Calidad**: Buena resolución pero optimizada

### 2. Crear Nuevas Categorías
Para agregar una nueva categoría con foto:

1. Agrega la imagen a `assets/`
2. Modifica `get_category_photo()` en `wolfseek_bot.py`:

```python
def get_category_photo(self, category):
    photos = {
        # ... categorías existentes ...
        "NUEVA_CATEGORIA": "assets/nueva_categoria.jpg"
    }
    return photos.get(category, "assets/default.jpg")
```

### 3. Agregar Fotos para Nuevos Comandos
Para nuevos comandos con fotos específicas:

1. Agrega la imagen a `assets/`
2. Modifica `get_command_photo()` en `wolfseek_bot.py`:

```python
def get_command_photo(self, command_type):
    photos = {
        # ... comandos existentes ...
        "nuevo_comando": "assets/nuevo_comando.jpg"
    }
    return photos.get(command_type, "assets/result.jpg")
```

## 🎨 Opciones de Personalización

### Opción 1: Fotos Estáticas (Actual)
- Fotos fijas para cada categoría/comando
- Fácil de implementar
- Consistente

### Opción 2: Fotos Dinámicas
Para fotos que cambien según el resultado:

```python
def get_dynamic_photo(self, command_type, result_data):
    """Obtener foto dinámica basada en el resultado"""
    if result_data.get('status') == 'success':
        return "assets/success.jpg"
    else:
        return "assets/error.jpg"
```

### Opción 3: Fotos con Texto Superpuesto
Para agregar texto a las fotos en tiempo real:

```python
from PIL import Image, ImageDraw, ImageFont

def create_photo_with_text(self, base_photo, text):
    """Crear foto con texto superpuesto"""
    img = Image.open(base_photo)
    draw = ImageDraw.Draw(img)
    # Agregar texto...
    return img
```

## 🚀 Ejecutar el Bot con Fotos

```bash
python wolfseek_bot.py
```

El bot ahora enviará automáticamente fotos con cada mensaje según la categoría o comando.

## 📝 Notas Importantes

1. **Fallback**: Si una foto no existe, el bot enviará el mensaje sin foto
2. **Optimización**: Las fotos se cargan desde el disco, no se almacenan en memoria
3. **Compatibilidad**: Funciona con JPG, PNG y otros formatos soportados por Telegram
4. **Tamaño**: Telegram tiene límites de tamaño para archivos multimedia

## 🎯 Próximos Pasos

- [ ] Agregar fotos personalizadas para cada comando específico
- [ ] Implementar sistema de fotos dinámicas
- [ ] Crear fotos con branding personalizado
- [ ] Agregar efectos visuales a las fotos
- [ ] Implementar cache de fotos para mejor rendimiento

¡Tu bot ahora tiene un aspecto mucho más profesional con fotos en cada mensaje! 🎉 