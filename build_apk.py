#!/usr/bin/env python3
"""
Script alternativo para generar APK de Calculadora 3D Pro
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def check_requirements():
    """Verifica que Flet esté instalado"""
    try:
        import flet
        print("✅ Flet está instalado")
        return True
    except ImportError:
        print("❌ Flet no está instalado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flet[mobile-build]"])
        return True

def create_simple_build():
    """Crea un build simple usando el comando básico de Flet"""
    print("🚀 Iniciando compilación de APK...")
    
    # Comando básico de build
    cmd = [
        sys.executable, "-m", "flet.cli", "build", "apk",
        "--name", "Calculadora3DPro",
        "--org", "com.calculadora3d",
        "--project", "calculadora-3d-pro",
        "--build-number", "1",
        "--build-version", "1.0.0"
    ]
    
    try:
        print(f"Ejecutando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 min timeout
        
        if result.returncode == 0:
            print("✅ APK generado exitosamente!")
            print(f"Salida: {result.stdout}")
            
            # Buscar el archivo APK generado
            dist_dir = Path("dist")
            if dist_dir.exists():
                apk_files = list(dist_dir.glob("*.apk"))
                if apk_files:
                    apk_file = apk_files[0]
                    print(f"📱 APK generado: {apk_file}")
                    print(f"📂 Ubicación: {apk_file.absolute()}")
                    print(f"📏 Tamaño: {apk_file.stat().st_size / (1024*1024):.1f} MB")
                    return True
        else:
            print(f"❌ Error en la compilación: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout en la compilación (30 minutos)")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def build_web_alternative():
    """Genera una versión web como alternativa"""
    print("🌐 Generando versión web como alternativa...")
    
    cmd = [sys.executable, "-m", "flet.cli", "build", "web"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            print("✅ Versión web generada exitosamente!")
            print("📂 Ubicación: dist/web/")
            return True
        else:
            print(f"❌ Error generando web: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error en web: {e}")
        return False

def main():
    print("🔧 Build Helper para Calculadora 3D Pro")
    print("=" * 50)
    
    if not check_requirements():
        return
    
    # Verificar archivos necesarios
    if not os.path.exists("main.py"):
        print("❌ No se encontró main.py")
        return
    
    print("📋 Archivos principales encontrados:")
    for file in ["main.py", "pyproject.toml", "assets/icon.png"]:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} (opcional)")
    
    print("\n🚀 Iniciando proceso de compilación...")
    
    # Intentar crear APK
    if create_simple_build():
        print("\n🎉 ¡APK creado exitosamente!")
    else:
        print("\n📱 El APK no se pudo crear. Intentando versión web...")
        if build_web_alternative():
            print("\n💡 Se creó una versión web que puedes usar en el navegador del móvil")
        else:
            print("\n❌ No se pudo crear ninguna versión")

if __name__ == "__main__":
    main()
