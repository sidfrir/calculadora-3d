import subprocess
import os
import requests
import json

def try_flutter_direct():
    """Intentar crear APK directamente con Flutter"""
    print("🔨 Intentando crear APK directamente con Flutter...")
    
    # Verificar Flutter
    try:
        result = subprocess.run(['flutter', '--version'], capture_output=True, text=True)
        print(f"✅ Flutter encontrado: {result.stdout.split()[1] if result.stdout else 'version unknown'}")
        
        # Crear proyecto Flutter básico
        if not os.path.exists('flutter_app'):
            print("📁 Creando proyecto Flutter...")
            subprocess.run(['flutter', 'create', 'flutter_app'], check=True)
            print("✅ Proyecto Flutter creado")
        
        # Cambiar al directorio del proyecto
        os.chdir('flutter_app')
        
        # Modificar main.dart para mostrar WebView a la aplicación
        main_dart = '''
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Calculadora 3D Pro',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  late final WebViewController _controller;

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..loadRequest(Uri.parse('http://192.168.1.100:8080')); // Cambiar por tu IP
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Calculadora 3D Pro'),
        backgroundColor: Color(0xFF2196F3),
      ),
      body: WebViewWidget(controller: _controller),
    );
  }
}
'''
        
        with open('lib/main.dart', 'w') as f:
            f.write(main_dart)
        
        # Agregar dependencia webview
        pubspec = '''
name: calculadora_3d_pro
description: Calculadora profesional para impresión 3D
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  webview_flutter: ^4.4.2

dev_dependencies:
  flutter_test:
    sdk: flutter

flutter:
  uses-material-design: true
'''
        
        with open('pubspec.yaml', 'w') as f:
            f.write(pubspec)
        
        # Obtener dependencias
        print("📦 Obteniendo dependencias...")
        subprocess.run(['flutter', 'pub', 'get'], check=True)
        
        # Construir APK
        print("🏗️  Construyendo APK...")
        result = subprocess.run(['flutter', 'build', 'apk'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ APK creado exitosamente!")
            apk_path = 'build/app/outputs/flutter-apk/app-release.apk'
            if os.path.exists(apk_path):
                # Copiar APK a directorio principal
                os.chdir('..')  # Volver al directorio principal
                import shutil
                shutil.copy(os.path.join('flutter_app', apk_path), 'Calculadora3DPro.apk')
                print(f"📱 APK copiado como: Calculadora3DPro.apk")
                return True
            else:
                print(f"❌ APK no encontrado en {apk_path}")
        else:
            print(f"❌ Error al construir APK: {result.stderr}")
        
        os.chdir('..')  # Volver al directorio principal
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error con Flutter: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def create_cordova_apk():
    """Crear APK usando Apache Cordova"""
    print("📱 Intentando crear APK con Apache Cordova...")
    
    try:
        # Verificar Cordova
        result = subprocess.run(['cordova', '--version'], capture_output=True, text=True)
        print(f"✅ Cordova encontrado: {result.stdout.strip()}")
        
        # Crear proyecto Cordova
        if not os.path.exists('cordova_app'):
            subprocess.run(['cordova', 'create', 'cordova_app', 'com.empresa.calculadora3dpro', 'Calculadora3DPro'], check=True)
        
        os.chdir('cordova_app')
        
        # Agregar plataforma Android
        subprocess.run(['cordova', 'platform', 'add', 'android'], check=True)
        
        # Crear index.html que redirija a la aplicación
        index_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Calculadora 3D Pro</title>
    <style>
        body { margin: 0; padding: 0; font-family: Arial; }
        iframe { width: 100%; height: 100vh; border: none; }
        .loading { text-align: center; padding: 50px; }
    </style>
</head>
<body>
    <div class="loading">
        <h2>🧮 Calculadora 3D Pro</h2>
        <p>Conectando con el servidor...</p>
        <p><small>Asegúrate de que el servidor esté ejecutándose en tu PC</small></p>
    </div>
    <iframe src="http://192.168.1.100:8080" onload="document.querySelector('.loading').style.display='none'"></iframe>
    
    <script>
        // Detectar IP local automáticamente si es posible
        setTimeout(() => {
            const possibleIPs = ['192.168.1.100', '192.168.0.100', '10.0.0.100'];
            // Intentar conectar a diferentes IPs comunes
        }, 2000);
    </script>
</body>
</html>
        '''
        
        with open('www/index.html', 'w') as f:
            f.write(index_html)
        
        # Construir APK
        print("🏗️  Construyendo APK con Cordova...")
        result = subprocess.run(['cordova', 'build', 'android'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ APK creado con Cordova!")
            # Buscar el APK generado
            apk_files = []
            for root, dirs, files in os.walk('platforms/android'):
                for file in files:
                    if file.endswith('.apk'):
                        apk_files.append(os.path.join(root, file))
            
            if apk_files:
                os.chdir('..')
                import shutil
                shutil.copy(apk_files[0], 'Calculadora3DPro-Cordova.apk')
                print(f"📱 APK copiado como: Calculadora3DPro-Cordova.apk")
                return True
        
        os.chdir('..')
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error con Cordova: {e}")
        if os.getcwd().endswith('cordova_app'):
            os.chdir('..')
        return False
    except Exception as e:
        print(f"❌ Error inesperado con Cordova: {e}")
        if os.getcwd().endswith('cordova_app'):
            os.chdir('..')
        return False

def main():
    """Función principal para crear APK"""
    print("🚀 CREADOR DE APK FINAL")
    print("=" * 50)
    print("📱 Intentando múltiples métodos para crear APK...")
    print()
    
    # Método 1: Flutter directo
    if try_flutter_direct():
        print("\n🎉 ¡APK creado exitosamente con Flutter!")
        return
    
    # Método 2: Cordova
    if create_cordova_apk():
        print("\n🎉 ¡APK creado exitosamente con Cordova!")
        return
    
    # Si ningún método funciona, crear instrucciones
    print("\n📝 Creando instrucciones alternativas...")
    
    instructions = """
# 📱 INSTRUCCIONES PARA CREAR APK MANUALMENTE

## Método 1: Usando ApkTool Online (Más Fácil)
1. Ve a: https://www.websitetoapk.com/ o https://appsgeyser.com/
2. Ingresa la URL: http://[TU_IP]:8080
3. Configura:
   - Nombre: "Calculadora 3D Pro"
   - Ícono: Sube el archivo assets/icon.png
   - Orientación: Portrait
4. Genera y descarga el APK
5. Instala en tu móvil

## Método 2: PWA Instalable (Recomendado)
1. Ejecuta: `.venv\\Scripts\\python run_web_server.py`
2. En tu móvil, abre Chrome
3. Ve a: http://[IP_DE_TU_PC]:8080
4. Menú > "Instalar aplicación"
5. ¡Listo! Tendrás la app en tu pantalla de inicio

## Método 3: Usando Capacitor
1. Instala Node.js y Capacitor: `npm install -g @capacitor/cli`
2. Crea proyecto: `npx cap init`
3. Agrega Android: `npx cap add android`
4. Construye: `npx cap build android`

## ✅ Tu aplicación está lista para usar!
El servidor web funciona perfectamente para acceso móvil.
"""
    
    with open("CREAR_APK_MANUAL.txt", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("✅ Instrucciones creadas en: CREAR_APK_MANUAL.txt")
    print("\n📱 RECOMENDACIÓN:")
    print("La versión web es la mejor opción - funciona igual que un APK")
    print("Ejecuta: `.venv\\Scripts\\python run_web_server.py`")
    print("Y accede desde tu móvil a: http://[IP_PC]:8080")

if __name__ == "__main__":
    main()
