import flet as ft
import json
import os
from datetime import datetime
import uuid

# Clase Quote simplificada
class Quote:
    def __init__(self, piece_name, weight_g, total_hours, filament_type, 
                 material_cost, print_time_cost, electricity_cost, 
                 profit_margin_percent, final_price):
        self.id = str(uuid.uuid4())
        self.piece_name = piece_name
        self.weight_g = weight_g
        self.total_hours = total_hours
        self.filament_type = filament_type
        self.material_cost = material_cost
        self.print_time_cost = print_time_cost
        self.electricity_cost = electricity_cost
        self.profit_margin_percent = profit_margin_percent
        self.final_price = final_price
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'id': self.id,
            'piece_name': self.piece_name,
            'weight_g': self.weight_g,
            'total_hours': self.total_hours,
            'filament_type': self.filament_type,
            'material_cost': self.material_cost,
            'print_time_cost': self.print_time_cost,
            'electricity_cost': self.electricity_cost,
            'profit_margin_percent': self.profit_margin_percent,
            'final_price': self.final_price,
            'timestamp': self.timestamp
        }

# Gestor de configuración simplificado
class SettingsManager:
    def __init__(self):
        self.settings_file = "settings.json"
        self.default_settings = {
            'machine_cost_per_hour': 5.0,
            'electricity_kwh_price': 0.15,
            'printer_power_watts': 200,
            'currency_symbol': '$',
            'filaments': {
                'PLA': {'price_per_kg': 25.0},
                'ABS': {'price_per_kg': 30.0},
                'PETG': {'price_per_kg': 35.0},
                'TPU': {'price_per_kg': 40.0}
            }
        }
    
    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return {**self.default_settings, **json.load(f)}
        except:
            pass
        return self.default_settings.copy()
    
    def get(self, key, default=None):
        settings = self.load_settings()
        return settings.get(key, default)

# Gestor de base de datos simplificado
class DatabaseManager:
    def __init__(self):
        self.quotes_file = "quotes.json"
        self.quotes = self.load_quotes()
    
    def load_quotes(self):
        try:
            if os.path.exists(self.quotes_file):
                with open(self.quotes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [self._dict_to_quote(q) for q in data]
        except:
            pass
        return []
    
    def _dict_to_quote(self, data):
        quote = Quote(
            data['piece_name'], data['weight_g'], data['total_hours'],
            data['filament_type'], data['material_cost'], data['print_time_cost'],
            data['electricity_cost'], data['profit_margin_percent'], data['final_price']
        )
        quote.id = data.get('id', quote.id)
        quote.timestamp = data.get('timestamp', quote.timestamp)
        return quote
    
    def save_quotes(self):
        try:
            with open(self.quotes_file, 'w', encoding='utf-8') as f:
                json.dump([q.to_dict() for q in self.quotes], f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def save_quote(self, quote_data):
        try:
            quote = Quote(**quote_data)
            self.quotes.append(quote)
            return self.save_quotes()
        except:
            return False
    
    def get_recent_quotes(self, limit=10):
        return sorted(self.quotes, key=lambda q: q.timestamp, reverse=True)[:limit]
    
    def delete_quote(self, quote_id):
        try:
            self.quotes = [q for q in self.quotes if q.id != quote_id]
            return self.save_quotes()
        except:
            return False

def main(page: ft.Page):
    page.title = "Calculadora 3D Pro"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 0
    page.spacing = 0
    
    # Configurar ventana para móvil
    page.window.width = 400
    page.window.height = 800
    page.window.resizable = False
    
    # Inicializar gestores
    settings_manager = SettingsManager()
    db_manager = DatabaseManager()
    
    # Variables globales
    current_view = "home"
    current_quote_data = None
    
    # Vista Principal
    def create_home_view():
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon("calculate", size=60, color="primary"),
                    ft.Text("Calculadora 3D Pro", size=28, weight=ft.FontWeight.BOLD, color="primary"),
                    ft.Text("Gestión profesional para impresión 3D", size=14, color="outline")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=40,
                alignment=ft.alignment.center
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon("calculate", color="primary"),
                            title=ft.Text("Calcular Costos"),
                            subtitle=ft.Text("Calcula el precio de impresión"),
                            on_click=lambda _: go_to_calculator()
                        ),
                        ft.Divider(height=1),
                        ft.ListTile(
                            leading=ft.Icon("history", color="primary"),
                            title=ft.Text("Historial"),
                            subtitle=ft.Text("Ver cotizaciones anteriores"),
                            on_click=lambda _: go_to_history()
                        ),
                        ft.Divider(height=1),
                        ft.ListTile(
                            leading=ft.Icon("settings", color="primary"),
                            title=ft.Text("Configuración"),
                            subtitle=ft.Text("Ajustar parámetros"),
                            on_click=lambda _: go_to_settings()
                        )
                    ], spacing=0),
                    padding=10
                ),
                elevation=4
            )
        ], spacing=20, scroll=ft.ScrollMode.AUTO, expand=True)
    
    # Vista Calculadora
    def create_calculator_view():
        # Campos
        piece_name = ft.TextField(label="Nombre de la pieza", border_radius=12, prefix_icon="text_fields")
        weight_g = ft.TextField(label="Peso (gramos)", keyboard_type=ft.KeyboardType.NUMBER, border_radius=12, prefix_icon="scale")
        time_h = ft.TextField(label="Horas", keyboard_type=ft.KeyboardType.NUMBER, width=150, border_radius=12, value="0")
        time_m = ft.TextField(label="Minutos", keyboard_type=ft.KeyboardType.NUMBER, width=150, border_radius=12, value="0")
        profit_margin = ft.TextField(label="Margen (%)", keyboard_type=ft.KeyboardType.NUMBER, border_radius=12, prefix_icon="percent", value="20")
        
        filament_options = []
        filaments = settings_manager.get('filaments', {})
        for name in filaments.keys():
            filament_options.append(ft.dropdown.Option(name))
        
        filament_type = ft.Dropdown(label="Filamento", options=filament_options, border_radius=12, prefix_icon="local_fire_department")
        
        # Resultados
        result_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Resultado del Cálculo", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("Complete los campos y presione Calcular", id="result_text"),
                ], spacing=8),
                padding=20
            ),
            visible=False
        )
        
        def calculate_price(e):
            nonlocal current_quote_data
            try:
                settings = settings_manager.load_settings()
                machine_cost_per_hour = float(settings['machine_cost_per_hour'])
                electricity_kwh_price = float(settings['electricity_kwh_price'])
                printer_power_watts = int(settings['printer_power_watts'])
                filament_prices = settings['filaments']

                weight = float(weight_g.value)
                hours = float(time_h.value or 0)
                minutes = float(time_m.value or 0)
                total_hours = hours + (minutes / 60)
                profit_margin_percent = float(profit_margin.value)
                selected_filament = filament_type.value

                if not all([weight_g.value, total_hours > 0, selected_filament]):
                    show_snack_bar("Por favor, completa todos los campos.", "error")
                    return

                filament_price_per_kg = float(filament_prices[selected_filament]['price_per_kg'])
                material_cost = (weight / 1000) * filament_price_per_kg
                print_time_cost = total_hours * machine_cost_per_hour
                electricity_cost = (printer_power_watts / 1000) * total_hours * electricity_kwh_price
                
                subtotal = material_cost + print_time_cost + electricity_cost
                margin_amount = subtotal * (profit_margin_percent / 100)
                final_price = subtotal + margin_amount

                currency_symbol = settings_manager.get('currency_symbol', '$')
                
                result_text = f"""Material: {currency_symbol}{material_cost:.2f}
Impresión: {currency_symbol}{print_time_cost:.2f}
Electricidad: {currency_symbol}{electricity_cost:.2f}
Subtotal: {currency_symbol}{subtotal:.2f}
Margen ({profit_margin_percent}%): {currency_symbol}{margin_amount:.2f}
PRECIO FINAL: {currency_symbol}{final_price:.2f}"""

                result_card.content.content.controls[2].value = result_text
                result_card.visible = True
                
                current_quote_data = {
                    "piece_name": piece_name.value or "Sin nombre",
                    "weight_g": weight,
                    "total_hours": total_hours,
                    "filament_type": selected_filament,
                    "material_cost": material_cost,
                    "print_time_cost": print_time_cost,
                    "electricity_cost": electricity_cost,
                    "profit_margin_percent": profit_margin_percent,
                    "final_price": final_price
                }

                page.update()

            except Exception as ex:
                show_snack_bar(f"Error en el cálculo: {ex}", "error")
        
        def save_quote(e):
            if current_quote_data and db_manager.save_quote(current_quote_data):
                show_snack_bar("Cotización guardada exitosamente", "success")
            else:
                show_snack_bar("Error al guardar la cotización", "error")
        
        # Agregar botón de guardar al resultado
        save_button = ft.ElevatedButton("Guardar Cotización", icon="save", on_click=save_quote, expand=True)
        
        return ft.Column([
            ft.Text("Calculadora de Costos", style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.W_500),
            piece_name,
            filament_type,
            weight_g,
            ft.Text("Tiempo de Impresión", style=ft.TextThemeStyle.BODY_LARGE),
            ft.Row([time_h, time_m], spacing=10),
            profit_margin,
            ft.ElevatedButton("Calcular Precio", icon="calculate", on_click=calculate_price, expand=True),
            result_card,
            save_button
        ], spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)
    
    # Vista Historial
    def create_history_view():
        quotes_list = ft.Column(controls=[], spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)
        
        def load_quotes():
            quotes_list.controls.clear()
            quotes = db_manager.get_recent_quotes(20)
            
            if not quotes:
                quotes_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon("receipt_long_outlined", size=60, color="outline"),
                            ft.Text("No hay cotizaciones", style=ft.TextThemeStyle.HEADLINE_SMALL, color="outline"),
                            ft.Text("Usa la calculadora para crear tu primera cotización", color="outline")
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                        alignment=ft.alignment.center,
                        padding=40
                    )
                )
            else:
                for quote in quotes:
                    quotes_list.controls.append(create_quote_card(quote))
            
            page.update()
        
        def create_quote_card(quote):
            return ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(quote.piece_name, style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD, expand=True),
                            ft.IconButton(icon="delete", tooltip="Eliminar", icon_color="error", on_click=lambda _, q=quote: delete_quote(q))
                        ]),
                        ft.Text(f"Filamento: {quote.filament_type}", style=ft.TextThemeStyle.BODY_MEDIUM),
                        ft.Text(f"Peso: {quote.weight_g}g | Tiempo: {quote.total_hours:.1f}h", style=ft.TextThemeStyle.BODY_SMALL),
                        ft.Row([
                            ft.Text(f"Precio: ${quote.final_price:.2f}", style=ft.TextThemeStyle.TITLE_SMALL, weight=ft.FontWeight.BOLD, color="primary", expand=True),
                            ft.Text(quote.timestamp, style=ft.TextThemeStyle.BODY_SMALL, color="outline")
                        ])
                    ], spacing=8),
                    padding=15
                ),
                elevation=2
            )
        
        def delete_quote(quote):
            def confirm_delete(e):
                if db_manager.delete_quote(quote.id):
                    show_snack_bar("Cotización eliminada", "success")
                    load_quotes()
                else:
                    show_snack_bar("Error al eliminar", "error")
                close_dialog()
            
            confirm_dialog = ft.AlertDialog(
                title=ft.Text("Confirmar Eliminación"),
                content=ft.Text(f"¿Eliminar la cotización '{quote.piece_name}'?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda _: close_dialog()),
                    ft.ElevatedButton("Eliminar", on_click=confirm_delete, bgcolor="error", color="onerror")
                ]
            )
            
            page.dialog = confirm_dialog
            page.dialog.open = True
            page.update()
        
        load_quotes()
        
        return ft.Column([
            ft.Text("Historial de Cotizaciones", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            quotes_list
        ], spacing=20, expand=True)
    
    # Vista Configuración
    def create_settings_view():
        return ft.Column([
            ft.Text("Configuración", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight=ft.FontWeight.BOLD),
            ft.Text("Aquí puedes ajustar los parámetros de cálculo", style=ft.TextThemeStyle.BODY_MEDIUM),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon("monetization_on"),
                            title=ft.Text("Precios de Filamentos"),
                            subtitle=ft.Text("Configurar costos por kg")
                        ),
                        ft.ListTile(
                            leading=ft.Icon("electrical_services"),
                            title=ft.Text("Costo de Electricidad"),
                            subtitle=ft.Text("Precio por kWh")
                        ),
                        ft.ListTile(
                            leading=ft.Icon("precision_manufacturing"),
                            title=ft.Text("Costo de Máquina"),
                            subtitle=ft.Text("Costo por hora de uso")
                        )
                    ])
                ),
                elevation=4
            )
        ], spacing=20, scroll=ft.ScrollMode.AUTO, expand=True)
    
    # Funciones de navegación
    def go_to_calculator():
        nonlocal current_view
        current_view = "calculator"
        update_view()
        page.navigation_bar.selected_index = 1
        page.update()
    
    def go_to_history():
        nonlocal current_view
        current_view = "history"
        update_view()
        page.navigation_bar.selected_index = 2
        page.update()
    
    def go_to_settings():
        nonlocal current_view
        current_view = "settings"
        update_view()
        page.navigation_bar.selected_index = 3
        page.update()
    
    def on_navigation_change(e):
        nonlocal current_view
        selected_index = e.control.selected_index
        
        if selected_index == 0:
            current_view = "home"
        elif selected_index == 1:
            current_view = "calculator"
        elif selected_index == 2:
            current_view = "history"
        elif selected_index == 3:
            current_view = "settings"
        
        update_view()
    
    def update_view():
        page.controls.clear()
        
        # AppBar
        page.appbar = ft.AppBar(
            title=ft.Text(get_title()),
            bgcolor="primary",
            color="onprimary",
            elevation=8
        )
        
        # Contenido principal
        content_container = ft.Container(
            content=get_current_view(),
            padding=20,
            expand=True
        )
        
        page.add(content_container)
        page.update()
    
    def get_title():
        titles = {
            "home": "Calculadora 3D Pro",
            "calculator": "Calculadora de Costos",
            "history": "Historial",
            "settings": "Configuración"
        }
        return titles.get(current_view, "Calculadora 3D Pro")
    
    def get_current_view():
        if current_view == "home":
            return create_home_view()
        elif current_view == "calculator":
            return create_calculator_view()
        elif current_view == "history":
            return create_history_view()
        elif current_view == "settings":
            return create_settings_view()
        else:
            return create_home_view()
    
    # Utilidades
    def show_snack_bar(message, tipo="info"):
        colors = {"success": "green", "error": "error", "info": "primary"}
        page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=colors.get(tipo, "primary"))
        page.snack_bar.open = True
        page.update()
    
    def close_dialog(e=None):
        if page.dialog:
            page.dialog.open = False
            page.update()
    
    # Configurar navegación
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon="home_outlined", selected_icon="home", label="Inicio"),
            ft.NavigationDestination(icon="calculate_outlined", selected_icon="calculate", label="Calcular"),
            ft.NavigationDestination(icon="history_outlined", selected_icon="history", label="Historial"),
            ft.NavigationDestination(icon="settings_outlined", selected_icon="settings", label="Ajustes"),
        ],
        on_change=on_navigation_change,
        selected_index=0,
        height=65,
        bgcolor="surface",
        indicator_color="primary",
        animation_duration=300,
    )
    
    # Inicializar vista
    update_view()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
