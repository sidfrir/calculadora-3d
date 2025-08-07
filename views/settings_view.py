import flet as ft
from models.settings_manager import SettingsManager

class SettingsView(ft.View):
    def __init__(self, page: ft.Page, settings_manager: SettingsManager):
        super().__init__()
        self.route = "/settings"
        self.page = page
        self.settings_manager = settings_manager
        self.appbar = ft.AppBar(
            title=ft.Text("Configuración"), 
            bgcolor="primary",
            leading=ft.IconButton(
                icon="home",
                tooltip="Volver al inicio",
                on_click=lambda _: page.go("/")
            ),
            actions=[
                ft.IconButton(
                    icon="help_outline", 
                    tooltip="Ayuda", 
                    on_click=self.show_help,
                    icon_color="onprimary"
                )
            ],
            elevation=8,
            color="onprimary",
        )

        # --- Configuración de Moneda ---
        self.currency_dropdown = ft.Dropdown(
            label="Moneda",
            value=self.settings_manager.get('currency', 'USD'),
            options=[
                ft.dropdown.Option("USD", "Dólares (USD)"),
                ft.dropdown.Option("ARS", "Pesos Argentinos (ARS)"),
            ],
            border_radius=12,
            prefix_icon="attach_money",
            border_color="outlinevariant",
            focused_border_color="primary",
            animate_scale=ft.Animation(duration=200, curve="easeInOut"),
            on_change=self.on_currency_change,
        )
        
        # --- Campos de Configuración General ---
        self.machine_cost = ft.TextField(
            label="Costo Máquina por Hora",
            value=str(self.settings_manager.get('machine_cost_per_hour')),
            prefix_text=self.settings_manager.get('currency_symbol'),
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=12,
            prefix_icon="euro_symbol",
            border_color="outlinevariant",
            focused_border_color="primary",
            animate_scale=ft.Animation(duration=200, curve="easeInOut"),
        )
        self.electricity_price = ft.TextField(
            label="Costo Electricidad (kWh)",
            value=str(self.settings_manager.get('electricity_kwh_price')),
            prefix_text=self.settings_manager.get('currency_symbol'),
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=12,
            prefix_icon="flash_on",
            border_color="outlinevariant",
            focused_border_color="primary",
            animate_scale=ft.Animation(duration=200, curve="easeInOut"),
        )
        self.printer_power = ft.TextField(
            label="Consumo Impresora (Watts)",
            value=str(self.settings_manager.get('printer_power_watts')),
            suffix_text="W",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=12,
            prefix_icon="bolt",
            border_color="outlinevariant",
            focused_border_color="primary",
            animate_scale=ft.Animation(duration=200, curve="easeInOut"),
        )

        self.theme_dropdown = ft.Dropdown(
            label="Tema de la Aplicación",
            value=self.settings_manager.get('theme_mode'),
            options=[
                ft.dropdown.Option("system", "Automático (Sistema)"),
                ft.dropdown.Option("light", "Claro"),
                ft.dropdown.Option("dark", "Oscuro"),
            ],
            border_radius=12,
            prefix_icon="palette",
            border_color="outlinevariant",
            focused_border_color="primary",
            animate_scale=ft.Animation(duration=200, curve="easeInOut"),
        )
        
        # Preferencias de usuario
        # Cargar preferencias actuales
        from models.user_preferences import UserPreferences
        self.user_preferences = UserPreferences()
        self.animations_switch = ft.Switch(
            label="Activar animaciones",
            value=self.user_preferences.get("animations_enabled", True),
            active_color="primary",
        )

        # --- Campos de Filamentos ---
        self.filament_fields = {}
        filament_controls = []
        for name, data in self.settings_manager.get('filaments', {}).items():
            field = ft.TextField(
                label=f"Precio {name} por kg",
                value=str(data.get('price_per_kg', 0)),
                prefix_text=self.settings_manager.get('currency_symbol'),
                keyboard_type=ft.KeyboardType.NUMBER,
                border_radius=12,
                prefix_icon="local_fire_department",
                border_color="outlinevariant",
                focused_border_color="primary",
                animate_scale=ft.Animation(duration=200, curve="easeInOut"),
            )
            self.filament_fields[name] = field
            filament_controls.append(field)

        # --- Organización en secciones con mejor diseño ---
        currency_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Configuración Monetaria", style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD, color="primary"),
                    self.currency_dropdown,
                    ft.Text(
                        f"Moneda actual: {self.settings_manager.get('currency_name', 'Dólares (USD)')}",
                        style=ft.TextThemeStyle.BODY_MEDIUM,
                        color="onsurfacevariant"
                    ),
                ],
                spacing=15
            ),
            padding=25,
            border_radius=15,
            bgcolor="primarycontainer",
            animate_scale=ft.Animation(duration=300, curve="easeOutBack"),
            scale=1.0,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color="black26",
            ),
        )
        
        appearance_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Apariencia", style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD, color="primary"),
                    self.theme_dropdown,
                    ft.Divider(height=20, color="outlinevariant"),
                    ft.Text("Preferencias de Usuario", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.W_500),
                    self.animations_switch,
                ],
                spacing=20
            ),
            padding=25,
            border_radius=15,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["surface", "surfacevariant"],
            ),
            animate_scale=ft.Animation(duration=300, curve="easeOutBack"),
            scale=1.0,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color="black26",
            ),
        )
        
        costs_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Costos Generales", style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD, color="primary"),
                    self.machine_cost,
                    self.electricity_price,
                    self.printer_power,
                ],
                spacing=20
            ),
            padding=25,
            border_radius=15,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["surface", "surfacevariant"],
            ),
            animate_scale=ft.Animation(duration=300, curve="easeOutBack"),
            scale=1.0,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color="black26",
            ),
        )
        
        filaments_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Precios de Filamentos", style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD, color="primary"),
                    *filament_controls,
                ],
                spacing=20
            ),
            padding=25,
            border_radius=15,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["surface", "surfacevariant"],
            ),
            animate_scale=ft.Animation(duration=300, curve="easeOutBack"),
            scale=1.0,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color="black26",
            ),
        )
        
        save_button = ft.Container(
            content=ft.ElevatedButton(
                text="Guardar Cambios",
                icon="save",
                on_click=self.save_settings,
                style=ft.ButtonStyle(
                    padding=ft.padding.symmetric(horizontal=35, vertical=20),
                    shape=ft.RoundedRectangleBorder(radius=12),
                    bgcolor="primary",
                    color="onprimary",
                    animation_duration=200,
                ),
                width=250,
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=30),
            animate_scale=ft.Animation(duration=300, curve="easeOutBack"),
            scale=1.0,
        )
        
        self.controls = [
            ft.Column(
                controls=[
                    currency_section,
                    appearance_section,
                    costs_section,
                    filaments_section,
                    save_button
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
                expand=True
            )
        ]

    def show_help(self, e):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Ayuda - Configuración", weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text("Configuración de la aplicación:", weight=ft.FontWeight.W_500),
                ft.Text("• Apariencia: Selecciona el tema de la aplicación (claro, oscuro o automático)."),
                ft.Text("• Costos Generales: Define los costos asociados a tu impresora 3D."),
                ft.Text("  - Costo Máquina por Hora: Costo de operación de tu impresora por hora."),
                ft.Text("  - Costo Electricidad (kWh): Precio del kilovatio-hora en tu región."),
                ft.Text("  - Consumo Impresora (Watts): Potencia de consumo de tu impresora."),
                ft.Text("• Precios de Filamentos: Establece el precio por kilogramo de cada tipo de filamento."),
                ft.Divider(height=20),
                ft.Text("Consejo: Ajusta estos valores según tus costos reales para obtener cotizaciones precisas.", weight=ft.FontWeight.W_500),
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Entendido", on_click=lambda e: self.page.close_dialog()),
            ],
        )
        self.page.open_dialog()

    def save_settings(self, e):
        try:
            # Guardar configuración general
            new_settings = self.settings_manager.load_settings()
            new_settings['machine_cost_per_hour'] = float(self.machine_cost.value)
            new_settings['electricity_kwh_price'] = float(self.electricity_price.value)
            new_settings['printer_power_watts'] = int(self.printer_power.value)
            new_settings['theme_mode'] = self.theme_dropdown.value

            # Aplicar el tema inmediatamente
            if self.theme_dropdown.value == "dark":
                self.page.theme_mode = ft.ThemeMode.DARK
            elif self.theme_dropdown.value == "light":
                self.page.theme_mode = ft.ThemeMode.LIGHT
            else:
                self.page.theme_mode = ft.ThemeMode.SYSTEM

            for name, field in self.filament_fields.items():
                new_settings['filaments'][name]['price_per_kg'] = float(field.value)
            
            self.settings_manager.save_settings(new_settings)

            # Guardar preferencias de usuario
            self.user_preferences.set("animations_enabled", self.animations_switch.value)

            self.page.snack_bar = ft.SnackBar(ft.Text("Configuración guardada."), bgcolor="green")
            self.page.snack_bar.open = True
            self.page.update()

        except (ValueError, TypeError):
            self.page.snack_bar = ft.SnackBar(ft.Text("Error: Asegúrate de que los valores numéricos son correctos."), bgcolor="error")
            self.page.snack_bar.open = True
            self.page.update()
    
    def on_currency_change(self, e):
        """Manejar el cambio de moneda"""
        try:
            currency_code = self.currency_dropdown.value
            self.settings_manager.update_currency(currency_code)
            
            # Actualizar los prefijos de los campos de precio
            new_symbol = self.settings_manager.get('currency_symbol')
            self.machine_cost.prefix_text = new_symbol
            self.electricity_price.prefix_text = new_symbol
            
            # Actualizar prefijos de filamentos
            for field in self.filament_fields.values():
                field.prefix_text = new_symbol
            
            # Actualizar texto de moneda actual
            self.page.update()
            
            # Mostrar confirmación
            currency_name = self.settings_manager.get('currency_name')
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Moneda cambiada a: {currency_name}"), 
                bgcolor="green"
            )
            self.page.snack_bar.open = True
            self.page.update()
            
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Error al cambiar moneda: {ex}"), 
                bgcolor="error"
            )
            self.page.snack_bar.open = True
            self.page.update()
