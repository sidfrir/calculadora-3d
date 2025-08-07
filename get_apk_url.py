import socket
import webbrowser
import subprocess
import time

def get_local_ip():
    """Obtener IP local automáticamente"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.1.100"  # IP por defecto

def main():
    print("🚀 CREADOR DE APK AUTOMÁTICO")
    print("=" * 50)
    
    # Obtener IP
    ip = get_local_ip()
    url = f"http://{ip}:8080"
    
    print(f"📱 Tu IP local es: {ip}")
    print(f"🌐 URL de tu aplicación: {url}")
    print()
    
    print("📋 OPCIONES PARA CREAR TU APK:")
    print()
    print("1️⃣  MÉTODO AUTOMÁTICO (Recomendado)")
    print(f"   • Ve a: https://www.websitetoapk.com/")
    print(f"   • Pega esta URL: {url}")
    print(f"   • Nombre: Calculadora 3D Pro")
    print(f"   • ¡Descarga tu APK!")
    print()
    print("2️⃣  MÉTODO PWA (Más fácil)")
    print(f"   • Abre Chrome en tu móvil")
    print(f"   • Ve a: {url}")
    print(f"   • Menú → 'Instalar aplicación'")
    print(f"   • ¡Listo!")
    print()
    
    # Preguntar qué hacer
    choice = input("¿Qué quieres hacer?\n"
                  "1 - Abrir WebsiteToApk automáticamente\n"
                  "2 - Iniciar servidor web\n"
                  "3 - Ver instrucciones detalladas\n"
                  "Escoge (1/2/3): ")
    
    if choice == "1":
        print("\n🌐 Abriendo WebsiteToApk...")
        apk_url = f"https://www.websitetoapk.com/?url={url}&title=Calculadora%203D%20Pro"
        webbrowser.open(apk_url)
        print("✅ WebsiteToApk abierto en tu navegador")
        print(f"📝 URL pre-configurada con: {url}")
        
    elif choice == "2":
        print("\n🚀 Iniciando servidor web...")
        print(f"📱 Tu aplicación estará en: {url}")
        print("⚠️  MANTÉN ESTA VENTANA ABIERTA")
        print()
        try:
            subprocess.run([".venv\\Scripts\\python", "run_web_server.py"])
        except KeyboardInterrupt:
            print("\n🛑 Servidor detenido")
            
    elif choice == "3":
        print("\n📖 Abriendo instrucciones detalladas...")
        with open("CREAR_APK_FACILMENTE.md", "r", encoding="utf-8") as f:
            print(f.read())
    
    else:
        print("\n❌ Opción inválida")
        
    print(f"\n💡 RECUERDA: Tu URL es {url}")
    print("   Úsala en cualquier herramienta de creación de APK")
    input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
