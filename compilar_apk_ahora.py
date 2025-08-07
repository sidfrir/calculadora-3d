"""
Compila el APK después de arreglar Gradle
"""
import subprocess
import os
import shutil
import sys

flutter_dir = r"C:\Users\Rolando\AppData\Local\Temp\flet_flutter_build_lyMX53e6Bc"
project_dir = r"d:\datos\proyectos para la agencia\PROGRAMA CALCULADORA IMPRESORA 3D"

def compile_apk():
    print("="*60)
    print("COMPILANDO APK - CALCULADORA 3D PRO")
    print("="*60)
    
    os.chdir(flutter_dir)
    
    # Limpiar
    print("\n1. Limpiando proyecto...")
    subprocess.run(["flutter", "clean"], capture_output=True)
    
    # Obtener dependencias
    print("2. Obteniendo dependencias...")
    subprocess.run(["flutter", "pub", "get"], capture_output=True)
    
    # Compilar APK
    print("3. Compilando APK (esto puede tomar 5-10 minutos)...")
    print("   Por favor espera...\n")
    
    result = subprocess.run(
        ["flutter", "build", "apk", "--debug"],
        capture_output=False,
        text=True
    )
    
    if result.returncode == 0:
        # Buscar APK
        apk_paths = [
            os.path.join(flutter_dir, "build", "app", "outputs", "flutter-apk", "app-debug.apk"),
            os.path.join(flutter_dir, "build", "app", "outputs", "apk", "debug", "app-debug.apk")
        ]
        
        apk_found = None
        for path in apk_paths:
            if os.path.exists(path):
                apk_found = path
                break
        
        if apk_found:
            dest = os.path.join(project_dir, "CALCULADORA_3D_PRO.apk")
            shutil.copy2(apk_found, dest)
            
            size_mb = os.path.getsize(dest) / (1024 * 1024)
            
            print("\n" + "="*60)
            print("✓ APK GENERADO EXITOSAMENTE!")
            print("="*60)
            print(f"\nArchivo: CALCULADORA_3D_PRO.apk")
            print(f"Ubicación: {dest}")
            print(f"Tamaño: {size_mb:.2f} MB")
            print("\n¡Listo para instalar en tu Android!")
            return 0
        else:
            print("\nERROR: APK compilado pero no encontrado")
            return 1
    else:
        print("\nERROR: Falló la compilación")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(compile_apk())
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
