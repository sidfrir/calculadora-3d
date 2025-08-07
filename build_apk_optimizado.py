#!/usr/bin/env python
"""
Script optimizado para construir el APK de Calculadora 3D Pro
Versión móvil sin conexión a internet requerida
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

def print_header(message):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"  {message}")
    print("="*60)

def check_requirements():
    """Verifica que todos los requisitos estén instalados"""
    print_header("VERIFICANDO REQUISITOS")
    
    # Verificar Python
    print("✓ Python:", sys.version)
    
    # Verificar Flet
    try:
        import flet
        print(f"✓ Flet instalado: versión {flet.version.version}")
    except ImportError:
        print("✗ Flet no está instalado")
        print("  Instalando Flet...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flet==0.24.1"])
        
    # Verificar Java (necesario para Android)
    try:
        result = subprocess.run(["java", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Java instalado")
        else:
            print("⚠ Java no encontrado - Se instalará automáticamente durante el build")
    except FileNotFoundError:
        print("⚠ Java no encontrado - Se instalará automáticamente durante el build")
    
    return True

def prepare_project():
    """Prepara el proyecto para el build"""
    print_header("PREPARANDO PROYECTO")
    
    # Limpiar builds anteriores
    if os.path.exists("build"):
        print("Limpiando builds anteriores...")
        shutil.rmtree("build", ignore_errors=True)
    
    if os.path.exists("dist"):
        shutil.rmtree("dist", ignore_errors=True)
    
    # Verificar archivos necesarios
    required_files = [
        "main_mobile.py",
        "pyproject.toml",
        "requirements.txt",
        "assets/icon.png",
        "models/database_simple.py",
        "views/calculator_view_mobile.py",
        "views/history_view_mobile.py",
        "views/settings_view.py",
        "views/home_view.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
            print(f"✗ Falta: {file}")
        else:
            print(f"✓ Encontrado: {file}")
    
    if missing_files:
        print("\n⚠ ADVERTENCIA: Faltan algunos archivos")
        print("  El build podría fallar")
        response = input("\n¿Continuar de todos modos? (s/n): ")
        if response.lower() != 's':
            return False
    
    # Crear archivo de datos JSON vacío si no existe
    if not os.path.exists("quotes.json"):
        with open("quotes.json", "w") as f:
            json.dump([], f)
        print("✓ Creado archivo quotes.json vacío")
    
    return True

def optimize_for_mobile():
    """Optimiza el código para dispositivos móviles"""
    print_header("OPTIMIZANDO PARA MÓVILES")
    
    # Verificar que main_mobile.py esté configurado correctamente
    with open("main_mobile.py", "r", encoding="utf-8") as f:
        content = f.read()
        
    # Verificar configuraciones importantes
    checks = [
        ("page.window.width = 400" in content, "Ancho de ventana móvil"),
        ("page.window.height = 800" in content, "Alto de ventana móvil"),
        ("DatabaseManager" in content, "Base de datos simple"),
        ("assets_dir=\"assets\"" in content, "Directorio de assets")
    ]
    
    for check, description in checks:
        if check:
            print(f"✓ {description} configurado")
        else:
            print(f"⚠ {description} podría necesitar configuración")
    
    return True

def build_apk():
    """Construye el APK usando Flet"""
    print_header("CONSTRUYENDO APK")
    
    print("\nEsto puede tomar entre 10-30 minutos en la primera compilación...")
    print("Las compilaciones posteriores serán más rápidas.\n")
    
    # Comando de build
    cmd = [
        sys.executable, "-m", "flet", "build", "apk",
        "--name", "Calculadora 3D Pro",
        "--description", "Gestión completa para impresión 3D",
        "--org", "com.calculadora3d",
        "--project", "pro",
        "--build-version", "2.0.0",
        "--verbose"
    ]
    
    print("Ejecutando comando:")
    print(" ".join(cmd))
    print("\n" + "-"*60)
    
    try:
        # Ejecutar el build
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Mostrar output en tiempo real
        for line in process.stdout:
            print(line, end='')
        
        process.wait()
        
        if process.returncode == 0:
            print("\n" + "-"*60)
            print_header("✅ BUILD COMPLETADO CON ÉXITO")
            return True
        else:
            print("\n" + "-"*60)
            print_header("❌ ERROR EN EL BUILD")
            return False
            
    except Exception as e:
        print(f"\n❌ Error durante el build: {e}")
        return False

def locate_apk():
    """Encuentra el APK generado"""
    print_header("LOCALIZANDO APK")
    
    # Buscar en las ubicaciones comunes
    possible_paths = [
        "build/apk/app-release.apk",
        "dist/app-release.apk",
        "build/app/outputs/flutter-apk/app-release.apk",
        "build/app/outputs/apk/release/app-release.apk"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            # Obtener tamaño del archivo
            size = os.path.getsize(path)
            size_mb = size / (1024 * 1024)
            
            print(f"✓ APK encontrado: {path}")
            print(f"  Tamaño: {size_mb:.2f} MB")
            
            # Copiar a ubicación más accesible
            final_name = "Calculadora3DPro_v2.0.0.apk"
            shutil.copy2(path, final_name)
            print(f"✓ Copiado como: {final_name}")
            
            return os.path.abspath(final_name)
    
    print("✗ No se encontró el APK")
    print("  Revisa la carpeta 'build' manualmente")
    return None

def create_installation_guide():
    """Crea una guía de instalación para el usuario"""
    print_header("CREANDO GUÍA DE INSTALACIÓN")
    
    guide_content = """# 📱 GUÍA DE INSTALACIÓN - CALCULADORA 3D PRO

## 🎯 Instalación Rápida

### Paso 1: Transferir el APK
1. Conecta tu dispositivo Android a la computadora
2. Copia el archivo `Calculadora3DPro_v2.0.0.apk` a tu dispositivo
3. Puedes copiarlo a la carpeta "Descargas" para encontrarlo fácilmente

### Paso 2: Habilitar Instalación de Fuentes Desconocidas
1. Ve a **Configuración** > **Seguridad**
2. Activa **"Fuentes desconocidas"** o **"Instalar apps desconocidas"**
3. En Android 8+: Da permiso al explorador de archivos para instalar apps

### Paso 3: Instalar la Aplicación
1. Abre el explorador de archivos en tu dispositivo
2. Navega hasta donde copiaste el APK
3. Toca el archivo APK
4. Presiona **"Instalar"**
5. Una vez instalada, presiona **"Abrir"**

## ✨ Características de la App

### 🔧 Funcionalidades Principales:
- **Calculadora de Costos**: Calcula costos de impresión 3D
- **Historial**: Guarda y revisa cotizaciones anteriores
- **Configuración**: Personaliza parámetros y moneda (USD/ARS)
- **Sin Internet**: Funciona 100% offline

### 📊 Datos Técnicos:
- Versión: 2.0.0
- Tamaño aproximado: 30-50 MB
- Android mínimo: 5.0 (API 21)
- Permisos: Almacenamiento local

## 🔒 Seguridad
La aplicación:
- ✅ No requiere conexión a internet
- ✅ No recopila datos personales
- ✅ Todos los datos se guardan localmente
- ✅ No contiene anuncios ni compras

## 🆘 Solución de Problemas

### "La app no se instala"
- Verifica que tengas suficiente espacio (necesitas ~100 MB libres)
- Asegúrate de haber habilitado fuentes desconocidas
- Intenta reiniciar el dispositivo

### "La app se cierra al abrir"
- Verifica que tu Android sea 5.0 o superior
- Reinicia el dispositivo
- Desinstala y vuelve a instalar

### "No puedo guardar cotizaciones"
- La app necesita permisos de almacenamiento
- Ve a Configuración > Apps > Calculadora 3D Pro > Permisos
- Activa el permiso de Almacenamiento

## 📞 Soporte
Si tienes problemas, verifica:
1. Tu versión de Android (mínimo 5.0)
2. Espacio disponible (mínimo 100 MB)
3. Permisos de la aplicación

---
**Disfruta de tu Calculadora 3D Pro!** 🚀
"""
    
    with open("GUIA_INSTALACION_APK.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✓ Guía creada: GUIA_INSTALACION_APK.md")
    return True

def main():
    """Función principal del script"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║           CALCULADORA 3D PRO - GENERADOR DE APK         ║
    ║                    Versión 2.0.0                        ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Paso 1: Verificar requisitos
        if not check_requirements():
            print("\n❌ No se pudieron cumplir los requisitos")
            return 1
        
        # Paso 2: Preparar proyecto
        if not prepare_project():
            print("\n❌ Error al preparar el proyecto")
            return 1
        
        # Paso 3: Optimizar para móviles
        if not optimize_for_mobile():
            print("\n⚠ Advertencias en la optimización")
        
        # Paso 4: Construir APK
        if not build_apk():
            print("\n❌ Error al construir el APK")
            print("\nPosibles soluciones:")
            print("1. Verifica que tengas Java instalado")
            print("2. Intenta: pip install --upgrade flet")
            print("3. Ejecuta: flet build apk --verbose")
            return 1
        
        # Paso 5: Localizar APK
        apk_path = locate_apk()
        if not apk_path:
            print("\n⚠ APK construido pero no localizado automáticamente")
            print("Busca manualmente en la carpeta 'build'")
        
        # Paso 6: Crear guía de instalación
        create_installation_guide()
        
        # Resumen final
        print_header("✅ PROCESO COMPLETADO")
        print("\n📱 Tu APK está listo para distribución!")
        
        if apk_path:
            print(f"\n📦 Archivo APK: {apk_path}")
        
        print("\n📋 Próximos pasos:")
        print("1. Lee GUIA_INSTALACION_APK.md")
        print("2. Transfiere el APK a dispositivos Android")
        print("3. Instala siguiendo la guía")
        print("\n¡La app funcionará 100% offline!")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠ Proceso cancelado por el usuario")
        return 1
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
