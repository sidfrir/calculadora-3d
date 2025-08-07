import flet as ft
import threading
import webbrowser
from main import main

def create_web_app():
    """Crear aplicación web optimizada para móviles"""
    print("🚀 Iniciando Calculadora 3D Pro - Versión Web")
    print("📱 Optimizada para navegadores móviles y de escritorio")
    print("🌐 Accesible desde cualquier dispositivo en la red local")
    
    def web_main(page: ft.Page):
        # Configuración específica para web/móvil
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.title = "Calculadora 3D Pro - Web"
        page.scroll = ft.ScrollMode.AUTO
        
        # Configuración responsiva
        page.adaptive = True
        
        # Llamar a la función principal
        main(page)
    
    # Iniciar aplicación web
    ft.app(target=web_main, port=8080, view=ft.AppView.WEB_BROWSER)

def run_web_server():
    """Ejecutar servidor web"""
    try:
        print("=" * 50)
        print("🎯 CALCULADORA 3D PRO - SERVIDOR WEB")
        print("=" * 50)
        print("")
        print("✅ Aplicación original completa disponible")
        print("✅ Compatible con dispositivos móviles")
        print("✅ Acceso desde navegador web")
        print("")
        print("📱 Para usar en móvil:")
        print("   1. Conecta tu dispositivo a la misma red WiFi")
        print("   2. Abre el navegador en tu móvil")
        print("   3. Ve a la dirección que aparecerá abajo")
        print("")
        print("🖥️  Para usar en PC:")
        print("   1. Se abrirá automáticamente en tu navegador")
        print("   2. También puedes ir a http://localhost:8080")
        print("")
        print("⚠️  IMPORTANTE: Mantén esta ventana abierta")
        print("   El servidor se cerrará si cierras esta ventana")
        print("")
        print("🔗 Iniciando servidor...")
        print("")
        
        # Crear y ejecutar la aplicación web
        create_web_app()
        
    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        print("🛑 Servidor detenido por el usuario")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ Error al iniciar servidor: {e}")
        print("\n🔧 Soluciones posibles:")
        print("   1. Verificar que el puerto 8080 esté libre")
        print("   2. Ejecutar como administrador")
        print("   3. Cambiar el puerto en el código")
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    run_web_server()
