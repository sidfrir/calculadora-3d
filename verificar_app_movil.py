"""
Script de Verificación de App Móvil
Verifica que todos los componentes estén listos para build APK
"""

import os
import json
import sys

def print_status(item, status):
    """Imprime estado con colores"""
    icon = "✅" if status else "❌"
    print(f"{icon} {item}")

def verificar_archivos():
    """Verifica que existan todos los archivos necesarios"""
    print("\n🔍 VERIFICANDO ARCHIVOS NECESARIOS:")
    print("-" * 40)
    
    archivos_necesarios = [
        ("main_mobile.py", "Archivo principal móvil"),
        ("pyproject.toml", "Configuración del proyecto"),
        ("requirements.txt", "Dependencias"),
        ("models/database_simple.py", "Base de datos JSON"),
        ("views/calculator_view_mobile.py", "Vista calculadora móvil"),
        ("views/history_view_mobile.py", "Vista historial móvil"),
        ("views/settings_view.py", "Vista configuración"),
        ("views/home_view.py", "Vista principal"),
        ("models/settings_manager.py", "Gestor de configuración"),
        ("quotes.json", "Archivo de cotizaciones"),
        ("assets/icon.png", "Icono de la app"),
    ]
    
    todos_ok = True
    for archivo, descripcion in archivos_necesarios:
        existe = os.path.exists(archivo)
        print_status(f"{descripcion}: {archivo}", existe)
        if not existe:
            todos_ok = False
    
    return todos_ok

def verificar_configuracion():
    """Verifica la configuración del proyecto"""
    print("\n⚙️ VERIFICANDO CONFIGURACIÓN:")
    print("-" * 40)
    
    try:
        # Verificar pyproject.toml
        with open("pyproject.toml", "r", encoding="utf-8") as f:
            contenido = f.read()
            
        checks = [
            ("module = \"main_mobile\"" in contenido, "Módulo principal: main_mobile"),
            ("name = \"Calculadora 3D Pro\"" in contenido, "Nombre de app configurado"),
            ("org = \"com.miempresa\"" in contenido, "Organización configurada"),
            ("version = \"2.0.0\"" in contenido, "Versión 2.0.0"),
            ("\"android.permission.WRITE_EXTERNAL_STORAGE\"" in contenido, "Permisos de almacenamiento"),
        ]
        
        todos_ok = True
        for check, descripcion in checks:
            print_status(descripcion, check)
            if not check:
                todos_ok = False
                
        return todos_ok
    except Exception as e:
        print(f"❌ Error leyendo configuración: {e}")
        return False

def verificar_base_datos():
    """Verifica que la base de datos JSON funcione"""
    print("\n💾 VERIFICANDO BASE DE DATOS:")
    print("-" * 40)
    
    try:
        # Verificar archivo quotes.json
        if not os.path.exists("quotes.json"):
            with open("quotes.json", "w") as f:
                json.dump([], f)
            print("✅ Archivo quotes.json creado")
        else:
            with open("quotes.json", "r") as f:
                data = json.load(f)
            print(f"✅ Base de datos JSON operativa ({len(data)} cotizaciones)")
        
        # Verificar carpeta de datos
        if not os.path.exists("data"):
            os.makedirs("data")
            print("✅ Carpeta data creada")
        else:
            print("✅ Carpeta data existe")
            
        return True
    except Exception as e:
        print(f"❌ Error con base de datos: {e}")
        return False

def verificar_dependencias():
    """Verifica las dependencias instaladas"""
    print("\n📦 VERIFICANDO DEPENDENCIAS:")
    print("-" * 40)
    
    try:
        import flet
        print(f"✅ Flet instalado (versión {flet.version.version})")
        
        # Verificar versión correcta
        if flet.version.version.startswith("0.24"):
            print("✅ Versión de Flet compatible (0.24.x)")
        else:
            print(f"⚠️ Versión de Flet puede no ser compatible: {flet.version.version}")
            
        return True
    except ImportError:
        print("❌ Flet no está instalado")
        return False

def probar_app_movil():
    """Intenta ejecutar la app móvil brevemente"""
    print("\n🚀 PROBANDO APP MÓVIL:")
    print("-" * 40)
    
    try:
        # Importar módulos principales
        from main_mobile import main
        from models.database_simple import DatabaseManager
        from views.calculator_view_mobile import CalculatorViewMobile
        from views.history_view_mobile import HistoryViewMobile
        
        print("✅ Todos los módulos se importan correctamente")
        
        # Probar base de datos
        db = DatabaseManager()
        print(f"✅ Base de datos inicializada ({len(db.get_all_quotes())} cotizaciones)")
        
        return True
    except Exception as e:
        print(f"❌ Error al probar la app: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("=" * 50)
    print("🔧 VERIFICACIÓN DE APP MÓVIL - CALCULADORA 3D PRO")
    print("=" * 50)
    
    resultados = {
        "Archivos": verificar_archivos(),
        "Configuración": verificar_configuracion(),
        "Base de datos": verificar_base_datos(),
        "Dependencias": verificar_dependencias(),
        "App móvil": probar_app_movil(),
    }
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIÓN:")
    print("-" * 40)
    
    todos_ok = True
    for componente, estado in resultados.items():
        print_status(componente, estado)
        if not estado:
            todos_ok = False
    
    print("\n" + "=" * 50)
    if todos_ok:
        print("✅ ¡TODO LISTO! La app está preparada para build APK")
        print("\nEjecuta: flet build apk --verbose")
    else:
        print("⚠️ HAY PROBLEMAS que resolver antes del build")
        print("\nRevisa los errores arriba y corrige antes de continuar")
    print("=" * 50)
    
    return 0 if todos_ok else 1

if __name__ == "__main__":
    sys.exit(main())
