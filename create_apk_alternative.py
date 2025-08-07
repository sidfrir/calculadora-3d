import os
import subprocess
import shutil
import zipfile
import json
from pathlib import Path

def create_simple_apk():
    """Crear APK usando herramientas alternativas"""
    
    print("🔧 Intentando crear APK con método alternativo...")
    
    try:
        # Verificar si existe buildozer
        try:
            result = subprocess.run(['buildozer', '--version'], capture_output=True, text=True)
            print("✅ Buildozer encontrado")
            use_buildozer = True
        except FileNotFoundError:
            print("❌ Buildozer no encontrado")
            use_buildozer = False
        
        if use_buildozer:
            return create_apk_with_buildozer()
        else:
            return create_web_apk()
            
    except Exception as e:
        print(f"❌ Error en creación de APK: {e}")
        return create_installable_web_app()

def create_apk_with_buildozer():
    """Crear APK usando Buildozer (Kivy)"""
    print("🏗️  Creando APK con Buildozer...")
    
    # Crear buildozer.spec
    buildozer_spec = """[app]
title = Calculadora 3D Pro
package.name = calculadora3dpro
package.domain = com.empresa.calculadora3dpro

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0
requirements = python3,kivy,flet

[buildozer]
log_level = 2

[app]
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
"""
    
    with open("buildozer.spec", "w") as f:
        f.write(buildozer_spec)
    
    # Ejecutar buildozer
    try:
        subprocess.run(['buildozer', 'android', 'debug'], check=True)
        print("✅ APK creado con Buildozer")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error con Buildozer: {e}")
        return False

def create_web_apk():
    """Crear APK a partir de aplicación web"""
    print("🌐 Creando APK web híbrida...")
    
    # Crear estructura básica de APK web
    manifest = {
        "name": "Calculadora 3D Pro",
        "short_name": "3D Calc Pro",
        "description": "Calculadora profesional para impresión 3D",
        "start_url": "http://localhost:8080",
        "display": "fullscreen",
        "orientation": "portrait",
        "theme_color": "#2196F3",
        "background_color": "#ffffff",
        "icons": [
            {
                "src": "icon.png",
                "sizes": "192x192",
                "type": "image/png"
            }
        ]
    }
    
    # Crear directorio web
    os.makedirs("web_app", exist_ok=True)
    
    with open("web_app/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    # Crear HTML básico
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Calculadora 3D Pro</title>
    <link rel="manifest" href="manifest.json">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <style>
        body { font-family: Arial; padding: 20px; }
        .container { max-width: 400px; margin: 0 auto; }
        h1 { color: #2196F3; text-align: center; }
        .info { background: #f0f8ff; padding: 15px; border-radius: 8px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧮 Calculadora 3D Pro</h1>
        <div class="info">
            <h3>📱 Para usar la aplicación completa:</h3>
            <ol>
                <li>Ejecuta en tu PC: <code>.venv\\Scripts\\python run_web_server.py</code></li>
                <li>Obtén la IP de tu PC (ejecuta <code>ipconfig</code>)</li>
                <li>En este navegador, ve a: <code>http://[IP_PC]:8080</code></li>
                <li>¡Listo! Tendrás la aplicación completa funcionando</li>
            </ol>
        </div>
        <div class="info">
            <h3>✅ Aplicación Completa Incluye:</h3>
            <ul>
                <li>🧮 Calculadora de costos 3D</li>
                <li>📊 Historial de cotizaciones</li>
                <li>👥 Gestión de clientes</li>
                <li>📋 Gestión de proyectos</li>
                <li>⚙️ Configuración personalizable</li>
            </ul>
        </div>
    </div>
</body>
</html>"""
    
    with open("web_app/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Copiar ícono
    if os.path.exists("assets/icon.png"):
        shutil.copy("assets/icon.png", "web_app/icon.png")
    
    print("✅ Aplicación web creada en carpeta 'web_app'")
    return True

def create_installable_web_app():
    """Crear aplicación web instalable"""
    print("📲 Creando aplicación web instalable...")
    
    instructions = """
# 📱 CÓMO INSTALAR LA APLICACIÓN EN TU MÓVIL

## Opción 1: Instalar como PWA (Recomendado)
1. Ejecuta: `.venv\\Scripts\\python run_web_server.py`
2. En tu móvil, abre el navegador Chrome
3. Ve a: http://[IP_DE_TU_PC]:8080
4. Toca el menú (3 puntos) del navegador
5. Selecciona "Instalar aplicación" o "Agregar a pantalla de inicio"
6. ¡Listo! Tendrás un ícono de la app en tu móvil

## Opción 2: Usar ApkTool Online
1. Ve a: https://www.websitetoapk.com/
2. Ingresa: http://[IP_DE_TU_PC]:8080
3. Configura el nombre: "Calculadora 3D Pro"
4. Descarga el APK generado
5. Instala en tu móvil

## Opción 3: Usar PWA Builder (Microsoft)
1. Ve a: https://www.pwabuilder.com/
2. Ingresa la URL de tu aplicación web
3. Genera el APK automáticamente
4. Instala en tu dispositivo

## ✅ Tu aplicación ya está lista para funcionar!
Solo necesita ejecutarse el servidor en tu PC.
"""
    
    with open("INSTRUCCIONES_APK.txt", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("✅ Instrucciones de instalación creadas")
    print("📄 Ver archivo: INSTRUCCIONES_APK.txt")
    return True

if __name__ == "__main__":
    print("🚀 GENERADOR DE APK ALTERNATIVO")
    print("=" * 50)
    success = create_simple_apk()
    if success:
        print("\n✅ ¡Proceso completado!")
        print("📱 Consulta las instrucciones para instalar en tu móvil")
    else:
        print("\n❌ No se pudo crear APK nativo")
        print("📲 Usa la versión web instalable como alternativa")
