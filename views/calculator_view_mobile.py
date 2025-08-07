import flet as ft
from models.settings_manager import SettingsManager
from models.database_simple import DatabaseManager

class CalculatorViewMobile(ft.View):
    def __init__(self, page: ft.Page, settings_manager: SettingsManager, db_manager: DatabaseManager):
        super().__init__()
        self.route = "/calculator"
        self.page = page
        self.settings_manager = settings_manager
        self.db_manager = db_manager
        self.current_quote_data = None
        
        self.appbar = ft.AppBar(
            title=ft.Text("Calculadora de Costos"),
            bgcolor="primary",
            leading=ft.IconButton(
                icon="home",
                tooltip="Volver al inicio",
                on_click=lambda _: page.go("/")
            ),
            elevation=8,
            color="onprimary",
        )
        
        # --- Campos del Formulario ---
        self.piece_name = ft.TextField(
            label="Nombre de la pieza",
            autofocus=True,
            border_radius=12,
            prefix_icon="text_fields",
        )
        
        # Cargar filamentos dinámicamente
        filament_options = []
        for name in self.settings_manager.get('filaments', {}).keys():
            filament_options.append(ft.dropdown.Option(name))

        self.filament_type = ft.Dropdown(
            label="Tipo de Filamento",
            options=filament_options,
            border_radius=12,
            prefix_icon="local_fire_department",
        )
        
        self.weight_g = ft.TextField(
            label="Peso (gramos)",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=12,
            prefix_icon="scale",
        )
        
        self.time_h = ft.TextField(
            label="Horas",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=150,
            border_radius=12,
            value="0"
        )
        
        self.time_m = ft.TextField(
            label="Minutos", 
            keyboard_type=ft.KeyboardType.NUMBER,
            width=150,
            border_radius=12,
            value="0"
        )
        
        self.profit_margin = ft.TextField(
            label="Margen de Ganancia (%)",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=12,
            prefix_icon="percent",
            value="20"
        )
        
        # --- Tarjeta de Resultados ---
        self.material_cost_text = ft.Text("Costo de Material: --", size=14)
        self.print_time_cost_text = ft.Text("Costo de Impresión: --", size=14)
        self.electricity_cost_text = ft.Text("Costo de Electricidad: --", size=14)
        self.subtotal_text = ft.Text("Subtotal: --", size=14)
        self.margin_text = ft.Text("Margen: --", size=14)
        self.final_price_text = ft.Text("PRECIO FINAL: --", size=18, weight=ft.FontWeight.BOLD, color="primary")
        
        self.result_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Resultado del Cálculo", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    self.material_cost_text,
                    self.print_time_cost_text,
                    self.electricity_cost_text,
                    self.subtotal_text,
                    self.margin_text,
                    ft.Divider(),
                    self.final_price_text,
                    ft.Row([
                        ft.ElevatedButton(
                            "Guardar Cotización",
                            icon="save",
                            on_click=self.save_quote,
                            expand=True
                        )
                    ], spacing=10)
                ], spacing=8),
                padding=20
            ),
            visible=False
        )
        
        # --- Diseño ---
        time_row = ft.Row([self.time_h, self.time_m], spacing=10)
        
        form_container = ft.Container(
            content=ft.Column([
                ft.Text("Datos de la Pieza", style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.W_500),
                self.piece_name,
                self.filament_type,
                self.weight_g,
                ft.Text("Tiempo de Impresión", style=ft.TextThemeStyle.BODY_LARGE),
                time_row,
                self.profit_margin,
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Calcular Precio",
                        icon="calculate",
                        on_click=self.calculate_price,
                        style=ft.ButtonStyle(
                            padding=ft.padding.symmetric(horizontal=30, vertical=15),
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                        expand=True
                    ),
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(top=10)
                )
            ], spacing=15),
            padding=20,
        )
        
        self.controls = [
            ft.Column([
                form_container,
                self.result_card
            ], spacing=20, scroll=ft.ScrollMode.AUTO, expand=True)
        ]
    
    def calculate_price(self, e):
        try:
            # --- Cargar valores desde el gestor de configuración ---
            settings = self.settings_manager.load_settings()
            machine_cost_per_hour = float(settings['machine_cost_per_hour'])
            electricity_kwh_price = float(settings['electricity_kwh_price'])
            printer_power_watts = int(settings['printer_power_watts'])
            filament_prices = settings['filaments']

            # --- Obtener valores del formulario ---
            weight = float(self.weight_g.value)
            hours = float(self.time_h.value or 0)
            minutes = float(self.time_m.value or 0)
            total_hours = hours + (minutes / 60)
            profit_margin_percent = float(self.profit_margin.value)
            selected_filament = self.filament_type.value

            if not all([self.weight_g.value, total_hours > 0, selected_filament]):
                self.page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos."), bgcolor="error")
                self.page.snack_bar.open = True
                self.page.update()
                return

            # --- Cálculos ---
            filament_price_per_kg = float(filament_prices[selected_filament]['price_per_kg'])
            material_cost = (weight / 1000) * filament_price_per_kg
            print_time_cost = total_hours * machine_cost_per_hour
            electricity_cost = (printer_power_watts / 1000) * total_hours * electricity_kwh_price
            
            subtotal = material_cost + print_time_cost + electricity_cost
            margin_amount = subtotal * (profit_margin_percent / 100)
            final_price = subtotal + margin_amount

            # --- Actualizar la tarjeta de resultados ---
            currency_symbol = self.settings_manager.get('currency_symbol', '$')
            self.material_cost_text.value = f"Costo de Material: {currency_symbol}{material_cost:.2f}"
            self.print_time_cost_text.value = f"Costo de Impresión: {currency_symbol}{print_time_cost:.2f}"
            self.electricity_cost_text.value = f"Costo de Electricidad: {currency_symbol}{electricity_cost:.2f}"
            self.subtotal_text.value = f"Subtotal: {currency_symbol}{subtotal:.2f}"
            self.margin_text.value = f"Margen ({profit_margin_percent}%): {currency_symbol}{margin_amount:.2f}"
            self.final_price_text.value = f"PRECIO FINAL: {currency_symbol}{final_price:.2f}"

            # Almacenar datos para guardado
            self.current_quote_data = {
                "piece_name": self.piece_name.value or "Sin nombre",
                "weight_g": weight,
                "total_hours": total_hours,
                "filament_type": selected_filament,
                "material_cost": material_cost,
                "print_time_cost": print_time_cost,
                "electricity_cost": electricity_cost,
                "profit_margin_percent": profit_margin_percent,
                "final_price": final_price
            }

            self.result_card.visible = True
            self.page.update()

        except (ValueError, TypeError, KeyError) as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error en el cálculo: {ex}"), bgcolor="error")
            self.page.snack_bar.open = True
            self.page.update()
    
    def save_quote(self, e):
        if not self.current_quote_data:
            self.page.snack_bar = ft.SnackBar(ft.Text("No hay datos para guardar"), bgcolor="error")
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        try:
            success = self.db_manager.save_quote(self.current_quote_data)
            if success:
                self.page.snack_bar = ft.SnackBar(ft.Text("Cotización guardada exitosamente"), bgcolor="green")
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Error al guardar la cotización"), bgcolor="error")
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="error")
        
        self.page.snack_bar.open = True
        self.page.update()
