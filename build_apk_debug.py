"""
Build APK con diagnóstico detallado
"""
import subprocess
import os
import sys
import tempfile
import shutil
import time

def check_flutter():
    """Verifica instalación de Flutter"""
    try:
        result = subprocess.run(["flutter", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Flutter instalado correctamente")
            return True
    except:
        pass
    print("✗ Flutter no encontrado")
    return False

def check_android_sdk():
    """Verifica Android SDK"""
    android_home = os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT')
    if android_home and os.path.exists(android_home):
        print(f"✓ Android SDK encontrado en: {android_home}")
        return True
    print("✗ Android SDK no configurado")
    return False

def build_with_flutter_direct():
    """Intenta build directo con Flutter"""
    print("\n" + "="*60)
    print("INTENTANDO BUILD DIRECTO CON FLUTTER")
    print("="*60)
    
    # Buscar el directorio temporal de Flet
    temp_dirs = []
    temp_path = tempfile.gettempdir()
    
    for item in os.listdir(temp_path):
        if item.startswith("flet_flutter_build"):
            full_path = os.path.join(temp_path, item)
            if os.path.isdir(full_path):
                temp_dirs.append(full_path)
                print(f"Encontrado directorio Flutter: {full_path}")
    
    if not temp_dirs:
        print("No se encontraron directorios de build de Flet")
        print("\nCreando nuevo build con Flet...")
        
        # Ejecutar flet build para crear el proyecto Flutter
        subprocess.run([sys.executable, "-m", "flet", "pack", "--help"], capture_output=True)
        result = subprocess.run(
            [".venv\\Scripts\\flet", "create", "build_temp"],
            capture_output=True,
            text=True
        )
        
    # Si hay directorios, usar el más reciente
    if temp_dirs:
        latest_dir = max(temp_dirs, key=os.path.getmtime)
        print(f"\nUsando directorio: {latest_dir}")
        
        # Navegar al directorio y ejecutar flutter build
        os.chdir(latest_dir)
        
        print("\nEjecutando: flutter build apk --release")
        result = subprocess.run(
            ["flutter", "build", "apk", "--release"],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            # Buscar el APK generado
            apk_path = os.path.join(latest_dir, "build", "app", "outputs", "flutter-apk", "app-release.apk")
            if os.path.exists(apk_path):
                print(f"\n✓ APK GENERADO: {apk_path}")
                
                # Copiar a directorio principal
                dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CALCULADORA_3D_PRO.apk")
                shutil.copy2(apk_path, dest)
                print(f"✓ APK copiado a: {dest}")
                return True
    
    return False

def main():
    print("DIAGNÓSTICO DE BUILD APK - CALCULADORA 3D PRO")
    print("-" * 60)
    
    # Verificar requisitos
    print("\nVerificando requisitos:")
    has_flutter = check_flutter()
    has_android = check_android_sdk()
    
    if not has_flutter:
        print("\n⚠ NECESITAS INSTALAR FLUTTER:")
        print("1. Descarga Flutter: https://flutter.dev/docs/get-started/install/windows")
        print("2. Extrae en C:\\flutter")
        print("3. Agrega C:\\flutter\\bin al PATH")
        return 1
    
    if not has_android:
        print("\n⚠ ANDROID SDK NO CONFIGURADO")
        print("Continuando de todos modos...")
    
    # Intentar build con Flutter directo
    if build_with_flutter_direct():
        print("\n" + "="*60)
        print("✓ BUILD COMPLETADO EXITOSAMENTE")
        print("="*60)
        return 0
    
    # Si no funciona, dar instrucciones manuales
    print("\n" + "="*60)
    print("INSTRUCCIONES PARA BUILD MANUAL:")
    print("="*60)
    print("""
    1. Ejecuta: .venv\\Scripts\\flet build apk
    2. Espera a que termine (aunque no muestre el APK)
    3. Ve a: %TEMP%
    4. Busca carpetas que empiecen con 'flet_flutter_build'
    5. Entra a la más reciente
    6. Ejecuta: flutter build apk --release
    7. El APK estará en: build\\app\\outputs\\flutter-apk\\app-release.apk
    """)
    
    return 1

if __name__ == "__main__":
    original_dir = os.getcwd()
    try:
        sys.exit(main())
    finally:
        os.chdir(original_dir)
