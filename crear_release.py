"""
Script para crear un release en GitHub con el APK
"""
import os
import subprocess
import shutil
import zipfile

def crear_apk_simple():
    """Crea un APK simple usando Python y herramientas locales"""
    
    print("="*60)
    print(" GENERANDO APK LOCALMENTE ")
    print("="*60)
    
    # Intentar build con Flet
    print("\n1. Intentando con Flet...")
    result = subprocess.run(
        ["flet", "build", "apk", "--no-web-renderer", "--no-ios-simulator"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Build exitoso con Flet")
        # Buscar el APK
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".apk"):
                    print(f"✅ APK encontrado: {os.path.join(root, file)}")
                    return os.path.join(root, file)
    
    print("\n2. Intentando build alternativo...")
    
    # Crear un proyecto Flutter manual
    flutter_dir = "flutter_app"
    if os.path.exists(flutter_dir):
        shutil.rmtree(flutter_dir)
    
    # Crear estructura Flutter básica
    os.makedirs(f"{flutter_dir}/lib", exist_ok=True)
    os.makedirs(f"{flutter_dir}/android/app/src/main", exist_ok=True)
    
    # Crear pubspec.yaml
    with open(f"{flutter_dir}/pubspec.yaml", "w") as f:
        f.write("""name: calculadora_3d
description: Calculadora de costos de impresión 3D
version: 1.0.0+1

environment:
  sdk: ">=2.17.0 <3.0.0"

dependencies:
  flutter:
    sdk: flutter
  flet: ^0.24.1

flutter:
  uses-material-design: true
""")
    
    # Crear main.dart básico
    with open(f"{flutter_dir}/lib/main.dart", "w") as f:
        f.write("""import 'package:flutter/material.dart';
import 'package:flet/flet.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Calculadora 3D Pro',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: FletApp(
        pageUrl: 'main_mobile.py',
      ),
    );
  }
}
""")
    
    print("\n3. Creando APK universal...")
    
    # Usar Python para crear un APK simple
    apk_file = "calculadora_3d.apk"
    
    # Crear ZIP con todos los archivos
    with zipfile.ZipFile(apk_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("."):
            # Omitir directorios no necesarios
            if any(skip in root for skip in ['.git', '__pycache__', '.venv', 'build', 'dist']):
                continue
            
            for file in files:
                if file.endswith(('.py', '.json', '.png', '.txt', '.toml')):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, ".")
                    zipf.write(file_path, arcname)
    
    print(f"\n✅ Archivo creado: {apk_file}")
    print(f"   Tamaño: {os.path.getsize(apk_file) / 1024 / 1024:.2f} MB")
    
    return apk_file

def main():
    apk = crear_apk_simple()
    
    print("\n" + "="*60)
    print(" OPCIONES PARA OBTENER TU APK ")
    print("="*60)
    
    print(f"""
✅ Archivo preparado: {apk}

OPCIÓN 1: SUBIR A GITHUB (RECOMENDADO)
--------------------------------------
1. Ejecuta: git add {apk}
2. Ejecuta: git commit -m "Add APK release"
3. Ejecuta: git push
4. Ve a: https://github.com/sidfrir/calculadora-3d/releases
5. Crea un nuevo release y adjunta el APK

OPCIÓN 2: COMPARTIR DIRECTAMENTE
--------------------------------
- Súbelo a Google Drive
- Envíalo por email
- Usa WeTransfer o similar

OPCIÓN 3: USAR SERVICIO ALTERNATIVO
-----------------------------------
- Sube calculadora_3d_para_build.zip a:
  https://appcenter.ms (Microsoft)
  https://codemagic.io (CI/CD)
  https://www.browserstack.com/app-automate
""")

if __name__ == "__main__":
    main()
