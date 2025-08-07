import flet as ft
from views.home_view import HomeView
from views.calculator_view import CalculatorView
from views.history_view import HistoryView
from views.settings_view import SettingsView
from views.projects_view import ProjectsView
from views.clients_view import ClientsView
from models.settings_manager import SettingsManager
from models.database_mobile import DatabaseManager
from models.user_preferences import UserPreferences
from utils.themes import CustomThemes

def main(page: ft.Page):
    page.title = "Calculadora 3D Pro"
    page.theme_mode = ft.ThemeMode.SYSTEM
    # Configurar ventana usando la nueva API
    page.window.width = 900
    page.window.height = 700
    page.padding = 0
    
    # Instancia única de los gestores
    settings_manager = SettingsManager()
    db_manager = DatabaseManager()
    user_preferences = UserPreferences()

    # Aplicar tema guardado al inicio
    theme = settings_manager.get('theme_mode')
    CustomThemes.apply_theme(page, theme, user_preferences)

    # Añadir FilePicker al overlay para que esté disponible en toda la app
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def route_change(route):
        page.views.clear()
        # Pasamos los gestores a las vistas que los necesitan
        if page.route == "/":
            page.views.append(HomeView(page))
        elif page.route == "/calculator":
            page.views.append(CalculatorView(page, settings_manager, db_manager))
        elif page.route == "/history":
            page.views.append(HistoryView(page, db_manager, file_picker))
        elif page.route == "/settings":
            page.views.append(SettingsView(page, settings_manager))
        elif page.route == "/projects":
            page.views.append(ProjectsView(page))
        elif page.route == "/clients":
            page.views.append(ClientsView(page))
        
        # Actualizar el índice del navigation bar según la ruta
        route_index = {"/": 0, "/calculator": 1, "/history": 2, "/settings": 3}
        if page.route in route_index:
            page.navigation_bar.selected_index = route_index[page.route]
        
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    def on_navigation_change(e):
        routes = ['/', '/calculator', '/history', '/settings']
        selected_route = routes[e.control.selected_index]
        page.go(selected_route)
    
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon="home_outlined", 
                selected_icon="home", 
                label="Inicio"
            ),
            ft.NavigationBarDestination(
                icon="calculate_outlined", 
                selected_icon="calculate", 
                label="Calcular"
            ),
            ft.NavigationBarDestination(
                icon="history_outlined", 
                selected_icon="history", 
                label="Historial"
            ),
            ft.NavigationBarDestination(
                icon="settings_outlined", 
                selected_icon="settings", 
                label="Ajustes"
            ),
        ],
        on_change=on_navigation_change,
        selected_index=0,
    )

    page.go(page.route)

ft.app(target=main, assets_dir="assets")
