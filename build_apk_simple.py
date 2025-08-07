"""
Build APK Simple - Sin caracteres especiales
"""

import subprocess
import os
import sys
import shutil

def limpiar_build():
    """Limpia carpetas de build anteriores"""
    carpetas = ['build', 'dist', '.dart_tool', '.flutter-plugins', '.flutter-plugins-dependencies']
    for carpeta in carpetas:
        if os.path.exists(carpeta):
            print(f"Eliminando {carpeta}...")
            shutil.rmtree(carpeta, ignore_errors=True)

def build_apk():
    """Ejecuta el build del APK"""
    print("\n" + "="*50)
    print("INICIANDO BUILD DE APK - CALCULADORA 3D PRO")
    print("="*50)
    
    # Limpiar builds anteriores
    limpiar_build()
    
    # Configurar encoding para evitar errores
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    print("\nEjecutando build de APK...")
    print("Esto puede tomar varios minutos...\n")
    
    # Comando de build
    cmd = [sys.executable, "-m", "flet", "build", "apk"]
    
    try:
        # Ejecutar build
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        print("\nSalida del build:")
        print("-" * 40)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Errores/Advertencias:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n" + "="*50)
            print("BUILD COMPLETADO EXITOSAMENTE!")
            print("="*50)
            
            # Buscar el APK generado
            buscar_apk()
        else:
            print("\n" + "="*50)
            print("ERROR EN EL BUILD")
            print(f"Codigo de salida: {result.returncode}")
            print("="*50)
            
    except Exception as e:
        print(f"\nError ejecutando build: {e}")
        return False
    
    return True

def buscar_apk():
    """Busca el archivo APK generado"""
    print("\nBuscando archivo APK generado...")
    
    # Posibles ubicaciones del APK
    posibles_rutas = [
        "build/apk/app-release.apk",
        "build/apk/app.apk",
        "build/app/outputs/flutter-apk/app-release.apk",
        "build/app/outputs/apk/release/app-release.apk",
        "dist/calculadora_3d_pro.apk",
        "dist/app.apk"
    ]
    
    apk_encontrado = None
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            apk_encontrado = ruta
            break
    
    if apk_encontrado:
        # Obtener tamaño del archivo
        size_mb = os.path.getsize(apk_encontrado) / (1024 * 1024)
        
        print(f"\nAPK ENCONTRADO!")
        print(f"Ubicacion: {os.path.abspath(apk_encontrado)}")
        print(f"Tamaño: {size_mb:.2f} MB")
        
        # Copiar a ubicación fácil de encontrar
        destino = "CALCULADORA_3D_PRO.apk"
        shutil.copy2(apk_encontrado, destino)
        print(f"\nAPK copiado a: {os.path.abspath(destino)}")
        print("\nPuedes transferir este archivo a tu dispositivo Android e instalarlo!")
        
    else:
        print("\nNo se encontro el archivo APK.")
        print("Posibles razones:")
        print("1. El build aun esta en proceso")
        print("2. Hubo un error durante el build")
        print("3. El APK se genero en otra ubicacion")
        
        # Buscar en todo el proyecto
        print("\nBuscando APK en todo el proyecto...")
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".apk"):
                    apk_path = os.path.join(root, file)
                    print(f"APK encontrado en: {apk_path}")
                    
                    # Copiar el primero encontrado
                    if not apk_encontrado:
                        apk_encontrado = apk_path
                        destino = "CALCULADORA_3D_PRO.apk"
                        shutil.copy2(apk_encontrado, destino)
                        print(f"APK copiado a: {os.path.abspath(destino)}")

def main():
    """Función principal"""
    print("SCRIPT DE BUILD APK - CALCULADORA 3D PRO")
    print("Version simplificada sin caracteres especiales")
    print("-" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("main_mobile.py"):
        print("ERROR: No se encontro main_mobile.py")
        print("Asegurate de ejecutar este script desde el directorio del proyecto")
        return 1
    
    # Ejecutar build
    if build_apk():
        print("\n" + "="*50)
        print("PROCESO COMPLETADO")
        print("="*50)
        print("\nSiguientes pasos:")
        print("1. Busca el archivo CALCULADORA_3D_PRO.apk en esta carpeta")
        print("2. Transfierelo a tu dispositivo Android")
        print("3. Habilita 'Fuentes desconocidas' en Configuracion")
        print("4. Instala el APK")
        print("5. Disfruta tu app!")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
