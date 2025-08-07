import flet as ft
from utils.project_manager import ProjectManager
from utils.client_manager import ClientManager

class ProjectsView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.route = "/projects"
        self.page = page
        self.project_manager = ProjectManager()
        self.client_manager = ClientManager()
        
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
                    on_click=self.show_new_project_dialog,
                    icon_color="onprimary"
                )
            ],
            elevation=8,
            color="onprimary",
        )
        
        # Lista de proyectos
        self.projects_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
        )
        
        self.controls = [
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Row([
                            ft.Icon("work", size=32, color="primary"),
                            ft.Text(
                                "Gestión de Proyectos", 
                                size=24, 
                                weight=ft.FontWeight.BOLD,
                                color="primary"
                            )
                        ], spacing=10),
                        margin=ft.margin.only(bottom=20)
                    ),
                    self.projects_list
                ]),
                expand=True,
                padding=20
            )
        ]
        
        self.load_projects()
    
    def load_projects(self):
        """Carga la lista de proyectos"""
        self.projects_list.controls.clear()
        projects = self.project_manager.get_projects()
        
        if not projects:
            self.projects_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon("folder_off", size=64, color="onsurfacevariant"),
                        ft.Text(
                            "No hay proyectos creados",
                            size=18,
                            color="onsurfacevariant",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "Toca el botón '+' para crear tu primer proyecto",
                            size=14,
                            color="onsurfacevariant",
                            text_align=ft.TextAlign.CENTER
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    padding=40
                )
            )
        else:
            for project in projects:
                self.projects_list.controls.append(self.create_project_card(project))
        
        self.page.update()
    
    def create_project_card(self, project):
        """Crea una tarjeta para mostrar un proyecto"""
        # Determinar color del estado
        status_colors = {
            "pending": "amber",
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
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text(
                                project.name,
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="primary"
                            ),
                            ft.Text(
                                project.description or "Sin descripción",
                                size=14,
                                color="onsurfacevariant"
                            )
                        ], expand=True),
                        ft.Container(
                            content=ft.Text(
                                status_label,
                                size=12,
                                color="onprimary",
                                weight=ft.FontWeight.BOLD
                            ),
                            bgcolor=status_color,
                            padding=8,
                            border_radius=20
                        )
                    ]),
                    ft.Divider(height=10),
                    ft.Row([
                        ft.Text(f"Cliente: {project.client or 'No asignado'}", size=12),
                        ft.Text(f"Presupuesto: ${project.budget or 0}", size=12),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.TextButton(
                            text="Ver Detalles",
                            icon="visibility",
                            on_click=lambda _, p=project: self.show_project_details(p)
                        ),
                        ft.TextButton(
                            text="Editar", 
                            icon="edit",
                            on_click=lambda _, p=project: self.show_edit_project_dialog(p)
                        ),
                        ft.TextButton(
                            text="Eliminar",
                            icon="delete",
                            icon_color="error",
                            on_click=lambda _, p=project: self.confirm_delete_project(p)
                        )
                    ], alignment=ft.MainAxisAlignment.END)
                ], spacing=10),
                padding=16
            ),
            elevation=4,
            margin=ft.margin.symmetric(vertical=5)
        )
    
    def show_new_project_dialog(self, e):
        """Muestra diálogo para crear nuevo proyecto"""
        name_field = ft.TextField(label="Nombre del Proyecto", autofocus=True)
        description_field = ft.TextField(label="Descripción", multiline=True, max_lines=3)
        client_field = ft.TextField(label="Cliente")
        budget_field = ft.TextField(label="Presupuesto", keyboard_type=ft.KeyboardType.NUMBER)
        
        def create_project(e):
            try:
                project = self.project_manager.create_project(
                    name=name_field.value,
                    description=description_field.value
                )
                
                if client_field.value:
                    project.client = client_field.value
                if budget_field.value:
                    project.budget = float(budget_field.value)
                
                self.project_manager.update_project(
                    project.id,
                    client=project.client,
                    budget=project.budget
                )
                
                self.page.close_dialog()
                self.load_projects()
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Proyecto creado exitosamente"),
                    bgcolor="green"
                )
                self.page.snack_bar.open = True
                self.page.update()
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Error al crear proyecto: {str(ex)}"),
                    bgcolor="error"
                )
                self.page.snack_bar.open = True
                self.page.update()
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Nuevo Proyecto"),
            content=ft.Column([
                name_field,
                description_field, 
                client_field,
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
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(f"Detalles: {project.name}"),
            content=ft.Column([
                ft.Text(f"ID: {project.id}"),
                ft.Text(f"Descripción: {project.description or 'Sin descripción'}"),
                ft.Text(f"Estado: {project.status}"),
                ft.Text(f"Cliente: {project.client or 'No asignado'}"),
                ft.Text(f"Presupuesto: ${project.budget or 0}"),
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
        name_field = ft.TextField(label="Nombre", value=project.name)
        description_field = ft.TextField(
            label="Descripción", 
            value=project.description or "",
            multiline=True,
            max_lines=3
        )
        client_field = ft.TextField(label="Cliente", value=project.client or "")
        budget_field = ft.TextField(
            label="Presupuesto",
            value=str(project.budget or 0),
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
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
                success, msg = self.project_manager.update_project(
                    project.id,
                    name=name_field.value,
                    description=description_field.value,
                    client=client_field.value,
                    budget=float(budget_field.value) if budget_field.value else None,
                    status=status_dropdown.value
                )
                
                self.page.close_dialog()
                self.load_projects()
                
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(msg),
                    bgcolor="green" if success else "error"
                )
                self.page.snack_bar.open = True
                self.page.update()
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Error al actualizar: {str(ex)}"),
                    bgcolor="error"
                )
                self.page.snack_bar.open = True
                self.page.update()
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Editar Proyecto"),
            content=ft.Column([
                name_field,
                description_field,
                client_field,
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
            success, msg = self.project_manager.delete_project(project.id)
            self.page.close_dialog()
            
            if success:
                self.load_projects()
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Proyecto eliminado"),
                    bgcolor="green"
                )
            else:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Error: {msg}"),
                    bgcolor="error"
                )
            
            self.page.snack_bar.open = True
            self.page.update()
        
        self.page.dialog = ft.AlertDialog(
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
         
         d e f   c l o s e _ d i a l o g ( s e l f ,   e = N o n e ) :  
                 " " " C i e r r a   e l   d i � � l o g o   a c t i v o " " "  
                 i f   s e l f . p a g e . d i a l o g :  
                         s e l f . p a g e . d i a l o g . o p e n   =   F a l s e  
                         s e l f . p a g e . u p d a t e ( )  
 