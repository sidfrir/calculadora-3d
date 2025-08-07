import flet as ft
from main import main

def create_pwa():
    """Crear Progressive Web App que se puede instalar como app nativa"""
    
    def pwa_main(page: ft.Page):
        # Configuración PWA
        page.title = "Calculadora 3D Pro"
        page.web_app_manifest = {
            "name": "Calculadora 3D Pro",
            "short_name": "3D Calc Pro",
            "description": "Calculadora profesional para impresión 3D",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#2196F3",
            "theme_color": "#2196F3",
            "icons": [
                {
                    "src": "icon-192.png",
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": "icon-512.png", 
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }
        
        # Configuración para móvil
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.scroll = ft.ScrollMode.AUTO
        page.adaptive = True
        
        # Llamar a la función principal
        main(page)
    
    print("🚀 Iniciando Calculadora 3D Pro - PWA")
    print("📱 Se puede instalar como app nativa en móviles")
    print("🌐 Accesible en: http://localhost:8080")
    print("📲 Para instalar en móvil: Menú del navegador > 'Instalar app'")
    
    # Crear PWA
    ft.app(
        target=pwa_main, 
        port=8080, 
        assets_dir="assets",
        web_renderer=ft.WebRenderer.HTML
    )

if __name__ == "__main__":
    create_pwa()
