import flet as ft
from gestion_app import ClientManager, client_manager, Client
from datetime import datetime

class ClientsView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.route = "/clients"
        self.page = page
        self.client_manager = client_manager
        
        self.appbar = ft.AppBar(
            title=ft.Text("Gestión de Clientes"),
            bgcolor="primary",
            leading=ft.IconButton(
                icon="home",
                tooltip="Volver al inicio",
                on_click=lambda _: page.go("/")
            ),
            actions=[
                ft.IconButton(
                    icon="person_add", 
                    tooltip="Nuevo Cliente", 
                    on_click=self.show_create_client_dialog,
                    icon_color="onprimary"
                )
            ],
            elevation=8,
            color="onprimary",
        )
        
        # Lista de clientes
        self.clients_list = ft.Column(
            controls=[],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        self.load_clients()
        
        # Contenedor principal
        main_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Base de Datos de Clientes", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    self.clients_list
                ],
                spacing=20,
                expand=True
            ),
            padding=20,
            expand=True
        )
        
        self.controls = [main_container]
    
    def load_clients(self):
        """Carga la lista de clientes"""
        self.clients_list.controls.clear()
        
        clients = self.client_manager.get_all_clients()
        
        if not clients:
            self.clients_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon("people_outline", size=60, color="outline"),
                        ft.Text("No hay clientes", style=ft.TextThemeStyle.HEADLINE_SMALL, color="outline"),
                        ft.Text("Usa el botón + para agregar tu primer cliente", color="outline")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    alignment=ft.alignment.center,
                    padding=40
                )
            )
        else:
            for client in clients:
                self.clients_list.controls.append(self.create_client_card(client))
        
        if self.page:
            self.page.update()
    
    def create_client_card(self, client):
        """Crea una tarjeta para mostrar un cliente"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(client.name, style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Email: {client.email}", style=ft.TextThemeStyle.BODY_MEDIUM),
                            ft.Text(f"Teléfono: {client.phone}", style=ft.TextThemeStyle.BODY_SMALL),
                        ],
                        expand=True,
                        spacing=5
                    ),
                    ft.Row([
                        ft.IconButton(
                            icon="visibility",
                            tooltip="Ver detalles",
                            on_click=lambda _, c=client: self.show_client_details(c)
                        ),
                        ft.IconButton(
                            icon="edit",
                            tooltip="Editar",
                            on_click=lambda _, c=client: self.show_edit_client_dialog(c)
                        ),
                        ft.IconButton(
                            icon="delete",
                            tooltip="Eliminar",
                            icon_color="error",
                            on_click=lambda _, c=client: self.confirm_delete_client(c)
                        )
                    ])
                ]
            ),
            bgcolor="surfacevariant",
            padding=15,
            border_radius=10,
            animate_scale=ft.Animation(duration=200, curve="easeInOut")
        )
    
    def show_create_client_dialog(self, e):
        """Muestra diálogo para crear nuevo cliente"""
        name_field = ft.TextField(label="Nombre completo", autofocus=True)
        email_field = ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL)
        phone_field = ft.TextField(label="Teléfono", keyboard_type=ft.KeyboardType.PHONE)
        company_field = ft.TextField(label="Empresa (opcional)")
        address_field = ft.TextField(label="Dirección", multiline=True)
        preferred_filament_field = ft.TextField(label="Filamento preferido (opcional)")
        
        def create_client(e):
            try:
                # Validaciones básicas
                if not name_field.value:
                    self.page.snack_bar = ft.SnackBar(ft.Text("El nombre es obligatorio"), bgcolor="error")
                    self.page.snack_bar.open = True
                    self.page.update()
                    return
                
                client = Client(
                    name=name_field.value,
                    email=email_field.value or "",
                    phone=phone_field.value or "",
                    company=company_field.value or "",
                    address=address_field.value or "",
                    preferred_filament=preferred_filament_field.value or ""
                )
                
                self.client_manager.create_client(client)
                self.close_dialog()
                self.load_clients()
                
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Cliente '{client.name}' creado exitosamente"), bgcolor="green")
                self.page.snack_bar.open = True
                self.page.update()
                
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="error")
                self.page.snack_bar.open = True
                self.page.update()
        
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Nuevo Cliente"),
            content=ft.Column([
                name_field,
                email_field,
                phone_field,
                company_field,
                address_field,
                preferred_filament_field
            ], tight=True, spacing=15),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog),
                ft.ElevatedButton("Crear", on_click=create_client)
            ]
        )
        self.page.dialog = confirm_dialog
        self.page.dialog.open = True
        self.page.update()
    
    def show_client_details(self, client):
        """Muestra detalles del cliente"""
        confirm_dialog = ft.AlertDialog(
            title=ft.Text(f"Detalles: {client.name}"),
            content=ft.Column([
                ft.Text(f"Email: {client.email}"),
                ft.Text(f"Teléfono: {client.phone}"),
                ft.Text(f"Empresa: {client.company}"),
                ft.Text(f"Dirección: {client.address}"),
                ft.Text(f"Filamento preferido: {client.preferred_filament}"),
                ft.Text(f"Creado: {client.created_at}"),
                ft.Text(f"Actualizado: {client.updated_at}")
            ], spacing=10),
            actions=[
                ft.TextButton("Cerrar", on_click=self.close_dialog)
            ]
        )
        self.page.dialog = confirm_dialog
        self.page.dialog.open = True
        self.page.update()
    
    def show_edit_client_dialog(self, client):
        """Muestra diálogo para editar cliente"""
        name_field = ft.TextField(label="Nombre completo", value=client.name)
        email_field = ft.TextField(label="Email", value=client.email, keyboard_type=ft.KeyboardType.EMAIL)
        phone_field = ft.TextField(label="Teléfono", value=client.phone, keyboard_type=ft.KeyboardType.PHONE)
        company_field = ft.TextField(label="Empresa", value=client.company)
        address_field = ft.TextField(label="Dirección", value=client.address, multiline=True)
        preferred_filament_field = ft.TextField(label="Filamento preferido", value=client.preferred_filament)
        
        def update_client(e):
            try:
                if not name_field.value:
                    self.page.snack_bar = ft.SnackBar(ft.Text("El nombre es obligatorio"), bgcolor="error")
                    self.page.snack_bar.open = True
                    self.page.update()
                    return
                
                client.name = name_field.value
                client.email = email_field.value or ""
                client.phone = phone_field.value or ""
                client.company = company_field.value or ""
                client.address = address_field.value or ""
                client.preferred_filament = preferred_filament_field.value or ""
                client.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                self.client_manager.update_client(client)
                self.close_dialog()
                self.load_clients()
                
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Cliente '{client.name}' actualizado"), bgcolor="green")
                self.page.snack_bar.open = True
                self.page.update()
                
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="error")
                self.page.snack_bar.open = True
                self.page.update()
        
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Editar Cliente"),
            content=ft.Column([
                name_field,
                email_field,
                phone_field,
                company_field,
                address_field,
                preferred_filament_field
            ], tight=True, spacing=15),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog),
                ft.ElevatedButton("Guardar", on_click=update_client)
            ]
        )
        self.page.dialog = confirm_dialog
        self.page.dialog.open = True
        self.page.update()
    
    def confirm_delete_client(self, client):
        """Confirma eliminación del cliente"""
        def delete_client(e):
            try:
                self.client_manager.delete_client(client.id)
                self.close_dialog()
                self.load_clients()
                
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Cliente '{client.name}' eliminado"), bgcolor="green")
                self.page.snack_bar.open = True
                self.page.update()
                
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"), bgcolor="error")
                self.page.snack_bar.open = True
                self.page.update()
        
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(f"¿Estás seguro de eliminar el cliente '{client.name}'?\n\nEsta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog),
                ft.ElevatedButton(
                    "Eliminar", 
                    on_click=delete_client,
                    bgcolor="error",
                    color="onerror"
                )
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
