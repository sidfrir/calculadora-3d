import flet as ft

from models.settings_manager import SettingsManager
from models.database_mobile import DatabaseManager

class CalculatorView(ft.View):
    def __init__(self, page: ft.Page, settings_manager: SettingsManager, db_manager: DatabaseManager):
        super().__init__()
        self.route = "/calculator"
        self.page = page
        self.settings_manager = settings_manager
        self.db_manager = db_manager
        self.current_quote_data = None # Para almacenar datos del último cálculo
        self.appbar = ft.AppBar(
            title=ft.Text("Calculadora de Costos"),
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
        
        # --- Campos del Formulario ---
        self.piece_name = ft.TextField(
            label="Nombre de la pieza",
            autofocus=True,
            border_radius=12,
            prefix_icon="text_fields",
            border_color="outlinevariant",
            focused_border_color="primary",
            animate_scale=ft.Animation(duration=200, curve="easeInOut"),
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
            border_color="outlinevariant",
            focused_border_color="primary",
            animate_scale=ft.Animation(duration=200, curve="easeInOut"),
        )
        
        # Grupo de campos de tiempo
        time_row = ft.Row(
            controls=[
                ft.Container(
                    content=ft.TextField(
                        label="Horas",
                        keyboard_type=ft.KeyboardType.NUMBER,
                        suffix_text="h",
                        width=100,
                        border_radius=12,
                        border_color="outlinevariant",
                        focused_border_color="primary",
                        animate_scale=ft.Animation(duration=200, curve="easeInOut"),
                    ),
                    expand=1
                ),
                ft.Container(
                    content=ft.TextField(
                        label="Minutos",
                        keyboard_type=ft.KeyboardType.NUMBER,
                        suffix_text="min",
                        width=100,
                        border_radius=12,
                        border_color="outlinevariant",
                        focused_border_color="primary",
                        animate_scale=ft.Animation(duration=200, curve="easeInOut"),
                    ),
                    expand=1
                )
            ],
            spacing=10
        )
        
        self.weight_g = ft.TextField(
            label="Peso",
            keyboard_type=ft.KeyboardType.NUMBER,
            suffix_text="g",
            border_radius=12,
            prefix_icon="scale",
            border_color="outlinevariant",
            focused_border_color="primary",
            animate_scale=ft.Animation(duration=200, curve="easeInOut"),
        )
        
        self.time_h = time_row.controls[0].content
        self.time_m = time_row.controls[1].content
        
        self.profit_margin = ft.TextField(
            label="Margen de Beneficio",
            value="20",
            keyboard_type=ft.KeyboardType.NUMBER,
            suffix_text="%",
            border_radius=12,
            prefix_icon="trending_up",
            border_color="outlinevariant",
            focused_border_color="primary",
            animate_scale=ft.Animation(duration=200, curve="easeInOut"),
        )

        self.save_button = ft.IconButton(icon="save", tooltip="Guardar Cotización", on_click=self.save_quote, visible=False)

        # --- Tarjeta de Resultados ---
        self.material_cost_text = ft.Text()
        self.print_time_cost_text = ft.Text()
        self.electricity_cost_text = ft.Text()
        self.subtotal_text = ft.Text(weight=ft.FontWeight.BOLD)
        self.margin_text = ft.Text()
        self.final_price_text = ft.Text(style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD)
        self.copy_button = ft.IconButton(icon="copy", visible=False, tooltip="Copiar Precio")

        # --- Tarjeta de Resultados Mejorada ---
        self.result_card = ft.Card(
            visible=False,
            elevation=10,
            shadow_color="black26",
            animate_scale=ft.Animation(duration=300, curve="easeOutBack"),
            scale=ft.Scale(scale=1),
            content=ft.Container(
                padding=25,
                content=ft.Column([
                    ft.Row([
                        ft.Icon("receipt_long", size=28, color="primary"),
                        ft.Text("Desglose de Costos", style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.BOLD, color="primary"),
                    ], alignment=ft.MainAxisAlignment.START, spacing=12),
                    ft.Divider(height=25, color="transparent"),
                    self.material_cost_text,
                    self.print_time_cost_text,
                    self.electricity_cost_text,
                    ft.Divider(height=15, color="outlinevariant"),
                    self.subtotal_text,
                    self.margin_text,
                    ft.Divider(height=25, color="transparent"),
                    ft.Row([
                        self.final_price_text,
                        ft.Container(content=self.copy_button, alignment=ft.alignment.center_right)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(height=25, color="transparent"),
                    ft.Row([
                        ft.Container(
                            content=ft.ElevatedButton(
                                text="Copiar Precio",
                                icon="content_copy",
                                on_click=lambda _: self.page.set_clipboard(self.final_price_text.value.split(": ")[-1]),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=ft.padding.symmetric(horizontal=25, vertical=12),
                                    bgcolor="primary",
                                    color="onprimary",
                                    animation_duration=200,
                                ),
                                width=180,
                            ),
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(
                                text="Guardar",
                                icon="save",
                                on_click=self.save_quote,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=ft.padding.symmetric(horizontal=25, vertical=12),
                                    bgcolor="secondary",
                                    color="onsecondary",
                                    animation_duration=200,
                                ),
                                width=180,
                            ),
                            expand=True,
                        ),
                    ], spacing=20),
                ]),
                border_radius=15,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=["surface", "surfacevariant"],
                ),
                animate_scale=ft.Animation(duration=300, curve="easeOutBack"),
                scale=ft.Scale(scale=1),
            )
        )

        # --- Diseño Responsivo ---
        form_container = ft.Container(
            content=ft.Column(
                controls=[
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
                ],
                spacing=15
            ),
            padding=20,
            border_radius=10,
            bgcolor="surfacevariant" if self.page.theme_mode == "dark" else "surface",
        )
        
        self.controls = [
            ft.Column(
                controls=[
                    form_container,
                    self.result_card
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
                expand=True
            )
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
                self.page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos."), bgcolor=ft.colors.ERROR)
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
            self.save_button.visible = True
            self.copy_button.visible = True
            self.copy_button.on_click = lambda _: self.page.set_clipboard(f"{final_price:.2f}")
            self.page.update()

        except (ValueError, TypeError):
            self.page.snack_bar = ft.SnackBar(ft.Text("Error: Revisa que los valores numéricos sean correctos."), bgcolor="error")
            self.page.snack_bar.open = True
            self.save_button.visible = False
            self.copy_button.visible = False
            self.page.update()

    def show_help(self, e):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Ayuda - Calculadora de Costos", weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text("Instrucciones para calcular el costo de una impresión 3D:", weight=ft.FontWeight.W_500),
                ft.Text("1. Nombre de la pieza: Asigna un nombre descriptivo a tu pieza."),
                ft.Text("2. Tipo de Filamento: Selecciona el material que usarás para la impresión."),
                ft.Text("3. Tiempo de Impresión: Ingresa las horas y minutos estimados de impresión."),
                ft.Text("4. Peso: Ingresa el peso total de la pieza en gramos."),
                ft.Text("5. Margen de Beneficio: Define el porcentaje de ganancia que deseas obtener."),
                ft.Divider(height=20),
                ft.Text("El cálculo considera:", weight=ft.FontWeight.W_500),
                ft.Text("• Costo del material (filamento)"),
                ft.Text("• Costo del tiempo de uso de la impresora"),
                ft.Text("• Costo del consumo eléctrico"),
                ft.Text("• Margen de beneficio aplicado"),
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Entendido", on_click=lambda e: self.page.close_dialog()),
            ],
        )
        self.page.open_dialog()

    def save_quote(self, e):
        if self.current_quote_data:
            self.db_manager.save_quote(self.current_quote_data)
            self.page.snack_bar = ft.SnackBar(ft.Text("Cotización guardada en el historial."), bgcolor="green")
            self.page.snack_bar.open = True
            self.save_button.visible = False
            self.copy_button.visible = False
            self.page.update()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("No hay cotización para guardar."), bgcolor="error")
            self.page.snack_bar.open = True
            self.page.update()
