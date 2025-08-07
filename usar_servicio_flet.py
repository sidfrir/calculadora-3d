"""
Script para usar el servicio online de Flet Build
"""
import webbrowser
import os
import zipfile
import shutil

def preparar_proyecto():
    print("="*60)
    print(" PREPARANDO PROYECTO PARA FLET BUILD SERVICE ")
    print("="*60)
    
    # Archivos necesarios
    archivos_necesarios = [
        "main_mobile.py",
        "pyproject.toml",
        "models/database_simple.py",
        "views/calculator_view_mobile.py",
        "views/history_view_mobile.py",
        "views/home_view.py",
        "views/settings_view.py",
        "models/settings_manager.py",
        "models/user_preferences.py",
        "utils/themes.py",
        "utils/visual_effects.py",
        "assets/icon.png",
        "quotes.json",
        "settings.json",
        "user_preferences.json"
    ]
    
    # Crear carpeta temporal
    temp_dir = "flet_build_upload"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # Copiar archivos
    print("\nCopiando archivos necesarios...")
    for archivo in archivos_necesarios:
        src = archivo
        dst = os.path.join(temp_dir, archivo)
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✓ {archivo}")
    
    # Crear ZIP
    print("\nCreando archivo ZIP...")
    zip_name = "calculadora_3d_pro.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    # Limpiar
    shutil.rmtree(temp_dir)
    
    print(f"\n✓ Archivo creado: {zip_name}")
    print(f"  Tamaño: {os.path.getsize(zip_name) / 1024:.2f} KB")
    
    return zip_name

def main():
    # Preparar proyecto
    zip_file = preparar_proyecto()
    
    print("\n" + "="*60)
    print(" INSTRUCCIONES PARA GENERAR APK ")
    print("="*60)
    
    print("""
1. ABRE EL SERVICIO FLET BUILD:
   https://build.flet.dev

2. SUBE EL ARCHIVO:
   - Haz clic en "Upload"
   - Selecciona: calculadora_3d_pro.zip

3. CONFIGURA:
   - Platform: Android
   - Build mode: Release
   - Entry point: main_mobile.py

4. GENERA:
   - Haz clic en "Build"
   - Espera ~5-10 minutos

5. DESCARGA:
   - Descarga el APK generado
   - ¡Listo para instalar!
    """)
    
    # Abrir navegador
    print("\nAbriendo navegador...")
    webbrowser.open("https://build.flet.dev")
    
    print(f"\n📦 Tu archivo está listo: {os.path.abspath(zip_file)}")
    print("Súbelo al servicio cuando se abra la página")

if __name__ == "__main__":
    main()
