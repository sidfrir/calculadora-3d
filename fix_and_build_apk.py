"""
Script para arreglar el proyecto Flutter y generar APK
"""
import os
import subprocess
import shutil
import tempfile

def main():
    print("="*60)
    print("GENERADOR DE APK - CALCULADORA 3D PRO")
    print("="*60)
    
    # Encontrar directorio Flutter
    temp_dir = tempfile.gettempdir()
    flutter_dir = None
    
    for item in os.listdir(temp_dir):
        if item.startswith("flet_flutter_build"):
            flutter_dir = os.path.join(temp_dir, item)
            break
    
    if not flutter_dir:
        print("ERROR: No se encontró el proyecto Flutter")
        print("\nPrimero ejecuta: .venv\\Scripts\\flet build apk")
        print("Luego vuelve a ejecutar este script")
        return 1
    
    print(f"\nProyecto Flutter encontrado: {flutter_dir}")
    
    # Navegar al directorio
    os.chdir(flutter_dir)
    
    # Arreglar el archivo build.gradle
    build_gradle = os.path.join(flutter_dir, "android", "app", "build.gradle")
    if os.path.exists(build_gradle):
        print("\nArreglando configuración de Android...")
        
        with open(build_gradle, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cambiar minSdkVersion si es necesario
        content = content.replace('minSdkVersion flutter.minSdkVersion', 'minSdkVersion 21')
        content = content.replace('targetSdkVersion flutter.targetSdkVersion', 'targetSdkVersion 33')
        
        # Asegurar que compileSdkVersion sea compatible
        if 'compileSdkVersion' in content:
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if 'compileSdkVersion' in line and not '//' in line:
                    new_lines.append('    compileSdkVersion 33')
                else:
                    new_lines.append(line)
            content = '\n'.join(new_lines)
        
        with open(build_gradle, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ Configuración arreglada")
    
    # Limpiar cache de Flutter
    print("\nLimpiando cache...")
    subprocess.run(["flutter", "clean"], capture_output=True)
    
    # Obtener dependencias
    print("Obteniendo dependencias...")
    result = subprocess.run(["flutter", "pub", "get"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error obteniendo dependencias:")
        print(result.stderr)
    
    # Construir APK (debug es más rápido y confiable)
    print("\n" + "="*60)
    print("CONSTRUYENDO APK...")
    print("Esto puede tomar 5-10 minutos...")
    print("="*60)
    
    # Intentar build debug primero (más confiable)
    result = subprocess.run(
        ["flutter", "build", "apk", "--debug", "--no-tree-shake-icons"],
        capture_output=False,
        text=True
    )
    
    apk_path = None
    if result.returncode == 0:
        # Buscar APK debug
        apk_path = os.path.join(flutter_dir, "build", "app", "outputs", "flutter-apk", "app-debug.apk")
        if not os.path.exists(apk_path):
            apk_path = os.path.join(flutter_dir, "build", "app", "outputs", "apk", "debug", "app-debug.apk")
    else:
        print("\nBuild debug falló, intentando release...")
        # Intentar release
        result = subprocess.run(
            ["flutter", "build", "apk", "--release", "--no-tree-shake-icons", "--no-shrink"],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            apk_path = os.path.join(flutter_dir, "build", "app", "outputs", "flutter-apk", "app-release.apk")
            if not os.path.exists(apk_path):
                apk_path = os.path.join(flutter_dir, "build", "app", "outputs", "apk", "release", "app-release.apk")
    
    # Verificar si se generó el APK
    if apk_path and os.path.exists(apk_path):
        print("\n" + "="*60)
        print("✓ APK GENERADO EXITOSAMENTE!")
        print("="*60)
        
        # Copiar a directorio principal
        project_dir = "d:\\datos\\proyectos para la agencia\\PROGRAMA CALCULADORA IMPRESORA 3D"
        dest_path = os.path.join(project_dir, "CALCULADORA_3D_PRO.apk")
        
        shutil.copy2(apk_path, dest_path)
        
        size_mb = os.path.getsize(dest_path) / (1024 * 1024)
        
        print(f"\nArchivo: CALCULADORA_3D_PRO.apk")
        print(f"Ubicación: {dest_path}")
        print(f"Tamaño: {size_mb:.2f} MB")
        print("\n¡APK listo para instalar en tu dispositivo Android!")
        print("\nPasos para instalar:")
        print("1. Transfiere CALCULADORA_3D_PRO.apk a tu teléfono")
        print("2. Habilita 'Fuentes desconocidas' en Configuración")
        print("3. Abre el archivo APK e instala")
        print("4. ¡Disfruta tu app!")
        
        return 0
    else:
        print("\n" + "="*60)
        print("ERROR: No se pudo generar el APK")
        print("="*60)
        print("\nPosibles soluciones:")
        print("1. Asegúrate de que Flutter esté actualizado: flutter upgrade")
        print("2. Verifica Android SDK: flutter doctor")
        print("3. Intenta manualmente en el directorio:")
        print(f"   cd {flutter_dir}")
        print("   flutter build apk --debug")
        
        return 1

if __name__ == "__main__":
    original_dir = os.getcwd()
    try:
        exit_code = main()
    finally:
        os.chdir(original_dir)
    
    input("\nPresiona Enter para salir...")
    exit(exit_code)
