import flet as ft
from models.database_mobile import DatabaseManager
import csv
import io

class HistoryView(ft.View):
    def __init__(self, page: ft.Page, db_manager: DatabaseManager, file_picker: ft.FilePicker):
        super().__init__()
        self.route = "/history"
        self.page = page
        self.db_manager = db_manager
        self.file_picker = file_picker
        self.file_picker.on_result = self.save_csv_file # Asignar el manejador

        self.appbar = ft.AppBar(
            title=ft.Text("Historial de Cotizaciones"), 
            bgcolor="primary",
            leading=ft.IconButton(
                icon="home",
                tooltip="Volver al inicio",
                on_click=lambda _: page.go("/")
            ),
            actions=[
                ft.IconButton(
                    icon="file_download",
                    tooltip="Exportar a CSV",
                    on_click=lambda _: self.file_picker.save_file(
                        dialog_title="Guardar Historial como CSV",
                        file_name="historial_cotizaciones.csv",
                        allowed_extensions=["csv"]
                    ),
                    icon_color="onprimary",
                )
            ],
            color="onprimary",
            elevation=5,
            shadow_color="black38",
        )
        
        # Crear un contenedor con mejor diseño
        self.history_list = ft.ListView(
            expand=True, 
            spacing=15, 
            padding=ft.padding.all(20)
        )
        
        self.controls = [
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "Tus Cotizaciones Recientes",
                            style=ft.TextThemeStyle.HEADLINE_SMALL,
                            weight=ft.FontWeight.BOLD,
                            color="primary",
                        ),
                        padding=ft.padding.only(left=25, top=15, bottom=5),
                        animate_opacity=ft.Animation(duration=500, curve="easeIn"),
                        opacity=1,
                    ),
                    self.history_list
                ],
                expand=True,
                spacing=15
            )
        ]

    def did_mount(self):
        """Se llama cuando la vista se muestra."""
        self.load_history()

    def load_history(self):
        self.history_list.controls.clear()
        quotes = self.db_manager.get_history()
        
        if not quotes:
            self.history_list.controls.append(
                ft.Container(
                    content=ft.Text("No hay cotizaciones guardadas.", style=ft.TextThemeStyle.BODY_LARGE, text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    expand=True
                )
            )
        else:
            for quote in quotes:
                # Crear una tarjeta más moderna con mejor diseño
                card_content = ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(
                                    content=ft.Icon("receipt", size=45, color="onprimary"),
                                    bgcolor="primary",
                                    border_radius=15,
                                    padding=15,
                                    width=75,
                                    height=75,
                                    animate_scale=ft.Animation(duration=200, curve="easeInOut"),
                                    scale=ft.Scale(scale=1),
                                ),
                                ft.Column(
                                    [
                                        ft.Text(
                                            quote.piece_name, 
                                            style=ft.TextThemeStyle.TITLE_MEDIUM, 
                                            weight=ft.FontWeight.BOLD,
                                            color="primary",
                                        ),
                                        ft.Text(
                                            f"Fecha: {quote.created_at.strftime('%d/%m/%Y %H:%M')}", 
                                            size=15,
                                            color="onsurfacevariant"
                                        ),
                                        ft.Container(
                                            content=ft.Text(
                                                f"${quote.final_price:.2f}", 
                                                weight=ft.FontWeight.BOLD, 
                                                size=22,
                                                color="primary"
                                            ),
                                            margin=ft.margin.only(top=8),
                                            animate_scale=ft.Animation(duration=300, curve="easeOutBack"),
                                            scale=ft.Scale(scale=1),
                                        )
                                    ],
                                    spacing=8,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    expand=True,
                                )
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=20
                        ),
                        padding=20,
                    ),
                    elevation=8,
                    shadow_color="black26",
                    animate_scale=ft.Animation(duration=200, curve="easeInOut"),
                    scale=ft.Scale(scale=1),
                )
                self.history_list.controls.append(card_content)
        self.update()

    def save_csv_file(self, e: ft.FilePickerResultEvent):
        if not e.path:
            self.page.snack_bar = ft.SnackBar(ft.Text("Exportación cancelada."))
            self.page.snack_bar.open = True
            self.page.update()
            return

        quotes = self.db_manager.get_history()
        try:
            with open(e.path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # Escribir cabecera
                writer.writerow([
                    'ID', 'Nombre Pieza', 'Fecha', 'Peso (g)', 'Tiempo (h)',
                    'Filamento', 'Costo Material', 'Costo Impresion',
                    'Costo Electricidad', 'Margen (%)', 'Precio Final'
                ])
                # Escribir datos
                for quote in quotes:
                    writer.writerow([
                        quote.id, quote.piece_name, quote.created_at.strftime('%Y-%m-%d %H:%M'),
                        f"{quote.weight_g:.2f}", f"{quote.total_hours:.2f}", quote.filament_type,
                        f"{quote.material_cost:.2f}", f"{quote.print_time_cost:.2f}",
                        f"{quote.electricity_cost:.2f}", f"{quote.profit_margin_percent:.2f}",
                        f"{quote.final_price:.2f}"
                    ])
            
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Historial guardado en {e.path}"), bgcolor="green")
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar el archivo: {ex}"), bgcolor="error")
        
        self.page.snack_bar.open = True
        self.page.update()
