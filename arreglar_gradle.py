"""
Arregla la configuración de Gradle para compilar el APK
"""
import os
import re

# Directorio del proyecto Flutter
flutter_dir = r"C:\Users\Rolando\AppData\Local\Temp\flet_flutter_build_lyMX53e6Bc"

def fix_build_gradle():
    """Arregla android/app/build.gradle"""
    build_gradle = os.path.join(flutter_dir, "android", "app", "build.gradle")
    
    if not os.path.exists(build_gradle):
        print(f"ERROR: No se encontró {build_gradle}")
        return False
    
    print(f"Arreglando {build_gradle}...")
    
    with open(build_gradle, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup
    with open(build_gradle + '.bak', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Arreglar compileSdkVersion
    content = re.sub(r'compileSdkVersion\s+flutter\.compileSdkVersion', 
                     'compileSdkVersion 33', content)
    content = re.sub(r'compileSdkVersion\s+\d+', 
                     'compileSdkVersion 33', content)
    
    # Arreglar minSdkVersion
    content = re.sub(r'minSdkVersion\s+flutter\.minSdkVersion', 
                     'minSdkVersion 21', content)
    
    # Arreglar targetSdkVersion
    content = re.sub(r'targetSdkVersion\s+flutter\.targetSdkVersion', 
                     'targetSdkVersion 33', content)
    
    # Agregar namespace si no existe
    if 'namespace "' not in content:
        content = content.replace('android {', 
                                  'android {\n    namespace "com.flet.calculadora3d"')
    
    with open(build_gradle, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ build.gradle arreglado")
    return True

def fix_gradle_properties():
    """Arregla android/gradle.properties"""
    gradle_props = os.path.join(flutter_dir, "android", "gradle.properties")
    
    print(f"Arreglando {gradle_props}...")
    
    properties = """org.gradle.jvmargs=-Xmx1536M
android.useAndroidX=true
android.enableJetifier=true
android.enableR8=true
"""
    
    with open(gradle_props, 'w', encoding='utf-8') as f:
        f.write(properties)
    
    print("✓ gradle.properties arreglado")
    return True

def fix_gradle_wrapper():
    """Actualiza gradle wrapper"""
    gradle_wrapper = os.path.join(flutter_dir, "android", "gradle", "wrapper", "gradle-wrapper.properties")
    
    if os.path.exists(gradle_wrapper):
        print(f"Actualizando Gradle wrapper...")
        
        with open(gradle_wrapper, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Actualizar a Gradle 7.6.1 (compatible con SDK 33)
        content = re.sub(r'gradle-\d+\.\d+(\.\d+)?-', 'gradle-7.6.1-', content)
        
        with open(gradle_wrapper, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ Gradle wrapper actualizado")
    
    return True

def fix_settings_gradle():
    """Arregla android/settings.gradle"""
    settings_gradle = os.path.join(flutter_dir, "android", "settings.gradle")
    
    if os.path.exists(settings_gradle):
        print(f"Arreglando {settings_gradle}...")
        
        with open(settings_gradle, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Quitar referencias problemáticas
        if "plugins {" in content:
            # Mantener solo lo esencial
            new_content = """include ':app'

def localPropertiesFile = new File(rootProject.projectDir, "local.properties")
def properties = new Properties()

assert localPropertiesFile.exists()
localPropertiesFile.withReader("UTF-8") { reader -> properties.load(reader) }

def flutterSdkPath = properties.getProperty("flutter.sdk")
assert flutterSdkPath != null, "flutter.sdk not set in local.properties"
apply from: "$flutterSdkPath/packages/flutter_tools/gradle/app_plugin_loader.gradle"
"""
            with open(settings_gradle, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✓ settings.gradle simplificado")
    
    return True

def main():
    print("="*60)
    print("ARREGLANDO CONFIGURACIÓN DE GRADLE")
    print("="*60)
    
    if not os.path.exists(flutter_dir):
        print(f"ERROR: No se encontró el directorio {flutter_dir}")
        return 1
    
    # Arreglar todos los archivos
    fix_build_gradle()
    fix_gradle_properties()
    fix_gradle_wrapper()
    fix_settings_gradle()
    
    print("\n" + "="*60)
    print("✓ CONFIGURACIÓN ARREGLADA")
    print("="*60)
    print("\nAhora ejecuta estos comandos en PowerShell:")
    print(f"\ncd '{flutter_dir}'")
    print("flutter clean")
    print("flutter pub get")
    print("flutter build apk --debug")
    print("\nO ejecuta el script 'compilar_apk_ahora.py'")
    
    return 0

if __name__ == "__main__":
    exit(main())
