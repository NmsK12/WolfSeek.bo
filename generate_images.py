from PIL import Image, ImageDraw, ImageFont
import os

def create_image(text, filename, size=(800, 600), bg_color=(0, 0, 0), text_color=(255, 255, 255)):
    """Crear una imagen con texto"""
    # Crear imagen
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Intentar usar una fuente del sistema
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Calcular posición del texto
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Dibujar texto
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Guardar imagen
    img.save(f"assets/{filename}")
    print(f"✅ Creada: {filename}")

def main():
    """Crear todas las imágenes necesarias"""
    
    # Asegurar que existe la carpeta assets
    os.makedirs("assets", exist_ok=True)
    
    # Imágenes principales
    create_image("WOLFSEEK\nWELCOME", "welcome.jpg", bg_color=(25, 25, 25), text_color=(0, 255, 255))
    create_image("BUY CREDITS", "buy.jpg", bg_color=(0, 100, 0), text_color=(255, 255, 255))
    create_image("USER PROFILE", "profile.jpg", bg_color=(100, 0, 100), text_color=(255, 255, 255))
    create_image("COMMAND RESULT", "command.jpg", bg_color=(100, 100, 0), text_color=(255, 255, 255))
    create_image("DEFAULT", "default.jpg", bg_color=(50, 50, 50), text_color=(200, 200, 200))
    
    # Imágenes de categorías
    create_image("RENIEC", "reniec.jpg", bg_color=(0, 0, 150), text_color=(255, 255, 255))
    create_image("TELEFONIA", "telefonia.jpg", bg_color=(0, 150, 0), text_color=(255, 255, 255))
    create_image("DELITOS", "delitos.jpg", bg_color=(150, 0, 0), text_color=(255, 255, 255))
    create_image("SUNARP", "sunarp.jpg", bg_color=(150, 150, 0), text_color=(0, 0, 0))
    create_image("GENERADORES", "generadores.jpg", bg_color=(150, 0, 150), text_color=(255, 255, 255))
    create_image("FAMILIARES", "familiares.jpg", bg_color=(0, 150, 150), text_color=(0, 0, 0))
    create_image("SPAM", "spam.jpg", bg_color=(100, 50, 0), text_color=(255, 255, 255))
    create_image("SEEKER", "seeker.jpg", bg_color=(50, 100, 0), text_color=(255, 255, 255))
    create_image("BAUCHER", "baucher.jpg", bg_color=(100, 0, 50), text_color=(255, 255, 255))
    create_image("EXTRAS", "extras.jpg", bg_color=(50, 0, 100), text_color=(255, 255, 255))
    create_image("GRATIS", "gratis.jpg", bg_color=(0, 100, 100), text_color=(0, 0, 0))
    create_image("VIP", "vip.jpg", bg_color=(255, 215, 0), text_color=(0, 0, 0))
    create_image("MUNDIAL", "mundial.jpg", bg_color=(0, 100, 200), text_color=(255, 255, 255))
    create_image("TEMPORAL", "temporal.jpg", bg_color=(200, 100, 0), text_color=(255, 255, 255))
    
    # Imágenes de resultados
    create_image("DNI RESULT", "dni_result.jpg", bg_color=(0, 50, 100), text_color=(255, 255, 255))
    create_image("PHONE RESULT", "phone_result.jpg", bg_color=(0, 100, 50), text_color=(255, 255, 255))
    create_image("DONATE", "donate.jpg", bg_color=(100, 0, 100), text_color=(255, 255, 255))
    create_image("RESULT", "result.jpg", bg_color=(50, 50, 100), text_color=(255, 255, 255))
    
    print("\n🎉 Todas las imágenes han sido creadas en la carpeta 'assets'")

if __name__ == "__main__":
    main() 