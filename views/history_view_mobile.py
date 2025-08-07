import flet as ft
from models.database_simple import DatabaseManager
import csv
import io

class HistoryViewMobile(ft.View):
    def __init__(self, page: ft.Page, db_manager: DatabaseManager):
        super().__init__()
        self.route = "/history"
        self.page = page
        self.db_manager = db_manager
        
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
                    tooltip="Exportar CSV", 
                    on_click=self.export_csv,
                    icon_color="onprimary"
                )
            ],
            elevation=8,
            color="onprimary",
        )
        
        # Lista de cotizaciones
        self.quotes_list = ft.Column(
            controls=[],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        self.load_quotes()
        
        # Contenedor principal
        main_container = ft.Container(
            content=ft.Column([
                ft.Text("Cotizaciones Recientes", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                self.quotes_list
            ], spacing=20, expand=True),
            padding=20,
            expand=True
        )
        
        self.controls = [main_container]
    
    def load_quotes(self):
        """Carga la lista de cotizaciones"""
        self.quotes_list.controls.clear()
        
        quotes = self.db_manager.get_recent_quotes(20)
        
        if not quotes:
            self.quotes_list.controls.append(
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
                self.quotes_list.controls.append(self.create_quote_card(quote))
        
        if self.page:
            self.page.update()
    
    def create_quote_card(self, quote):
        """Crea una tarjeta para mostrar una cotización"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(quote.piece_name, style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD, expand=True),
                        ft.IconButton(
                            icon="delete",
                            tooltip="Eliminar",
                            icon_color="error",
                            on_click=lambda _, q=quote: self.delete_quote(q)
                        )
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
    
    def delete_quote(self, quote):
        """Elimina una cotización"""
        def confirm_delete(e):
            if self.db_manager.delete_quote(quote.id):
                self.page.snack_bar = ft.SnackBar(ft.Text("Cotización eliminada"), bgcolor="green")
                self.load_quotes()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Error al eliminar"), bgcolor="error")
            
            self.page.snack_bar.open = True
            self.close_dialog()
            self.page.update()
        
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(f"¿Eliminar la cotización '{quote.piece_name}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog),
                ft.ElevatedButton("Eliminar", on_click=confirm_delete, bgcolor="error", color="onerror")
            ]
        )
        
        self.page.dialog = confirm_dialog
        self.page.dialog.open = True
        self.page.update()
    
    def close_dialog(self, e=None):
        """Cierra el diálogo activo"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
    
    def export_csv(self, e):
        """Exporta las cotizaciones a CSV"""
        try:
            quotes = self.db_manager.get_all_quotes()
            
            if not quotes:
                self.page.snack_bar = ft.SnackBar(ft.Text("No hay cotizaciones para exportar"), bgcolor="error")
                self.page.snack_bar.open = True
                self.page.update()
                return
            
            # Crear CSV en memoria
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Encabezados
            writer.writerow([
                'Nombre', 'Peso (g)', 'Tiempo (h)', 'Filamento', 
                'Costo Material', 'Costo Impresión', 'Costo Electricidad',
                'Margen (%)', 'Precio Final', 'Fecha'
            ])
            
            # Datos
            for quote in quotes:
                writer.writerow([
                    quote.piece_name,
                    quote.weight_g,
                    quote.total_hours,
                    quote.filament_type,
                    quote.material_cost,
                    quote.print_time_cost,
                    quote.electricity_cost,
                    quote.profit_margin_percent,
                    quote.final_price,
                    quote.timestamp
                ])
            
            # Intentar guardar el archivo
            csv_content = output.getvalue()
            filename = f"cotizaciones_3d_pro.csv"
            
            # En móvil, mostrar el contenido como texto para copiar
            self.show_csv_content(csv_content)
            
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al exportar: {ex}"), bgcolor="error")
            self.page.snack_bar.open = True
            self.page.update()
    
    def show_csv_content(self, csv_content):
        """Muestra el contenido CSV para copiar"""
        csv_dialog = ft.AlertDialog(
            title=ft.Text("Datos CSV"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Copia este contenido y guárdalo como archivo .csv:", style=ft.TextThemeStyle.BODY_MEDIUM),
                    ft.TextField(
                        value=csv_content,
                        multiline=True,
                        max_lines=10,
                        read_only=True,
                        border_radius=8
                    )
                ], spacing=10),
                width=350,
                height=300
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=self.close_dialog)
            ]
        )
        
        self.page.dialog = csv_dialog
        self.page.dialog.open = True
        self.page.update()
