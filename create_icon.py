from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    # Crear un ícono de 512x512 para la aplicación
    size = 512
    img = Image.new('RGBA', (size, size), (33, 150, 243, 255))  # Color azul material
    draw = ImageDraw.Draw(img)
    
    # Dibujar un cubo 3D simple
    # Cara frontal
    draw.polygon([(100, 150), (400, 150), (400, 450), (100, 450)], 
                fill=(255, 255, 255, 200), outline=(0, 0, 0, 255), width=3)
    
    # Cara superior (perspectiva)
    draw.polygon([(100, 150), (150, 100), (450, 100), (400, 150)], 
                fill=(200, 200, 200, 200), outline=(0, 0, 0, 255), width=3)
    
    # Cara derecha (perspectiva)
    draw.polygon([(400, 150), (450, 100), (450, 400), (400, 450)], 
                fill=(150, 150, 150, 200), outline=(0, 0, 0, 255), width=3)
    
    # Agregar texto "3D"
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    text = "3D"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 + 20
    
    draw.text((text_x, text_y), text, fill=(0, 0, 0, 255), font=font)
    
    # Guardar el ícono
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    img.save(os.path.join(assets_dir, "icon.png"))
    print("Ícono creado exitosamente en assets/icon.png")

if __name__ == "__main__":
    create_app_icon()
