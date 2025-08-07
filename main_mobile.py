import flet as ft
from views.home_view import HomeView
from views.calculator_view_mobile import CalculatorViewMobile
from views.history_view_mobile import HistoryViewMobile
from views.settings_view import SettingsView
from models.settings_manager import SettingsManager
from models.database_simple import DatabaseManager
from models.user_preferences import UserPreferences
from utils.themes import CustomThemes

def main(page: ft.Page):
    page.title = "Calculadora 3D Pro"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 0
    page.spacing = 0
    
    # Configurar ventana para móvil
    page.window.width = 400
    page.window.height = 800
    page.window.resizable = False
    
    # --- Inicializar gestores ---
    settings_manager = SettingsManager()
    db_manager = DatabaseManager()
    user_preferences = UserPreferences()
    themes = CustomThemes()
    
    # Aplicar tema guardado
    saved_theme = settings_manager.get('theme_mode', 'system')
    if saved_theme == "dark":
        page.theme_mode = ft.ThemeMode.DARK
    elif saved_theme == "light":
        page.theme_mode = ft.ThemeMode.LIGHT
    else:
        page.theme_mode = ft.ThemeMode.SYSTEM
    
    # --- Vistas ---
    home_view = HomeView(page)
    calculator_view = CalculatorViewMobile(page, settings_manager, db_manager)
    history_view = HistoryViewMobile(page, db_manager)
    settings_view = SettingsView(page, settings_manager)
    
    def route_change(route):
        page.views.clear()
        
        # Determinar qué vista mostrar
        if page.route == "/":
            page.views.append(home_view)
            page.selected_index = 0
        elif page.route == "/calculator":
            page.views.append(calculator_view)
            page.selected_index = 1
        elif page.route == "/history":
            page.views.append(history_view)
            page.selected_index = 2
        elif page.route == "/settings":
            page.views.append(settings_view)
            page.selected_index = 3
        else:
            page.views.append(home_view)
            page.selected_index = 0
            
        page.update()
    
    def on_navigation_change(e):
        selected_index = e.control.selected_index
        
        if selected_index == 0:
            page.go("/")
        elif selected_index == 1:
            page.go("/calculator")
        elif selected_index == 2:
            page.go("/history")
        elif selected_index == 3:
            page.go("/settings")
    
    # Configurar navegación
    page.on_route_change = route_change
    page.go(page.route)
    
    # --- Barra de navegación inferior ---
    navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(
                icon="home_outlined",
                selected_icon="home",
                label="Inicio"
            ),
            ft.NavigationDestination(
                icon="calculate_outlined", 
                selected_icon="calculate",
                label="Calcular"
            ),
            ft.NavigationDestination(
                icon="history_outlined",
                selected_icon="history", 
                label="Historial"
            ),
            ft.NavigationDestination(
                icon="settings_outlined",
                selected_icon="settings",
                label="Ajustes"
            ),
        ],
        on_change=on_navigation_change,
        selected_index=0,
        height=65,
        bgcolor="surface",
        indicator_color="primary",
        animation_duration=300,
    )
    
    page.navigation_bar = navigation_bar
    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
