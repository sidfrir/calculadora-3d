"""
Generador definitivo de APK usando Flet
"""
import subprocess
import os
import sys
import time
import tempfile
import shutil

def main():
    print("="*70)
    print(" GENERADOR DE APK - CALCULADORA 3D PRO ")
    print("="*70)
    
    # Paso 1: Limpiar y preparar
    print("\n[1/4] Preparando entorno...")
    
    # Verificar que main_mobile.py existe
    if not os.path.exists("main_mobile.py"):
        print("ERROR: main_mobile.py no encontrado")
        return 1
    
    # Paso 2: Intentar con flet pack primero (más directo)
    print("\n[2/4] Intentando empaquetado con Flet Pack...")
    
    result = subprocess.run(
        [".venv\\Scripts\\flet", "pack", "main_mobile.py", 
         "--name", "Calculadora3D",
         "--product-name", "Calculadora 3D Pro",
         "--product-version", "1.0.0",
         "--file-description", "Calculadora de costos para impresion 3D"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Empaquetado exitoso")
        
        # Buscar el ejecutable generado
        if os.path.exists("dist"):
            files = os.listdir("dist")
            print(f"Archivos generados: {files}")
            
            # Si hay un .exe, intentar convertirlo a APK
            exe_file = None
            for f in files:
                if f.endswith(".exe"):
                    exe_file = f
                    break
            
            if exe_file:
                print(f"✓ Ejecutable generado: {exe_file}")
                print("\nNOTA: Se generó un ejecutable Windows.")
                print("Para Android necesitas compilar en un entorno Linux/Mac")
                print("o usar GitHub Actions como se explica en SOLUCION_APK_FINAL.md")
    
    # Paso 3: Intentar build APK normal
    print("\n[3/4] Intentando build APK con Flet...")
    
    # Configurar variables de entorno
    os.environ['FLET_BUILD_MODE'] = 'release'
    os.environ['FLET_MODULE'] = 'main_mobile'
    
    # Ejecutar build
    print("Ejecutando: flet build apk")
    print("(Esto puede tomar varios minutos...)")
    
    process = subprocess.Popen(
        [".venv\\Scripts\\flet", "build", "apk"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    # Esperar y mostrar progreso
    start_time = time.time()
    while True:
        output = process.stdout.readline()
        if output:
            print(output.strip())
        
        if process.poll() is not None:
            break
            
        # Timeout después de 10 minutos
        if time.time() - start_time > 600:
            print("\nTimeout: El build está tardando demasiado")
            process.terminate()
            break
    
    # Verificar resultado
    if process.returncode == 0:
        print("\n✓ Build completado")
        
        # Paso 4: Buscar el APK
        print("\n[4/4] Buscando APK generado...")
        
        # Buscar en el directorio temporal
        temp_dir = tempfile.gettempdir()
        apk_found = False
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(".apk"):
                    apk_path = os.path.join(root, file)
                    print(f"✓ APK encontrado: {apk_path}")
                    
                    # Copiar a directorio actual
                    dest = "CALCULADORA_3D_PRO.apk"
                    shutil.copy2(apk_path, dest)
                    
                    size_mb = os.path.getsize(dest) / (1024 * 1024)
                    
                    print("\n" + "="*70)
                    print(" ✓ APK GENERADO EXITOSAMENTE ")
                    print("="*70)
                    print(f"\nArchivo: {dest}")
                    print(f"Tamaño: {size_mb:.2f} MB")
                    print(f"Ubicación: {os.path.abspath(dest)}")
                    print("\n¡Listo para instalar en Android!")
                    
                    apk_found = True
                    break
            
            if apk_found:
                break
        
        if not apk_found:
            print("\nNo se encontró el APK en las ubicaciones esperadas")
            print("Verifica manualmente en %TEMP%")
    else:
        print(f"\nBuild falló con código: {process.returncode}")
    
    # Información adicional
    print("\n" + "="*70)
    print(" ALTERNATIVAS SI NO FUNCIONA ")
    print("="*70)
    print("""
1. USA GITHUB ACTIONS (Recomendado):
   - Sube tu código a GitHub
   - Usa el workflow en SOLUCION_APK_FINAL.md
   - El APK se genera automáticamente

2. USA GOOGLE COLAB:
   - Sube tu proyecto a Google Drive
   - Ejecuta el build en Colab (Linux)
   - Descarga el APK generado

3. USA UNA VM LINUX:
   - Instala VirtualBox con Ubuntu
   - Instala Flutter y Flet
   - Compila desde Linux

4. SERVICIO ONLINE:
   - https://build.flet.dev
   - Sube tu proyecto
   - Descarga el APK
    """)
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nBuild cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
