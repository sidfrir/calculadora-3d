import flet as ft
from gestion_app import ProjectManager, project_manager, Project, Client
from datetime import datetime

class ProjectsView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.route = "/projects"
        self.page = page
        self.project_manager = project_manager
        
        self.appbar = ft.AppBar(
            title=ft.Text("Gestión de Proyectos"),
            bgcolor="primary",
            leading=ft.IconButton(
                icon="home",
                tooltip="Volver al inicio",
                on_click=lambda _: page.go("/")
            ),
            actions=[
                ft.IconButton(
                    icon="add", 
                    tooltip="Nuevo Proyecto", 
                    on_click=self.show_create_project_dialog,
                    icon_color="onprimary"
                )
            ],
            elevation=8,
            color="onprimary",
        )
        
        # Lista de proyectos
        self.projects_list = ft.Column(
            controls=[],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        self.load_projects()
        
        # Contenedor principal
        main_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Proyectos Activos", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    self.projects_list
                ],
                spacing=20,
                expand=True
            ),
            padding=20,
            expand=True
        )
        
        self.controls = [main_container]
    
    def load_projects(self):
        """Carga la lista de proyectos"""
        self.projects_list.controls.clear()
        
        projects = self.project_manager.get_all_projects()
        
        if not projects:
            self.projects_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon("work_outline", size=60, color="outline"),
                        ft.Text("No hay proyectos", style=ft.TextThemeStyle.HEADLINE_SMALL, color="outline"),
                        ft.Text("Usa el botón + para crear tu primer proyecto", color="outline")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    alignment=ft.alignment.center,
                    padding=40
                )
            )
        else:
            for project in projects:
                self.projects_list.controls.append(self.create_project_card(project))
        
        if self.page:
            self.page.update()
    
    def create_project_card(self, project):
        """Crea una tarjeta para mostrar un proyecto"""
        # Determinar color del estado
        status_colors = {
            "pending": "orange",
            "in_progress": "blue", 
            "completed": "green",
            "cancelled": "red"
        }
        
        status_labels = {
            "pending": "Pendiente",
            "in_progress": "En Progreso",
            "completed": "Completado", 
            "cancelled": "Cancelado"
        }
        
        status_color = status_colors.get(project.status, "grey")
        status_label = status_labels.get(project.status, project.status)
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(project.name, style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Cliente: {project.client_name}", style=ft.TextThemeStyle.BODY_MEDIUM),
                            ft.Text(f"Presupuesto: ${project.budget:.2f}", style=ft.TextThemeStyle.BODY_SMALL),
                        ],
                        expand=True,
                        spacing=5
                    ),
                    ft.Container(
                        content=ft.Text(status_label, color="white"),
                        bgcolor=status_color,
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=12
                    ),
                    ft.Row([
                        ft.IconButton(
                            icon="visibility",
                            tooltip="Ver detalles",
                            on_click=lambda _, p=project: self.show_project_details(p)
                        ),
                        ft.IconButton(
                            icon="edit",
                            tooltip="Editar",
                            on_click=lambda _, p=project: self.show_edit_project_dialog(p)
                        ),
                        ft.IconButton(
                            icon="delete",
                            tooltip="Eliminar",
                            icon_color="error",
                            on_click=lambda _, p=project: self.confirm_delete_project(p)
                        )
                    ])
                ]
            ),
            bgcolor="surfacevariant",
            padding=15,
            border_radius=10,
            animate_scale=ft.Animation(duration=200, curve="easeInOut")
        )
    
    def show_create_project_dialog(self, e):
        """Muestra diálogo para crear nuevo proyecto"""
        name_field = ft.TextField(label="Nombre del Proyecto", autofocus=True)
        client_name_field = ft.TextField(label="Nombre del Cliente")
        description_field = ft.TextField(label="Descripción", multiline=True)
        budget_field = ft.TextField(label="Presupuesto", keyboard_type=ft.KeyboardType.NUMBER)
        
        def create_project(e):
            try:
                # Validaciones básicas
                if not name_field.value or not client_name_field.value:
                    self.page.snack_bar = ft.SnackBar(ft.Text("Nombre y cliente son obligatorios"), bgcolor="error")
                    self.page.snack_bar.open = True
                    self.page.update()
                    return
                
                budget = float(budget_field.value) if budget_field.value else 0.0
                
                project = Project(
                    name=name_field.value,
                    client_name=client_name_field.value,
                    description=description_field.value or "",
                    budget=budget,
                    status="pending"
                )
                
                self.project_manager.create_project(project)
                self.close_dialog()
                self.load_projects()
                
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Proyecto '{project.name}' creado exitosamente"), bgcolor="green")
                self.page.snack_bar.open = True
                self.page.update()
                
            except ValueError:
                self.page.snack_bar = ft.SnackBar(ft.Text("El presupuesto debe ser un número válido"), bgcolor="error")
                self.page.snack_bar.open = True
                self.page.update()
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="error")
                self.page.snack_bar.open = True
                self.page.update()
        
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Nuevo Proyecto"),
            content=ft.Column([
                name_field,
                client_name_field,
                description_field,
                budget_field
            ], tight=True, spacing=15),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog),
                ft.ElevatedButton("Crear", on_click=create_project)
            ]
        )
        self.page.dialog = confirm_dialog
        self.page.dialog.open = True
        self.page.update()
    
    def show_project_details(self, project):
        """Muestra detalles del proyecto"""
        confirm_dialog = ft.AlertDialog(
            title=ft.Text(f"Detalles: {project.name}"),
            content=ft.Column([
                ft.Text(f"Cliente: {project.client_name}"),
                ft.Text(f"Descripción: {project.description}"),
                ft.Text(f"Presupuesto: ${project.budget:.2f}"),
                ft.Text(f"Estado: {project.status}"),
                ft.Text(f"Creado: {project.created_at}"),
                ft.Text(f"Actualizado: {project.updated_at}")
            ], spacing=10),
            actions=[
                ft.TextButton("Cerrar", on_click=self.close_dialog)
            ]
        )
        self.page.dialog = confirm_dialog
        self.page.dialog.open = True
        self.page.update()
    
    def show_edit_project_dialog(self, project):
        """Muestra diálogo para editar proyecto"""
        name_field = ft.TextField(label="Nombre del Proyecto", value=project.name)
        client_name_field = ft.TextField(label="Nombre del Cliente", value=project.client_name)
        description_field = ft.TextField(label="Descripción", value=project.description, multiline=True)
        budget_field = ft.TextField(label="Presupuesto", value=str(project.budget), keyboard_type=ft.KeyboardType.NUMBER)
        status_dropdown = ft.Dropdown(
            label="Estado",
            value=project.status,
            options=[
                ft.dropdown.Option("pending", "Pendiente"),
                ft.dropdown.Option("in_progress", "En Progreso"),
                ft.dropdown.Option("completed", "Completado"),
                ft.dropdown.Option("cancelled", "Cancelado")
            ]
        )
        
        def update_project(e):
            try:
                if not name_field.value or not client_name_field.value:
                    self.page.snack_bar = ft.SnackBar(ft.Text("Nombre y cliente son obligatorios"), bgcolor="error")
                    self.page.snack_bar.open = True
                    self.page.update()
                    return
                
                budget = float(budget_field.value) if budget_field.value else 0.0
                
                project.name = name_field.value
                project.client_name = client_name_field.value
                project.description = description_field.value or ""
                project.budget = budget
                project.status = status_dropdown.value
                project.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                self.project_manager.update_project(project)
                self.close_dialog()
                self.load_projects()
                
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Proyecto '{project.name}' actualizado"), bgcolor="green")
                self.page.snack_bar.open = True
                self.page.update()
                
            except ValueError:
                self.page.snack_bar = ft.SnackBar(ft.Text("El presupuesto debe ser un número válido"), bgcolor="error")
                self.page.snack_bar.open = True
                self.page.update()
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="error")
                self.page.snack_bar.open = True
                self.page.update()
        
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Editar Proyecto"),
            content=ft.Column([
                name_field,
                client_name_field,
                description_field,
                budget_field,
                status_dropdown
            ], tight=True, spacing=15),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog),
                ft.ElevatedButton("Guardar", on_click=update_project)
            ]
        )
        self.page.dialog = confirm_dialog
        self.page.dialog.open = True
        self.page.update()
    
    def confirm_delete_project(self, project):
        """Confirma eliminación del proyecto"""
        def delete_project(e):
            try:
                self.project_manager.delete_project(project.id)
                self.close_dialog()
                self.load_projects()
                
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Proyecto '{project.name}' eliminado"), bgcolor="green")
                self.page.snack_bar.open = True
                self.page.update()
                
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"), bgcolor="error")
                self.page.snack_bar.open = True
                self.page.update()
        
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(f"¿Estás seguro de eliminar el proyecto '{project.name}'?\n\nEsta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog),
                ft.ElevatedButton(
                    "Eliminar", 
                    on_click=delete_project,
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
